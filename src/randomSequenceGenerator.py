'''
    Externals importations.
'''
import random
import string
'''
    Internals importations.
'''
from src.constants import RANDOM_SEQUENCE_LENGTH

class RandomSequenceGenerator:
    ''' 
        TOOL:
            This class contains the tools to produce a random sequence with a specified length
            and one of a predetermined length.
    '''
    def genererate_sequence(self, length:int) -> str:
        '''
            Method returning a random sequence of numbers and ascii caracters.
            This random sequence has the specified length.
        '''
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate(self) -> str:
        '''
            Method returning a random sequence of predetermined length.
        '''
        return self.genererate_sequence(RANDOM_SEQUENCE_LENGTH)