from langchain.prompts import PromptTemplate
from src.settings import MODEL_LLM

class PromptManage:

    '''
        A class for managing prompts and generating responses based on templates.

        This class initializes with a prompt template for generating answers to questions. 
        It can handle different types of return formats and provides methods for generating 
        specific prompts.

        Attributes
        ----------
        answer_prompt : PromptTemplate
            A template for generating prompts to answer questions, initialized based on the 
            specified language model (MODEL_LLM).

        Methods
        -------
        return_list() -> str:
            Generates a prompt instructing the user to list items separated by commas.

        return_yes_or_no() -> str:
            Generates a prompt instructing the user to answer with "Yes" or "No" only.
    '''


    def __init__(self):

        if MODEL_LLM == "mistral":
            self.answer_prompt = PromptTemplate.from_template(
                """
                <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
                    to answer the question. If you don't know the answer, just say that you don't know.
                    The answer must be a list of tuple. Separate answer by a comma.
                        Example :
                        {example}
                    [/INST] </s>

                    [INST] Question : Give me some for the tuple {input}
                    Context: {context} 
                    Answer: [/INST]
                """
            )
        elif MODEL_LLM == "llama3":
            self.answer_prompt = PromptTemplate.from_template(
                """
                    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
                    Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
                    Don't make a sentence. The answer must be a list of tuple. Separate answer by a comma.
                    Example :
                    {example}
                    <|start_header_id|>user<|end_header_id|>
                    Question : Give me some for the tuple {input}
                    Context: {context}
                    <|start_header_id|>assistant<|end_header_id|>
                """
            )
        else:
            self.answer_prompt = PromptTemplate.from_template(
                """
                    Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
                    Don't make a sentence. The answer must be a list of tuple. Separate answer by a comma.
                    Example :
                    {example}
                    Question : Give me some for the tuple {input}
                    Context: {context}
                """
            )
              

    def return_list(self) -> str:
        return "<INST> Separate them by a comma. List as much as you can.</INST>"
    
    
    def return_yes_or_no(self) -> str:
        return "<INST> Answer with Yes or No only.</INST>"

