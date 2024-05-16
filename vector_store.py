

class VectorStore:
    '''
        A class used to manage vector storage and retrieval.

        This class provides static methods to interact with a vector store, including
        methods to store vectors obtained from document chunks and to retrieve vectors
        from a pre-existing database.

        Methods
        -------
        get_vector_from_chunks(chunks, db, embedding, db_path)
            Retrieves vectors from document chunks and stores them in a vector database.
        get_vector_from_db(db, embedding, db_path)
            Retrieves vectors from a pre-existing vector database.
    '''
    
    @staticmethod
    def get_vector_from_chunks(chunks, db, embedding, db_path):
        vectore_store = db.from_documents(
                documents = chunks,
                embedding = embedding,
                persist_directory = db_path
            )
        vectore_store.persist()

        return vectore_store

    @staticmethod
    def get_vector_from_db(db, embedding, db_path):
        return  db(
            persist_directory = db_path,
            embedding_function = embedding,
        )

