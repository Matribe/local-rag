'''
    Externals importations.
'''
import pandas as pd
'''
    Internals importations.
'''
from src.enumBoxComponent import Boxcomponent
from src.planText import PlanText
from settings import ELEMENT_TO_REPLACE

class DiagramHandler:
    '''
        TOOL:
            This class contains methods to handled the diagram produced by DuckDB 
            with its explain function.
    '''
    def clean_rows(self, all_rows:list) -> list:
        '''
            Performs final processing on each row of cell contents.
            This method iterates through all rows and cells, formatting non-empty cells.
            It converts rows to a specific format and cleans the cell content.
        '''
        row_index = 0
        cell_index = 0
        old_cell = ""
        while row_index < len(all_rows):
            cell_index = 0
            while cell_index < len(all_rows[row_index]):
                if(len(all_rows[row_index][cell_index]) == 0 and cell_index != 0):
                    all_rows[row_index][cell_index] = ','
                else:
                    if(old_cell != ',' and cell_index != 0):
                        all_rows[row_index][cell_index] = ","+all_rows[row_index][cell_index]
                old_cell = all_rows[row_index][cell_index]
                cell_index += 1
            all_rows[row_index] = self.row_to_none("".join(all_rows[row_index]))
            all_rows[row_index] = self.clean_cells(all_rows[row_index])
            row_index += 1
            old_cell = ""
        return all_rows

    def clean_cells(self, cell_content:str) -> str:
        '''
            Cleans and processes the content of a cell.
            This method splits the cell content by commas, removes empty elements, 
            and joins elements based on specific conditions. 
        '''
        if(cell_content != None):
            cell_content = cell_content.split(",")
            cell_index = 0
            while cell_index<len(cell_content):
                if(len(cell_content[cell_index]) == 0):
                    cell_content.pop(cell_index)
                    cell_index-=1
                if("(" in cell_content[cell_index]):
                    old_len = len(cell_content)
                    cell_content = self.cell_join_on_condition(cell_content, cell_index)
                    cell_index = cell_index+1 if old_len>len(cell_content) else cell_index
                cell_index +=1
            cell_content = ",".join(cell_content)
        return cell_content
           
    def clean_row_format(self, row:str) -> str:
        '''
            Removes specific format elements from the given row.
        '''
        for element in ELEMENT_TO_REPLACE:
            row = row.replace(element, "")
        return row

    def cell_join_on_condition(self, cell_content_list:list, cell_index) -> str:
        '''
            Joins cell elements based on specific conditions.
            This method checks if the next cell in the list contains a closing parenthesis. 
            If so, it concatenates the current cell with the next cell 
            and removes the next cell from the list.
        '''
        if(cell_index<len(cell_content_list)-1):
            if(")" in cell_content_list[cell_index+1]):
                cell_content_list[cell_index] += cell_content_list[cell_index+1]
                cell_content_list.pop(cell_index+1)
        return cell_content_list

    def get_cells_content(self, plan_text:PlanText) -> list:
        '''
            Retrieves the content of all cells in the plan text.
            This method iterates through the rows of the plan text.
            The contents of each row are added to a list, which is then returned.
        '''
        plan_text.next_row()
        all_rows = []
        while not(self.check_end_cell(plan_text.current_row)):
            row_content = self.process_multiple_cells_stage(plan_text.current_row)
            all_rows.append(row_content)
            plan_text.next_row()
        return all_rows

    def check_end_cell(self, row:str) ->  bool:
        '''
            Checks if the given row is an end cell.
        '''
        if(str(Boxcomponent.SIMPLE_BOTTOM) in row):
            return True
        if(str(Boxcomponent.LINKED_BOTTOM) in row):
            return True
        return False

    def process_cells_stage(self, plan_text:PlanText, instruction_table:pd.DataFrame) -> None:
        '''
            Processes the cells content of a plan for one stage,
            adjusts the instruction table, and adds rows to the instruction table.
        '''
        all_rows = self.get_cells_content(plan_text)
        all_rows = [list(item) for item in zip(*all_rows)]
        plan_text.set_instruction_table_max_len(len(all_rows))
        if(len(all_rows)<plan_text.instruction_table_len):
            for null_to_append in range (0, plan_text.instruction_table_len-len(all_rows)) : all_rows.append([])
        all_rows = self.clean_rows(all_rows)
        self.increase_size_instruction_table(plan_text,plan_text.branch_index,len(all_rows),instruction_table)
        self.add_row_in_instruction_table(all_rows, plan_text, instruction_table)
  
    def process_multiple_cells_stage(self, row_content:str) -> list:
        '''
            Processes the content of a row with multiple cells.
            This method splits the row into individual cells, and then cleans the format of each cell.
        '''
        row_content = row_content.replace(str(Boxcomponent.SPACER), str(Boxcomponent.SPACER_FULL))
        row_content = row_content.split(str(Boxcomponent.BETWEEN_BOX))
        index_cell = 0
        while index_cell < len(row_content):
            row_content[index_cell] = self.clean_row_format(row_content[index_cell])
            index_cell+=1
        return row_content
    
    def row_to_none(self, row:str) -> str:
        '''
            Converts a row to None if it contains only commas.
        '''
        for char in row:
            if(char != ','):
                return row
        return None
      
    def add_row_in_instruction_table(self, all_rows:list, plan_text:PlanText, instruction_table:pd.DataFrame) -> None:
        '''
            Adds a processed row to the instruction table.This method constructs a dictionary from the processed 
            rows, where each key represents a branch column.
            It then adds this dictionary as a new row in the instruction table.
        '''
        column_index = 0
        row_to_add = {}
        while column_index < instruction_table.shape[1]:
            row_to_add[f"branch{column_index+1}"] = all_rows[column_index]
            column_index+=1
        instruction_table.loc[plan_text.step_index] = row_to_add
        plan_text.next_step()

    def increase_size_instruction_table(self, plan_text:PlanText, old_len:int, new_len:int, instruction_table:pd.DataFrame) -> None:
         '''
            Increases the size of the instruction table by adding new branch columns.
        '''
         if(old_len-1 < new_len):
            while plan_text.branch_index <= (new_len-old_len)+1:
                instruction_table[f"branch{plan_text.branch_index}"] = []
                plan_text.next_branch()