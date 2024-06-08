from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from ingest import IngestManage
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
            to answer the question. If you don't know the answer, just say that you don't know.
            {format_answer}
            [/INST] </s> 
            [INST] Question: {input} 
            Context: {context} 
            Answer: [/INST]
            """
        )

        self.ingest = IngestManage()
        self.retriever = self.ingest.retriver()

        self.document_chain = create_stuff_documents_chain(self.model, self.prompt)
        self.chain = create_retrieval_chain(self.retriever, self.document_chain)

        # self.chain = (
        #     {"context": self.retriever, "input": RunnablePassthrough()}
        #     | self.prompt
        #     | self.model
        #     | StrOutputParser()
        # )


    

    def get_chat_chain(self, document):

        self.ingest.ingest_document(document)

        self.retriever = self.ingest.retriver()

        self.chain = create_retrieval_chain(self.retriever, self.document_chain)

        # self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
        #         | self.prompt
        #         | self.model
        #         | StrOutputParser())
        

    def ask(self, query: str, max_len = 1024, format_answer = "") -> str:
        self.model = ChatOllama(model=MODEL_LLM, num_predict=max_len)

        result = self.chain.invoke({"input": query, "format_answer": format_answer})

        if not result["context"]:
            return "Aucun fichier trouvé ne correspond à la question."

        sources = []
        for doc in result["context"]:
            sources.append(
                {"source": doc.metadata["source"], "page_content": doc.page_content}
            )
        print(sources)

        return result["answer"]
    



# llm = Llm()
# print(llm.ask("Donne moi la liste des différentes limites.", format_answer="List as much as you can. Separate them by a comma. Start with a [ and finish with ]."))


# print(llm.ask("Peut on avoir une asynptote oblique ?", max_len = 1, format_answer="Answer with Yes or No only."))



# Ancienne version de ask, avec : self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                            #         | self.prompt
                            #         | self.model
                            #         | StrOutputParser())

# def ask(self, query: str, max_len = 1024) -> str:
#     self.model = ChatOllama(model=MODEL_LLM, num_predict=max_len)

#     result = self.chain.invoke(query)

#     return result