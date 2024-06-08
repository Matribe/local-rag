class PlanText:
    '''
        OBJECT:
            This objet is used to keep all the parameters
            of a text file containing a diagram which explains 
            a sql query.
    '''
    file_name:str
    content:str
    content_list:list
    number_rows:int
    row_index:int
    branch_index:int
    step_index:int
    current_row:str
    instruction_table_len:int

    def __init__(self, file_name:str, plan:str) -> None:
        '''
            Constructor of an PlanText objet.
            The attributes are :
                - file_name:str the name of the txt file.
                - content:str the txt file content.
                - row_index:int the current row index.
                - branch_index:int the branch index used in the DataFrame
                               as the columns index.
                _ step_index:int the step index used in the DataFrame
                                 as the row index.
                - current_row:str is the content of the current row
                                  in a str format.
                - instruction_table_len:int is the max len of the DataFrame
                                            produced to traduct the diagram
                                            (dynamically allocated).
        '''
        self.file_name = file_name
        self.content = plan
        self.row_index = 0
        self.branch_index = 1
        self.step_index = 1
        self.write_plan_file()
        self.to_list()
        self.number_rows = len(self.content_list)
        self.current_row = self.content_list[0]
        self.instruction_table_len = 0

    def set_instruction_table_max_len(self, len:int) -> None:
        '''
            Method changing the instruction_table_len:int attribute if
            the specified len is greater than the old one.
        '''
        if(len > self.instruction_table_len):
            self.instruction_table_len = len

    def next_row(self) -> None:
        '''
            Method incrementing the row_index:int attribute and 
            switching the content of the current_row to the next one.
        '''
        self.row_index+=1
        self.current_row = self.content_list[self.row_index]

    def next_branch(self) -> None:
        '''
            Method incrementing the branch_index:int attribute.
        '''
        self.branch_index+=1

    def next_step(self) -> None:
        '''
            Method incrementing the step_index:int attribute.
        '''
        self.step_index+=1

    def write_plan_file(self) -> None:
        '''
            Method opening a txt file as the specified file_name:str 
            to save the content:str.
        '''
        with open(f"data/{self.file_name}", 'w', encoding='utf-8') as file:
            file.write(self.content)

    def to_list(self) -> list:
        ''' 
            Method returning a list of rows from the specified file_name:str txt file.
        '''
        with open(f"data/{self.file_name}", 'r', encoding='utf-8') as file:
            rows = file.readlines()
        self.content_list = rows
