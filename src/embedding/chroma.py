import chromadb

from src.settings import CHROMA_PATH

class ChromaManage:
    '''
        A class for managing data retrieval from a ChromaDB instance.

        Attributes
        ----------
            client (chromadb.PersistentClient): The persistent client instance connected to ChromaDB.

        Methods
        -------
            collection(name="langchain"):
                Retrieves a collection from ChromaDB.
            documents(name="langchain"):
                Retrieves documents from a specific collection in ChromaDB.           
            sources(name="langchain"):
                Retrieves unique sources from documents in a specific collection in ChromaDB.
    '''

        
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path= CHROMA_PATH)


    def collection(self, name="langchain"):
            return self.client.get_collection(name=name)

    def documents(self, name="langchain"):
        return self.collection(name).get(include=["metadatas"])["metadatas"]
    
    def sources(self, name="langchain"):
        return list(set(doc['source'] for doc in self.documents(name)))