from langchain.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM  # LLM remains unchanged
import chromadb
import os

# Define the LLM model to be used
llm_model = "llama3.2:1b"

# Configure ChromaDB
# Initialize the ChromaDB client with persistent storage in the current directory
chroma_client = chromadb.PersistentClient(path="M:/HackCU11/backend/chroma_db")

# Define a custom embedding function for ChromaDB using HuggingFace embeddings
class ChromaDBEmbeddingFunction:
    """
    Custom embedding function for ChromaDB using embeddings.
    """
    def __init__(self, langchain_embeddings):
        self.langchain_embeddings = langchain_embeddings

    def __call__(self, input):
        # Ensure the input is in a list format for processing
        if isinstance(input, str):
            input = [input]
        return self.langchain_embeddings.embed_documents(input)

# Initialize the embedding function with HuggingFace embeddings
embedding = ChromaDBEmbeddingFunction(
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
)

# Define a collection for the RAG workflow
collection_name = "conversation_ansh"
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    metadata={"description": "A collection for RAG with HuggingFace embeddings - Demo1"},
    embedding_function=embedding  # Use the custom embedding function
)

# Function to show all collections and their documents
def show_all_collections():
    """
    Display all collections and print the actual text (words) from each document stored.
    """
    try:
        collections = chroma_client.list_collections()  # List all collection names
        if not collections:
            print("No collections found in the database.")
            return

        print("All Collections in the Database:")
        for col in collections:
            print(f"\nCollection: {col.name}")
            coll_obj = chroma_client.get_collection(col.name, embedding_function=embedding)
            print(coll_obj, type(coll_obj))
            # Retrieve documents, embeddings, and metadatas (excluding ids)
            results = coll_obj.get(include=["documents", "embeddings", "metadatas"])
            documents = results.get("documents", [])
            print(documents)

    except Exception as e:
        print(f"Error while retrieving collections or documents: {str(e)}")

# Function to add documents to the ChromaDB collection
def add_documents_to_collection(documents, ids):
    """
    Add documents to the ChromaDB collection.
    
    Args:
        documents (list of str): The documents to add.
        ids (list of str): Unique IDs for the documents.
    """
    collection.add(
        documents=documents,
        ids=ids
    )

# Function to query the ChromaDB collection
def query_chromadb(query_text, n_results=3):
    """
    Query the ChromaDB collection for relevant documents.
    
    Args:
        query_text (str): The input query.
        n_results (int): The number of top results to return.
    
    Returns:
        list of dict: The top matching documents and their metadata.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results["documents"], results["metadatas"]

# Function to interact with the Ollama LLM
def query_ollama(prompt):
    """
    Send a query to Ollama and retrieve the response.
    
    Args:
        prompt (str): The input prompt for Ollama.
    
    Returns:
        str: The response from Ollama.
    """
    llm = OllamaLLM(model=llm_model)
    return llm.invoke(prompt)

# RAG pipeline: Combine ChromaDB and Ollama for Retrieval-Augmented Generation
def rag_pipeline(query_text):
    """
    Perform Retrieval-Augmented Generation (RAG) by combining ChromaDB and Ollama.
    
    Args:
        query_text (str): The input query.
    
    Returns:
        str: The generated response from Ollama augmented with retrieved context.
    """
    # Step 1: Retrieve relevant documents from ChromaDB
    retrieved_docs, metadata = query_chromadb(query_text)
    print("Type of metadata:", type(metadata))

    # Flatten the list if needed (in case retrieved_docs is a list of lists)
    context = " ".join([doc for sublist in retrieved_docs for doc in (sublist if isinstance(sublist, list) else [sublist])]) if retrieved_docs else "No relevant documents found."

    # Step 2: Send the query along with the context to Ollama
    augmented_prompt = f"Context: {context}\n\nQuestion: {query_text}\nAnswer:"
    print("######## Augmented Prompt ########")
    print(augmented_prompt)

    response = query_ollama(augmented_prompt)

    # Step 3: Store the new response in ChromaDB for future reference
    doc_id = f"doc{len(metadata) + 1}"  # Simple way to generate new unique IDs
    add_documents_to_collection([response], [doc_id])

    # Optionally, store the facts from the response as new context in ChromaDB
    facts = extract_facts(response)  # This is a placeholder for a function you might create for extracting facts.
    add_documents_to_collection(facts, [f"fact_{doc_id}" for _ in range(len(facts))])
    show_all_collections()
    return response

def extract_facts(response):
    """
    Extract relevant facts or pieces of information from the response.
    
    Args:
        response (str): The generated response from Ollama.
    
    Returns:
        list: A list of extracted facts (strings).
    """
    # Example: Extract facts from the response by splitting on sentences.
    facts = response.split(". ")
    return facts

# Function to interact with the user and handle queries dynamically
def ask_question():
    """
    Function to allow the user to input questions and get RAG responses.
    """
    while True:
        query = input("Please ask a question: ")
        
        if query.lower() in ['exit', 'quit', 'bye']:
            print("Exiting the conversation.")
            break
        
        response = rag_pipeline(query)
        print(f"Answer: {response}")

# Example usage
show_all_collections()
ask_question()  # Start the interactive Q&A loop
