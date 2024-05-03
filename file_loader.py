from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader, Docx2txtLoader


class FileLoader:

    def __init__(self, file_path):
        if file_path.endswith('.md'):
            self.document = UnstructuredMarkdownLoader(file_path)
        elif file_path.endswith('.pdf'):
            self.document = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            self.document = Docx2txtLoader(file_path)
    
    
    def load(self):
        return self.document.load()

