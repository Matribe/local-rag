from src.query import Query
from tabulate import tabulate

# STEP 1: Créer un objet Query avec juste sa formule SQL.
# ------------------------------------------------------------------------------------
# CAS 1: SQL avec une seule table -> OK.
# sql = "SELECT id, name, age FROM db WHERE age > 18"

# CAS 2: SQL avec plusieurs tables sans alias -> Erreur levée.
# sql = "SELECT id, name, age FROM db, ager WHERE age > 18"

# CAS 3: SQL avec plusieurs tables et des alias avec un point -> OK.
sql = "SELECT t1.id, t1.value, t2.description FROM table1.t1 JOIN table2.t2 ON t1.id = t2.id"

# CAS 4: SQL avec plusieurs tables et des alias avec AS -> OK.
# sql = "SELECT t1.id, t1.value, t2.description FROM table1 AS t1 JOIN table2 AS t2 ON t1.id = t2.id"

# STEP 2: Créer l'objet Query avec sa formule SQL en parametre.
# -------------------------------------------------------------------------------------------
query = Query(sql)

# Afficher l'explication de la requête
print("\n\nEXPLANATION:\n\n" + query.to_string() + "\n\n")

# STEP 3: Utiliser la fonction explain de Query pour obtenir le diagramme DuckDB de la requête.
# -------------------------------------------------------------------------------------------
print("DuckDB Query Plan:\n")
print(query.explain())

# ====================================================================OR=============================================================

# STEP 3 (Alternative): Utiliser la fonction explain_query_as_dataframe de Query pour obtenir un tableau d'instruction.
# -------------------------------------------------------------------------------------------
print("Instruction Table:\n")
print(tabulate(query.explain_query_as_dataframe(), headers='keys', tablefmt='pretty'))
