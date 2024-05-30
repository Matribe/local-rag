class RelationScheme:
    ''' 
        OBJECT:
            The RelationScheme class is an object containing
            a name and an attribute list.
    '''

    name = ''
    attributes = [] 
      
    def __init__(self, name:str, attributes:list) -> None:
        '''
            Constructor of relation_scheme object with:
                - name:str is the relation scheme name.
                - attributes:list is a list of attributes (str).

        '''
        self.name = name
        self.attributes = attributes

    def to_string(self) -> str:
        '''
            Method returning a String with all the RelationScheme's values.
        '''
        return  f'\tname : {self.name} \n\tattributes : {str(self.attributes)}'
