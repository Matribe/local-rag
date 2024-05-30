import csv
import traceback
from src.query import Query
from exceptions.queryExceptions import MultiTablesInQueryWithoutAlias

csv_file1 = 'data/Spider_Filtered_Data_generic.csv'
csv_file2 = 'data/Final_Queries.csv'

def test_sample(data_file: str, verbose_mode: int) -> str:
    with open(data_file, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        check_case = 0
        case = 0
        first_one = True
        no_alias_error_case = 0
        duckdb_error_case = 0
        weird_cases = []

        for row in csv_reader:
            if not first_one:
                if verbose_mode in (1, 3):
                    print("\n\n")
                
                row_usable = row[3].replace('"', "'")

                try:
                    query = Query(row_usable)
                    explanation = query.explain_query_as_dataframe()

                    if verbose_mode in (1, 3):
                        print("##################################################")
                        print(f"TEST nº{case} :")
                        print(row[3])
                        print("SUCCESS ##########################################")
                        print(explanation)
                        print("##################################################\n\n")

                    
                    check_case += 1
                
                except Exception as e:
                    if isinstance(e, MultiTablesInQueryWithoutAlias):
                        no_alias_error_case += 1
                    elif "duckdb" in traceback.format_exc():
                        duckdb_error_case += 1
                    else:
                        weird_cases.append(case)

                    if verbose_mode in (2, 3):
                        print("##################################################")
                        print(f"TEST nº{case} :")
                        print(row[3])
                        print("FAILURE ##########################################")
                        print(f"Type d'erreur : {type(e).__name__}\n")
                        print(f"Message d'erreur : \n{str(e)}\n")
                        print(f"Traceback : \n{traceback.format_exc()}")
                        print("##################################################\n\n")
            else:
                first_one = False
            case += 1

    case -= 1  # Enlever les en-têtes
    number_cases_to_except = no_alias_error_case + duckdb_error_case

    if verbose_mode in (1, 2, 3):
        print(f"\n\n\nTAUX DE RÉUSSITE FINAL FICHIER {data_file} : {check_case}/{case} soit {(check_case * 100) / case}%")
        print(f"- {no_alias_error_case} cas sont dus à une erreur du type {MultiTablesInQueryWithoutAlias.__name__}")
        print(f"- {duckdb_error_case} cas sont dus à une erreur de la librairie DuckDB")
        print(f"COMPTAGE SANS ERREURS CONNUES : {check_case}/{case - number_cases_to_except} soit {(check_case * 100) / (case - number_cases_to_except)}%")
        print(f"Cas anormaux  : {weird_cases}")

    return (
        f"\nTAUX DE RÉUSSITE FINAL FICHIER {data_file} : {check_case}/{case} soit {(check_case * 100) / case}%"
        f"\n- {no_alias_error_case} cas sont dus à une erreur du type {MultiTablesInQueryWithoutAlias.__name__}"
        f"\n- {duckdb_error_case} cas sont dus à une erreur de la librairie DuckDB"
        f"\nCOMPTAGE SANS ERREURS CONNUES : {check_case}/{case - number_cases_to_except} soit {(check_case * 100) / (case - number_cases_to_except)}%"
    )

# Test des fichiers CSV
result1 = test_sample(csv_file1, 3)
result2 = test_sample(csv_file2, 3)

# Affichage des résultats si non verbose mode
# print(result1)
# print(result2)