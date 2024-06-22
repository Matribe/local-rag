
from src.settings import INITIAL_INDEX_TUPLE


class TupleManage:
    """
        A class to manage and modify tuples to fit a specified size.

        Methods
        -------
        verif_size_columns(size: int, answer) -> list
            Verifies and adjusts the size of tuples in the provided list to match the specified size.
            
        modify_size_tuple(current_tuple: tuple, size: int) -> tuple
            Modifies the size of a given tuple to match the specified size, either by truncating or augmenting it.
            
        add_size_tuple(current_tuple: tuple, size: int) -> tuple
            Augments the size of a given tuple to match the specified size by adding None elements.
            
        minus_size_tuple(current_tuple: tuple, size: int, begin_index=0) -> tuple
            Reduces the size of a given tuple to match the specified size starting from a specified index.
    """



    def verif_size_columns(self, size: int, answer):
        answer_verified = []
        for data in answer:

            if len(data) == size:
                answer_verified.append(data)
            elif len(data) > 0 :
                current_data = self.modify_size_tuple(data, size)
                answer_verified.append(current_data)

        return answer_verified

    
    def modify_size_tuple(self, current_tuple: tuple, size: int) -> tuple:
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