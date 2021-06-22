import sqlite3

conn = sqlite3.connect("users.sqlite")

cursor = conn.cursor()
sql_query = """CREATE TABLE users (
    id text PRIMARY KEY,
    username text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    uuid text NOT NULL,
    publickey text NOT NULL
)"""
cursor.execute(sql_query)