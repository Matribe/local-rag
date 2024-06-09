'''
    Externals importations.
'''
from enum import Enum

class Boxcomponent(Enum):
    '''
        ENUM:
            "This class contains only constants that represent all the 
            components of a DuckDB query plan diagram."
    '''
    SIMPLE_TOP = "┌───────────────────────────┐"
    SIMPLE_BOTTOM = "└───────────────────────────┘"
    LINKED_TOP = "┌─────────────┴─────────────┐"
    LINKED_BOTTOM = "└─────────────┬─────────────┘"
    SEPARATOR = "│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │"
    RIGHT_LINK = "├──────────────┐"
    SPACER = "                             "
    SPACER_FULL = '│                           │'
    SPACER_LEFT = "│                           "
    SPACER_RIGHT = "                           │"
    BETWEEN_BOX = "││"

    def __str__(self):
        '''
            Method returning the str value when a constant is chosen.
        '''
        return str(self.value)