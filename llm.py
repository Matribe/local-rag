from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from ingest import Ingest
from constants import MODEL_LLM


class Llm:
    '''
        A class used for question-answering tasks using a language model.

        This class initializes a language model, a prompt template, and an ingestion process for documents.
        It provides methods to ingest documents, set up a retrieval chain, and ask questions using the model.

        Attributes
        ----------
        model : ChatOllama
            An instance of the ChatOllama model configured for generating responses.
        prompt : PromptTemplate
            A template for structuring the input prompt for the model.
        ingest : Ingest
            An instance of the Ingest class used to process and store documents.
        retriever : Callable
            A retriever callable that queries the vector store for relevant document passages.
        chain : Callable
            A processing chain that retrieves context, formats the prompt, and generates a response.

        Methods
        -------
        get_chat_chain(document)
            Ingests a document and sets up the retrieval and response generation chain.
        ask(query: str, max_len=1024)
            Asks a question to the model and returns the response.
    '''

    def __init__(self) -> None:

        self.model = ChatOllama(model=MODEL_LLM)

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

        self.ingest = Ingest()
        self.retriever = self.ingest.retriver()

        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.model
            | StrOutputParser())


    

    def get_chat_chain(self, document):

        self.ingest.ingest_document(document)

        self.retriever = self.ingest.retriver()

        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                | self.prompt
                | self.model
                | StrOutputParser())
        

    def ask(self, query: str, max_len = 1024):
        self.model = ChatOllama(model=MODEL_LLM, num_predict=max_len)

        return self.chain.invoke(query)
