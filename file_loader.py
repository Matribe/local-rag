from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader, Docx2txtLoader


class FileLoader:
    '''
        Allows to retrieve different types of files: md, pdf, and docx in order to be able to split them.    
    '''

    def __init__(self, document):
        if document.endswith('.md'):
            self.document = UnstructuredMarkdownLoader(document)
        elif document.endswith('.pdf'):
            self.document = PyPDFLoader(document)
        elif document.endswith('.docx'):
            self.document = Docx2txtLoader(document)
    
    
    def load(self):
        return self.document.load()

