
import os
from table_generator.table_creator import TableCreator
from src.query import Query
from llm import Llm
from constants import *
from table_generator.llm_to_json import LlmToJson



class Main:
    def __init__(self):
        self.query = Query(SQL_REQUEST)

        self.tables_name_dict = {}
        self.tables_dict = {}

        self.llm = Llm()
        self.llm_to_json = LlmToJson()
        

    def extract_tables_names(self):
        for table in self.query.tables:
            split_table = table.split(".")
            if len(split_table) == 2:
                self.tables_name_dict[split_table[1]] = split_table[0]

        print(self.tables_name_dict)

    def extract_attributes(self):
        for attribute in self.query.attributes:

            split_attribute = attribute.split(".")
            if len(split_attribute) == 2:

                if split_attribute[0] in self.tables_name_dict:
                    table_name = self.tables_name_dict[split_attribute[0]]
                    if table_name in self.tables_dict:
                        self.tables_dict[table_name].append(split_attribute[1])
                    else:
                        self.tables_dict[table_name] = [split_attribute[1]]

        print(self.tables_dict)

    

    

    def test_create_table(self, tables_dict):
        table_creator = TableCreator("test.db")
        table_creator.create_tables(tables_dict)


        
    def create_prompt(self, table_dict):
        prompt = """Récupérer les éléments suivants pour chaque table en json : \n\n
        Exemple : 
                ```json
                {"[TABLE NAME]" :
                        {
                            "column_names" : ["[VALUE 1]", "[VALUE 2]", "[VALUE 3]"],
                            "data" : [
                                {"id": 1, "value": 100},
                                {"id": 2, "value": 150},
                                {"id": 3, "value": 200}
                            ]
                        },
                    "[TABLE NAME2]" : ...
                }``` :        
        \n"""
        for table, columns in table_dict.items():
            prompt += f"Table {table} :\n"
            for column in columns:
                prompt += f" - {column}\n"
        return prompt
    


    
    def run(self):
        self.extract_tables_names()
        self.extract_attributes()

        self.test_create_table(self.tables_dict)
        print("Table created successfully.")


        #  LLM
        prompt = self.create_prompt(self.tables_dict)
        print(f"Prompt : {prompt}")

        self.llm.get_chat_chain("uploads/paper.md")
        print("Chain created successfully.")

        answer = self.llm.ask(prompt)
        print(f"Answer : {answer}")

        tables_json = self.llm_to_json.convert_to_json(answer)
        print(tables_json)

        # tables_json = {'table1': {'column_names': ['id', 'value'], 'data': [{'id': 1, 'value': 100}, {'id': 2, 'value': 150}, {'id': 3, 'value': 200}]}, 'table2': {'column_names': ['description', 'id'], 'data': [{'description': 'Produit A', 'id': 1}, {'description': 'Produit B', 'id': 2}, {'description': 'Produit C', 'id': 3}]}}

        table_creator = TableCreator("test.db")
        table_creator.json_to_database(tables_json)

        print("Tables created successfully.")


    def test(self):
        table_creator = TableCreator("test.db")
        print(table_creator.query(SQL_REQUEST))



if __name__ == "__main__":
    main = Main()
    main.test()

