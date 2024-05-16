from langchain_community.embeddings import HuggingFaceEmbeddings
import uuid
import os
import json
import chromadb


class ChromaManager:

    def __init__(self, chroma_path, docs_path, embedding_model = "BAAI/bge-base-en-v1.5"):
        self.chroma_path = chroma_path
        self.docs_path = docs_path

        self.embedding_model = embedding_model

        self.documents = self.map_documents_to_ids()

        self.client = chromadb.PersistentClient(
            path=self.chroma_path
        )
        self.collection = self.client.get_or_create_collection(
            name="RAG",
            # embedding_function = HuggingFaceEmbeddings(
            #     model_name=self.embedding_model,
            #     encode_kwargs = {"normalize_embeddings": True},
            #     ),
            )


    # def save_to_chroma(self, chunks):
    #     vector_store = Chroma.from_documents(
    #         documents=chunks,
    #         embedding=HuggingFaceEmbeddings(
    #             model_name=self.embedding_model,
    #             encode_kwargs = {"normalize_embeddings": True},
    #             ),
    #         persist_directory=self.path
    #         )
    #     vector_store.persist()

    #     return vector_store


    def map_documents_to_ids(self):
        if os.path.exists(self.docs_path + "/documents_to_ids.json"):
            with open(self.docs_path + "/documents_to_ids.json", "r") as fichier_json:
                # Charger le contenu JSON
                return json.load(fichier_json)
        else:
            with open(self.docs_path + "/documents_to_ids.json", "w") as fichier_json:
                json.dump({}, fichier_json)
                return {}
    
    def add_documents(self, list_of_documents, list_of_ids):
        self.collection.add(
            documents = list_of_documents,
            ids = list_of_ids
        )


CHROMA_PATH = "chroma"
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"
DATA_PATH = "data"

db = ChromaManager(CHROMA_PATH, DATA_PATH)