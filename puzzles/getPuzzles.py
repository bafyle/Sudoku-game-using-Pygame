import pandas as pd
import numpy as np
import sqlite3 as sql


connection = sql.connect("puzzles.db")
cur = connection.cursor()

data = pd.read_csv("sudoku.csv")
count = 100
for i in range(count):
    cur.execute("INSERT INTO Quizzes(quiz) VALUES(?);", [data["quizzes"][i]])
    cur.execute("INSERT INTO Answers VALUES(?, ?);", [i+1, data["solutions"][i]])
    connection.commit()

connection.close()
