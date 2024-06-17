from langchain_community.chat_models import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


from src.embedding.ingest import IngestManage
from src.settings import MODEL_LLM
from src.prompt import PromptManage
from src.embedding.chroma import ChromaManage
from src.utils.exemples import JSON_EXEMPLE

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

        self.prompt = PromptManage(type_return="Json").answer_prompt

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

        result = self.chain.invoke({"input": query, "type_return": JSON_EXEMPLE})

        print("\n------- Prompt : -------")
        print(self.prompt.format(input=query, type_return=JSON_EXEMPLE, context = result["context"]))

        if not result["context"]:
            return "Aucun document trouvé correspondant à la question."

        sources = []
        for doc in result["context"]:
            sources.append(
                {"source": doc.metadata["source"], "page_content": doc.page_content}
            )
        # print(sources)

        return result["answer"], sources

