from src.query import Query
import pandas as pd


sql = "SELECT t1.id, t1.value, t2.description FROM table1.t1 JOIN table2.t2 ON t1.id = t2.id"

query = Query(sql)

df = pd.DataFrame(query.explain_query_as_dataframe())

print(df)

print("----")

for column in list(df.columns):
    print("\n")
    print(column)
    for l in df[column]:
        if l:
            print(l.split(","))

print("----")
print(df.shape)


print("----")
print(df.iloc[len(df)-1,len(df.columns)-1])