from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.embeddings.
from llama_index.core import Settings

import chromadb
from chromadb.config import Settings
import os

class Chroma:
    def __init__(self, collection_name = "rag_demo"):
        # os.environ['OPENAI_API_KEY'] = 'ollama'
        self.embedding_function = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        # self.Settings = self.embedding_function
        self.chroma_client = chromadb.PersistentClient(
            path="./chroma_db",
            # persist_directory="/c/Users/aup/source/repos/HackCU11/chroma_db",
            # anonymized_telemetry=False
        )
        self.chroma_client.heartbeat()
        self.collection_name = collection_name

    def add(self, document):
        # document is of the form {"id": "doc1", "content": "Python is a versatile programming language."}
        collection = self.chroma_client.get_or_create_collection(self.collection_name)
        embedding = self.embedding_function.get_text_embedding(document['content'])
        # embed_query(document['content'])
        collection.add(
            documents=[document['content']],
            ids=[document['id']],
            embeddings=[embedding]
        )

    def query(self, query_text):
        query_embedding = self.embedding_function.get_text_embedding(query_text)

        collection = self.chroma_client.get_or_create_collection(self.collection_name)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        retrieved_docs = results['documents'][0]
        return retrieved_docs