

from collections import Counter
from src.settings import *

class StringAnalyze:
    '''
        A class for generating and processing strings from different types of data structures.

        This class provides methods for converting dictionaries to formatted strings,
        extracting dictionaries from JSON-like strings, processing results into lists of tuples,
        and identifying the most frequent tuples in a list of responses.
    '''

    def tables_bulletpoints(self, tables_dict) -> str:
        string = ""
        for table, columns in tables_dict.items():
            string += f"{table} :\n"
            for column in columns:
                string += f" - {column}\n"
        return string
    
    def treat_results(self, results: str) -> list:
        final_list = []
        results = results.split("), (")
        for element in results:
            liste = element.replace("(", "").replace(")", "")
            liste = liste.replace("]", "").replace("[", "")
            liste = liste.replace("'", "")
            
            liste = liste.split(",")
            liste_analyzed = []
            for data in liste:
                data = data.lstrip()
                data = data.lower()
                data = self.convert_suffix_to_number(data)
                data = self.replace_units(data)
                data = self.try_cast_as_integer(data)
                liste_analyzed.append(data)
            final_list.append(tuple(liste_analyzed))
        return final_list

    def get_most_frequent_tuples(self, responses, threshold) -> float:
        tuple_counts = Counter(responses)
        frequent_tuples = [t for t, count in tuple_counts.items() if count >= threshold]
        return frequent_tuples
    
    def verif_size_columns(self, size, answer):
        answer_verified = []
        for data in answer:

            if len(data) == size:
                answer_verified.append(data)
            elif len(data) > 0 :
                current_data = self.modify_size_tuple(data, size)
                answer_verified.append(current_data)

        return answer_verified
    
    def modify_size_tuple(self, current_tuple: tuple, size: int) -> tuple:
        pass
        if len(current_tuple) > size:
            return self.minus_size_tuple(current_tuple, size, INITIAL_INDEX_TUPLE)
        
        return self.add_size_tuple(current_tuple, size)

    def add_size_tuple(self, current_tuple: tuple, size: int) -> tuple:
        tuple_length = len(current_tuple)
        tuple_as_list = []

        if tuple_length > size :
            return current_tuple

        for index in range(size):

            if index < tuple_length :
                tuple_as_list.append(current_tuple[index])
            else:
                tuple_as_list.append(None)
        
        augmented_tuple = tuple(tuple_as_list)
        return augmented_tuple

    def minus_size_tuple(self, current_tuple: tuple, size: int, begin_index=0) -> tuple:
        tuple_length = len(current_tuple)
        tuple_as_list = []

        if tuple_length < size or begin_index > size:
            return current_tuple

        for index in range(begin_index, size):
            tuple_as_list.append(current_tuple[index])
        
        decreased_tuple = tuple(tuple_as_list)
        return decreased_tuple

    def is_integer(self, string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False
    
    def try_cast_as_integer(self, string: str) -> int | str:
        try: 
            integer = int(string)
            return integer
        except:
            return string

    def type_of_attributs(self, tables, answer):
        table_with_type = {}
        for table, columns in tables.items():
            table_with_type[table] = {"column_names": columns}
            table_with_type[table]["type"] = ["TEXT" for _ in columns]
            if answer[table]["data"]:
                attributs = answer[table]["data"][0]
                for i in range(len(columns)):
                    attribut = attributs[i]
                    if self.is_integer(attribut):
                        table_with_type[table]["type"][i] = "INTEGER"
        return table_with_type
    
    def convert_suffix_to_number(self, string: str):
        data = string
        if not data:
            return ""
        if data[-1] in ['k', 'm', 'b'] and data[:-1].isdigit():
            number = int(data[:-1])
            suffix = data[-1]
            if suffix == 'k':
                return number * 1000
            elif suffix == 'm':
                return number * 1000000
            elif suffix == 'b':
                return number * 1000000000
        return string

    def replace_units(self, string: str) -> str:
        if not isinstance(string, int):
            data = string.replace('thousand','*10**3').replace('million','*10**6').replace('billion','*10**9').replace('trillion','*10**12')
            if self.is_integer(data[:-6]):
                return int(eval(data))
        return string