import chromadb

from src.settings import CHROMA_PATH

class ChromaManage:
        
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path= CHROMA_PATH)


    def collection(self, name="langchain"):
            return self.client.get_collection(name=name)


    def documents(self, name="langchain"):
        return self.collection(name).get(include=["metadatas"])["metadatas"]
    
    def sources(self, name="langchain"):
        return list(set(doc['source'] for doc in self.documents(name)))