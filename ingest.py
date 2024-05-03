
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.utils import filter_complex_metadata

from file_loader import FileLoader

class Ingest:

    docs = None

    def __init__(self, file_path: str, text_splitter, prompt, llm_model, embedding_model = "BAAI/bge-base-en-v1.5"):

        self.docs = FileLoader(file_path=file_path).load()

        chunks = text_splitter.split_documents(self.docs)
        self.chunks = filter_complex_metadata(chunks)
        
        self.prompt = prompt
        self.llm_model = llm_model
        self.embedding_model = embedding_model

        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=HuggingFaceEmbeddings(
                model_name=self.embedding_model,
                encode_kwargs = {"normalize_embeddings": True},
                )
            )
        
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5,
            },
        )




