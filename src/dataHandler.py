'''
    Externals importations.
'''
import json
'''
    Internals importations.
'''
from src.constants import *

class DataHandler:
    '''
    A handler for extracting SQL operators from a JSON file as a dictionary or a list.
    '''
    def get_operators_as_dict(self) -> dict:
        '''
            Extracts all the content of sql_operators.json as a dictionnary.
        '''
        with open(SQL_OPERATORS_FILE_PATH, 'r') as json_file:
            return json.load(json_file)
        
    def get_operators_as_list(self) -> list[str]:
        '''
            Extracts all the content of sql_operators.json as a list.
        '''
        selected_value = []
        for element in self.get_operators_as_dict().values():
            selected_value += element
        return selected_value
