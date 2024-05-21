from langchain_community.embeddings import HuggingFaceEmbeddings


from constants import EMBEDDING_MODEL_NAME



class EmbeddingManage:
    '''
        A class used to generate embeddings for documents using a Hugging Face model.

        This class initializes an embedding model from Hugging Face with specified parameters.
        It can be used to encode documents into vector representations.

        Attributes
        ----------
        embedding : HuggingFaceEmbeddings
            An instance of the HuggingFaceEmbeddings class configured with the specified model and encoding parameters.
        
        Methods
        -------
        (None currently defined)
    '''

    def __init__(self) -> None:
        self.embedding = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL_NAME,
                encode_kwargs = {"normalize_embeddings": True},
            )
