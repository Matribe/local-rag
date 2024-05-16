from langchain_community.vectorstores import Chroma
from embedding import Embedding
from vector_store import VectorStore
from chunks import Chunks


CHROMA_PATH = "chroma"

class Ingest:
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

        self.embedding = Embedding().embedding
        self.vector_store = VectorStore().get_vector_from_db(Chroma, self.embedding, CHROMA_PATH)



    def ingest_document(self, document: str) -> None:

        chunks = Chunks(document).get_chunks()

        self.vector_store = VectorStore().get_vector_from_chunks(chunks, Chroma, self.embedding, CHROMA_PATH)
    

    def retriver(self):

        return self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3, # on récupére seulement 3 passages
                "score_threshold": 0.5,
            },
        )
