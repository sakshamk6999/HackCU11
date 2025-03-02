# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain_ollama import OllamaEmbeddings
import chromadb
from chromadb.config import Settings
import os
os.environ['OPENAI_API_KEY'] = 'ollama'

class Chroma:
    def __init__(self, collection_name = "rag_demo"):
        os.environ['OPENAI_API_KEY'] = 'ollama'
        self.embedding_function = OllamaEmbeddings(model="llama3.2:1b")
        self.chroma_client = chromadb.PersistentClient(settings=Settings(
            persist_directory="./chroma_db",
            # persist_directory="/c/Users/aup/source/repos/HackCU11/chroma_db",
            anonymized_telemetry=False
        ))
        self.collection_name = collection_name

    def add(self, document):
        # document is of the form {"id": "doc1", "content": "Python is a versatile programming language."}
        collection = self.chroma_client.get_or_create_collection(self.collection_name)
        embedding = self.embedding_function.embed_query(document['content'])
        collection.add(
            documents=[document['content']],
            ids=[document['id']],
            embeddings=[embedding]
        )

    def query(self, query_text):
        query_embedding = self.embedding_function.embed_query(query_text)

        collection = self.chroma_client.get_or_create_collection(self.collection_name)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        retrieved_docs = results['documents'][0]
        return retrieved_docs