
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.utils import filter_complex_metadata

from file_loader import FileLoader

class Ingest:
    '''
        Enables converting documents into vectors of numbers for classifying different texts.
    '''

    docs = None

    def __init__(self, file_path: str, text_splitter, embedding_model = "BAAI/bge-base-en-v1.5"):
        '''
            Args:
                file_path : link to the folder containing the files
                text_splitter : splits the documents
                embedding_model :  model used for embedding
        '''

        self.docs = FileLoader(file_path=file_path).load()

        chunks = text_splitter.split_documents(self.docs)
        self.chunks = filter_complex_metadata(chunks)
        
        self.embedding_model = embedding_model


        # Enables creating a vector representation of the documents.
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=HuggingFaceEmbeddings(
                model_name=self.embedding_model,
                encode_kwargs = {"normalize_embeddings": True},
                )
            )
        

        # Enables selecting a set of documents or passages that are likely to contain relevant information.
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3, # on récupére seulement 3 passages
                "score_threshold": 0.5,
            },
        )




