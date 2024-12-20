import sqlite3

connection = sqlite3.connect('capstone.db')
cursor = connection.cursor()

def create_schema(cursor):
    with open('capstone.txt', 'r') as readfile:
        cr_queries = readfile.read()
    
    cursor.executescript(cr_queries);


result = create_schema(cursor)