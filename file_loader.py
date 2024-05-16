from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader, Docx2txtLoader
from langchain_core.documents import Document
from pathlib import Path

FILE_READER = {
    ".md": UnstructuredMarkdownLoader,
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
}


class FileLoader:
    '''
        A class used to transform files into a list of Document objects.
        
        This class provides a static method to read a file, determine its type
        based on the file extension, and use the appropriate reader to convert
        the file contents into Document objects.
        
        Methods
        -------
        transform_file_into_documents(file_name: str) -> list[Document]
            Reads a file and returns a list of Document objects based on the file content.
    '''

    @staticmethod
    def transform_file_into_documents(file_name: str) -> list[Document]:
        extension = Path(file_name).suffix
        reader = FILE_READER[extension]
        documents = reader(file_name)
        return documents.load()


