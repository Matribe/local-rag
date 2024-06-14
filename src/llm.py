from langchain_community.chat_models import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate


from src.embedding.ingest import IngestManage
from src.settings import MODEL_LLM
from src.prompt import PromptManage
from src.chroma import ChromaManage
from src.utils.exemples import EXEMPLE1

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

    def __init__(self, type_return = None) -> None:

        self.type_return = type_return

        self.model = ChatOllama(model=MODEL_LLM)

        self.prompt = PromptTemplate.from_template(
                """
                    <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
                    to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
                    maximum and keep the answer concise. [/INST] </s>

                    [INST] Retrieve the items in the following format :
                        {EXEMPLE1} 
                    [/INST] 
                    
                    [INST] Question: {input} 
                    Context: {context} 
                    Answer: [/INST]
                """
            )

        self.ingest = IngestManage()
        self.retriever = self.ingest.retriver()

        self.document_chain = create_stuff_documents_chain(self.model, self.prompt)
        self.chain = create_retrieval_chain(self.retriever, self.document_chain)

    

    def get_chat_chain(self, document):

        sources = ChromaManage().sources()


        if document not in sources:

            self.ingest.ingest_document(document)
            self.retriever = self.ingest.retriver()
            self.chain = create_retrieval_chain(self.retriever, self.document_chain)

        

    def ask(self, query: str, max_len = 1024) -> str:
        self.model = ChatOllama(model=MODEL_LLM, num_predict=max_len)

        result = self.chain.invoke({"input": query, "EXEMPLE1": EXEMPLE1})

        if not result["context"]:
            return "Aucun document trouvé correspondant à la question."

        sources = []
        for doc in result["context"]:
            sources.append(
                {"source": doc.metadata["source"], "page_content": doc.page_content}
            )
        # print(sources)

        return result["answer"]

