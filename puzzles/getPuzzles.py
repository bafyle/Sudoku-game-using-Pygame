import pandas as pd
import numpy as np
import sqlite3 as sql


connection = sql.connect("puzzles.db")
cur = connection.cursor()

data = pd.read_csv("sudoku.csv") # reading the csv file
puzzlesNumber = 100 # we want to get 100 puzzle
for i in range(puzzlesNumber):
    """
    the column name of the puzzle is 'quizzes' and we want the i-th row
    from the dataset to be inserted to the Quizzes table.
    The same thing for the solutions but i inserted the row number as a
    foreign key to the Answers table.
    """
    cur.execute("INSERT INTO Quizzes(quiz) VALUES(?);", [data["quizzes"][i]])
    cur.execute("INSERT INTO Answers VALUES(?, ?);", [i+1, data["solutions"][i]])
 
connection.commit() # commiting the changes 
connection.close() # closing the database
data.close() # and closing the file
