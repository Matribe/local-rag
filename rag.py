from langchain_community.chat_models import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from ingest import Ingest
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import ConfigurableField

# RAG : Retrieval Augmented Generation

class ChatPDF:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):
        self.model = ChatOllama(model="mistral")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024,
                                                            chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
             maximum and keep the answer concise. [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )


    def add_files(self, file_path: str):
        files = Ingest(file_path, self.text_splitter)

        self.retriever = files.retriever
        
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                    | self.prompt
                    | self.model
                    | StrOutputParser())


    def ask(self, query: str, max_len = 1024):
        if not self.chain:
            return "Please, add a PDF document first."
        self.model = ChatOllama(model="mistral", num_predict=max_len)
        return self.chain.invoke(query)


    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None

