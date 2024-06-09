from langchain.prompts import PromptTemplate
from src.utils.string import StringGenerator
from src.utils.exemples import *


class PromptManage:
    def __init__(self):
        self.answer_prompt = PromptTemplate.from_template(
            """
                <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
                to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
                maximum and keep the answer concise. [/INST] </s> 
                [INST] Question: {question} 
                Context: {context} 
                Answer: [/INST]
            """
        )
        
        self.condense_question_prompt = PromptTemplate.from_template(
            """
                <s> [INST] Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question. [/INST] </s>

                [INST] Chat History:
                {chat_history}

                Follow Up Input: {question}
                Standalone question: [/INST]
            """
        )

        self.document_prompt = PromptTemplate.from_template(
            template="Source Document: {source}, Page {page}:\n{page_content}"
        )

        self.string_generator = StringGenerator()


    def messages_to_prompt(self, messages) -> str:
        """
            Convert a list of message dictionaries to a formatted prompt string.

            Args:
                messages (list of dict): List of messages where each message is a dictionary with 'role' and 'content'.

            Returns:
                str: Formatted prompt string.
        """
        
        prompt = "<s>"
        for message in messages:
            role = message.get('role', '').lower()
            content = (message.get('content') or "").strip()
            if role == "system":
                prompt += f"[INST] {content} [/INST]"
            elif role == "user":
                prompt += f"</s>\n [INST] {content} [/INST]"
        return prompt
    

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

