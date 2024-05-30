'''
    Externals importations.
'''
import pandas as pd
'''
    Internals importations.
'''
from src.planText import PlanText
from src.diagramHandler import DiagramHandler
from src.dbHandler import DbHandler

class SqlExplainer:
    '''
        TOOL:
            This class contains tools for explain sql queries.
            It can be used to find the query plan as a str diagram from a sql formula
            and its relation scheme.
            It can provide this query plan as a pandas dataframe.
    '''
    def explain(self, sql_formula:str, relation_schemes:list) -> str:
        '''
            Method returning a diagram as a String from a sql_formula and a RelationScheme list.
            This diagram is obtained via the duckDB librairy and
            explain the sql query as a query plan.
        '''
        return DbHandler().explain_with_duckdb(sql_formula, relation_schemes)
    
    def sql_plan_to_table(self, sql_formula:str, relation_schemes:list) -> pd.DataFrame:
        '''
            Method returning a DataFrame 
            from a sql_formula and a RelationScheme list. It uses the duckDB diagram suppliyed
            by the SqlExplainer.explain() method.
        '''
        plan = self.explain(sql_formula, relation_schemes)
        plan_text = PlanText('current_plan', plan)
        instruction_table = pd.DataFrame()
        diagram_handler = DiagramHandler()
        while plan_text.row_index < plan_text.number_rows-1:
            diagram_handler.process_cells_stage(plan_text, instruction_table)
            if(plan_text.row_index < plan_text.number_rows-1):                                       
                plan_text.next_row()
        return instruction_table      
        

        