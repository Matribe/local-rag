from sql_metadata import Parser as parser

class SqlParser:
    
    def __init__(self, query: str) -> None:
        self.query = query

    def find_tables(self) -> list[str]:
        return parser(self.query).tables
    
    def find_attributes(self) -> list[str]:
        
        sql_formula = self.query
        columns = parser(sql_formula).columns

        if not columns and 'SELECT' in sql_formula:
            
            # double partition to get tables between SELECT [...] FROM
            _, _, formula_after_select = sql_formula.partition('SELECT ')
            formula_between_select_and_from, _, _ = formula_after_select.partition(' FROM')

            columns.append(formula_between_select_and_from)

        return columns
