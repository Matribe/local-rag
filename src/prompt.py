from langchain.prompts import PromptTemplate
from src.utils.string import StringGenerator
from src.utils.exemples import *


class PromptManage:

    '''
        A class for managing prompts and generating responses based on templates.

        This class initializes with a prompt template for generating answers to questions. 
        It can handle different types of return formats and provides methods for generating 
        specific prompts.

        Attributes
        ----------
        answer_prompt : PromptTemplate
            A template for generating prompts to answer questions, initialized based on whether 
            a specific type of return is provided or not.


        Methods
        -------
        return_list() -> str:
            Generates a prompt instructing the user to answer with "Yes" or "No" only.
        return_yes_or_no() -> str:
            Generates a prompt instructing the user to list items separated by commas.
    '''


    def __init__(self, type_return = None):

        if not type_return:
            self.answer_prompt = PromptTemplate.from_template(
                """
                    <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
                    to answer the question. If you don't know the answer, just say that you don't know.[/INST] </s>
                    
                    [INST] Question: {input} 
                    Context: {context} 
                    Answer: [/INST]
                """
            )
        else:
            self.answer_prompt = PromptTemplate.from_template(
                """
                    <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
                    to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
                    maximum and keep the answer concise. [/INST] </s>

                    [INST]
                        {type_input}
                        The response should be in JSON format with table and column :
                        {tables}
                    [/INST]

                    [INST] Question : {input}
                    Context: {context} 
                    Answer: [/INST]
                """
            )

    def return_list(self) -> str:
        return "<INST> Answer with Yes or No only.</INST>"
    
    
    def return_yes_or_no(self) -> str:
        return "<INST> Separate them by a comma. List as much as you can.</INST>"

