from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStoreRetriever


from src.embedding.embedding import EmbeddingManage
from src.embedding.vector_store import VectorStoreManage
from src.embedding.chunks import Chunks

from src.settings import CHROMA_PATH


class IngestManage:
    '''
        A class used to manage the ingestion and retrieval of documents into/from a vector store.

        This class initializes with an embedding model and a vector store. It provides methods
        to ingest documents by chunking them and adding them to the vector store, and to retrieve
        similar documents based on a similarity score threshold.

        Attributes
        ----------
        embedding : 
            An instance of tembedding model used for generating document embeddings.
        vector_store : VectorStore
            An instance of the vector store configured for storing and retrieving document vectors.

        Methods
        -------
        ingest_document(document)
            Processes the given document by chunking it and adding the chunks to the vector store.
        retriever() -> Callable
            Returns a retriever configured to search for documents based on similarity score threshold.
    '''

    def __init__(self) -> None:

        self.embedding = EmbeddingManage().embedding
        self.vector_store = VectorStoreManage().get_vector_from_db(Chroma, self.embedding, CHROMA_PATH)



    def ingest_document(self, document: str) -> None:

        chunks = Chunks(document).get_chunks()

        self.vector_store = VectorStoreManage().get_vector_from_chunks(chunks, Chroma, self.embedding, CHROMA_PATH)
    

    def retriver(self) -> VectorStoreRetriever:

        return self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 5, # on récupére seulement 5 passages
                "score_threshold": 0.5,
            },
        )
    
    def retriver_from_doc(self, name_of_the_document : str) -> VectorStoreRetriever:
        
        return self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 5, # on récupére seulement 5 passages
                "score_threshold": 0.5,
                'filter': {'paper_title': name_of_the_document},
            },
        )
