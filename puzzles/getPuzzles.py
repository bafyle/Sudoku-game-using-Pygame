import pandas as pd
import sqlite3 as sql

puzzles_number = 100 # we want to get first 100 puzzle

# connect to the database
connection = sql.connect("puzzles.db")
cur = connection.cursor()

# create the database schema
with open("Table Creation.sql", 'r') as f:
    cur.executescript(f.read())

data = pd.read_csv("./sudoku.csv") # reading the csv file

for i in range(puzzles_number):
    """
    Inserting first 100 puzzles to the database, since the primary key is auto-incremented
    we don't need to specify the primary key value

    In inserting the solution of the quizzes we need to insert the foreign key of that solution
    and since i is a zero-based index, we have to add 1 to I before inserting it the database
    """
    cur.execute("INSERT INTO Quizzes(quiz) VALUES(?);", [data["quizzes"][i]])
    cur.execute("INSERT INTO Answers VALUES(?, ?);", [i+1, data["solutions"][i]])
 
connection.commit() # commiting the changes 
connection.close() # closing the database
