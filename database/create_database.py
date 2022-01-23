import pandas as pd
import sqlite3 as sql

puzzles_number = 100 # first 100 puzzle

# create a database or connect to existing one
connection = sql.connect("../puzzles.db")
cur = connection.cursor()

# create the database schema
with open("Table Creation.sql", 'r') as f:
    cur.executescript(f.read())

data = pd.read_csv("./sudoku.csv")

for i in range(puzzles_number):
    """
    Inserting first 100 puzzles into the database, since the primary key is auto-incremented,
    There is no need to specify it
    """
    cur.execute("INSERT INTO Quizzes(quiz) VALUES(?);", [data["quizzes"][i]])
    cur.execute("INSERT INTO Answers VALUES(?, ?);", [i+1, data["solutions"][i]])
 
connection.commit() # commit changes
connection.close()
