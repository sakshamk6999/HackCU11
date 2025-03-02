#!/usr/bin/env python3
#
# Copyright © 2023 Advanced Micro Devices, Inc. All rights reserved.
#

import argparse
import os
import time
import re
from transformers import set_seed

# --- New LLM using lemonade.api ---
from lemonade.api import from_pretrained
import chromadb

# --- Embedding and Settings Imports ---
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # Llama_index embedding
from llama_index.core import Settings  # For embedding model assignment

# Set a fixed seed for reproducibility
set_seed(123)

# Set the embedding model using llama_index's HuggingFaceEmbedding.
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Define the new OllamaModel class.
class OllamaModel:
    def __init__(self):
        self.model, self.tokenizer = from_pretrained(
            "amd/Llama-3.2-3B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid", recipe="oga-hybrid"
        )
        # Initialize a persistent ChromaDB client (used here for side effects).
        chromadb.PersistentClient(path="M:/HackCU11/backend/chroma_db")
        self.ANSH_SYSTEM_PROMPT = """
            You are Ansh, a young Indian boy who is the user's friend and digital diary. 
            Your personality traits:
            - Keeps responses brief (under 100 words)

            Your responses should:
            1. Ask follow-up questions to learn more about the user
            2. Be supportive and positive
            """
    
    def ask(self, prompt: str):
        # Generate an initial answer.
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        response1 = self.model.generate(input_ids)
        decoded_response1 = self.tokenizer.decode(response1[0])
        
        # Build an extraction prompt to obtain key facts.
        extraction_prompt = f"""
            Extract key facts and information from the following message. 
            Focus on personal details, events, preferences, emotions, and relationships.
            Format the output as a JSON list of facts.
            
            User message: {decoded_response1}
            
            Output format:
            [
            "fact 1",
            "fact 2",
            ...
            ]
        """
        pattern1 = "Here is the output in JSON format:"
        input_ids = self.tokenizer(self.ANSH_SYSTEM_PROMPT + extraction_prompt, return_tensors="pt").input_ids
        response = self.model.generate(input_ids, max_new_tokens=1000)
        decoded_response = self.tokenizer.decode(response[0])
    
        reg_match = re.search(pattern1, decoded_response)
        if reg_match:
            extracted = decoded_response[reg_match.end():]
            reg_match2 = re.search("]", extracted)
            if reg_match2:
                extracted = extracted[:reg_match2.start()]
            extracted = extracted.replace('\n', ' ').replace('\r', '').replace("\"", '').replace("[", '')
            facts = [fact.strip() for fact in extracted.split(",") if fact.strip()]
            return facts
        return decoded_response.split(". ")

# Define a custom embedding function for ChromaDB that uses the llama_index embeddings.
class ChromaDBEmbeddingFunction:
    def __init__(self, llama_embedding):
        self.llama_embedding = llama_embedding

    def __call__(self, input):
        # Ensure the input is a list of strings.
        if isinstance(input, str):
            input = [input]
        return self.llama_embedding.embed_documents(input)

if __name__ == "__main__":
    # --- Parse Command-Line Arguments ---
    parser = argparse.ArgumentParser(description='AMD Chatbot Parameters with OllamaModel using llama_index embeddings')
    parser.add_argument("--direct_llm", help="Run LLM directly (--direct_llm) or via an augmented prompt (--no-direct_llm).", required=True, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    print(f"Arguments: {args}")
    
    # --- Initialize the LLM using OllamaModel ---
    ollama = OllamaModel()
    
    # --- Setup the embedding function for ChromaDB using llama_index's embedding.
    embedding_function = ChromaDBEmbeddingFunction(Settings.embed_model)
    
    # --- Initialize ChromaDB ---
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection_name = "conversation_ansh"
    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "A collection for RAG with llama_index embeddings"},
        embedding_function=embedding_function
    )
    
    # --- Helper Functions for ChromaDB ---
    def show_all_collections():
        try:
            collections = chroma_client.list_collections()
            if not collections:
                print("No collections found in the database.")
                return
            print("All Collections in the Database:")
            for col in collections:
                print(f"\nCollection: {col.name}")
                coll_obj = chroma_client.get_collection(col.name, embedding_function=embedding_function)
                results = coll_obj.get(include=["documents", "embeddings", "metadatas"])
                documents = results.get("documents", [])
                print("Documents:", documents)
        except Exception as e:
            print(f"Error while retrieving collections: {str(e)}")
    
    def add_documents_to_collection(documents, ids):
        collection.add(documents=documents, ids=ids)
    
    def query_chromadb(query_text, n_results=3):
        results = collection.query(query_texts=[query_text], n_results=n_results)
        return results["documents"], results["metadatas"]
    
    # --- RAG Pipeline ---
    def rag_pipeline(query_text):
        # Step 1: Retrieve context from ChromaDB.
        retrieved_docs, metadata = query_chromadb(query_text)
        if retrieved_docs:
            flat_docs = []
            for doc in retrieved_docs:
                if isinstance(doc, list):
                    flat_docs.extend(doc)
                else:
                    flat_docs.append(doc)
            context = " ".join(flat_docs)
        else:
            context = "No relevant documents found."
    
        # Step 2: Augment the prompt with the retrieved context.
        augmented_prompt = f"Context: {context}\n\nQuestion: {query_text}\nAnswer:"
        print("\n######## Augmented Prompt ########")
        print(augmented_prompt)
    
        # Step 3: Call the LLM.
        try:
            if args.direct_llm:
                llm_response = ollama.ask(query_text)
            else:
                llm_response = ollama.ask(augmented_prompt)
        except Exception as e:
            print("Error during LLM query:", e)
            llm_response = ["Error retrieving response."]
    
        # If the response is a list of facts, join them into a single string.
        if isinstance(llm_response, list):
            response_text = " ".join(llm_response)
        else:
            response_text = llm_response
    
        # Step 4: Store the LLM response in ChromaDB.
        doc_id = f"doc_{int(time.time())}"
        add_documents_to_collection([response_text], [doc_id])
    
        # Optionally, extract facts from the response and store them separately.
        facts = [fact.strip() for fact in response_text.split(". ") if fact.strip()]
        for idx, fact in enumerate(facts):
            add_documents_to_collection([fact], [f"fact_{doc_id}_{idx}"])
    
        show_all_collections()
        return response_text
    
    # --- Interactive Q&A Loop ---
    def ask_question():
        print("\nType your questions below. Enter 'exit', 'quit', or 'bye' to end the session.\n")
        while True:
            query = input("Please ask a question: ")
            if query.lower() in ['exit', 'quit', 'bye']:
                print("Exiting the conversation.")
                break
            answer = rag_pipeline(query)
            print(f"\nAnswer: {answer}\n")
    
    # Show existing collections then enter interactive loop.
    show_all_collections()
    ask_question()
