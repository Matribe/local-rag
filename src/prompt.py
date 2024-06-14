from langchain.prompts import PromptTemplate
from src.utils.string import StringGenerator
from src.utils.exemples import *


class PromptManage:
    def __init__(self, type_return = None):

        if not type_return:
            self.answer_prompt = PromptTemplate.from_template(
                """
                    <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
                    to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
                    maximum and keep the answer concise. [/INST] </s>
                    
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
                    
                    [INST] Retrieve the items in the following format :
                        {type_return} 
                    [/INST] 

                    [INST] Question: {input}
                    Context: {context} 
                    Answer: [/INST]
                """
            )

        self.string_generator = StringGenerator()


    def extract_data_from_text(self, tables_dict):
        tables = self.string_generator.tables_bulletpoints(tables_dict)

        prompt = f"""
                        Récupérer les éléments suivants pour chaque table en json : \n\n
                        Exemple : {EXEMPLE1}  \n   {tables}   \n
                """
        return prompt    




    def return_list(self) -> str:
        return "<INST> Answer with Yes or No only.</INST>"
    
    
    def return_yes_or_no(self) -> str:
        return "<INST> Separate them by a comma. List as much as you can.</INST>"

