import sqlite3
import pandas as pd
from sqlalchemy import create_engine

file1 = "database/Book.csv"
file2 = "database/Author.csv"
file3 = "database/User.csv"
file4 = "database/Rating.csv"
file5 = "database/ListBook.csv"
file6 = "database/List.csv"

engine = create_engine(f'sqlite:///bookworms_db.sqlite', echo=False)
df1 = pd.read_csv(file1)
# print(df1)

df2 = pd.read_csv(file2)
# print(df2)

df3 = pd.read_csv(file3)
# print(df3)

df4 = pd.read_csv(file4)
# print(df4)

df5 = pd.read_csv(file5)
# print(df5)

df6 = pd.read_csv(file6)
# print(df6)

df1.to_sql('Book', engine, if_exists="replace", index=False)
df2.to_sql('Author', engine, if_exists='replace', index=False)
df3.to_sql('User', engine, if_exists='replace', index=False)
df4.to_sql('Rating', engine, if_exists="replace", index=False)
df5.to_sql('ListBook', engine, if_exists='replace', index=False)
df6.to_sql('List', engine, if_exists='replace', index=False)