from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.documents import Document

from llm.utils.file_loader import FileLoader


TEXT_SPLITTER = RecursiveCharacterTextSplitter(
        chunk_size=1024, 
        chunk_overlap=100
    )


class Chunks:
    '''
        A class used to manage and process document chunks for vector storage.

        This class initializes by transforming a given document into a list of `Document`
        objects, splitting these documents into smaller chunks, and filtering out any
        metadata types that are not supported for vector storage.

        Attributes
        ----------
        docs : list[Document]
            A list of `Document` objects obtained from the input file.
        chunks : list
            A list of smaller document chunks generated from `docs`.
        filtered_chunks : list
            A list of filtered document chunks with unsupported metadata types removed.

        Methods
        -------
        get_chunks() -> list
            Returns the list of filtered document chunks.
    '''

    def __init__(self, document : str) -> None:
        self.docs = FileLoader().transform_file_into_documents(document)
    
        self.chunks = TEXT_SPLITTER.split_documents(self.docs)

        # Filter out metadata types that are not supported for a vector store.
        self.filtered_chunks = filter_complex_metadata(self.chunks)
    
    def get_chunks(self) -> list[Document]:
        return self.filtered_chunks

