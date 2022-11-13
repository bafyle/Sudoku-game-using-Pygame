import pandas as pd
import sqlite3 as sql
from pathlib import Path
import os

DB_PATH = r"./puzzles.db"
puzzles_db_path = Path(DB_PATH)
if puzzles_db_path.exists():
    os.remove(DB_PATH)

puzzles_number = 1000 # first 100 puzzle

connection = sql.connect(DB_PATH)
"""
The database location is relative to the parent directory, not to this directory.
"""
cur = connection.cursor()

# create the database schema
with open(r"database/Database Schema.sql", 'r') as f:
    cur.executescript(f.read())

data = pd.read_csv("database/sudoku.csv") # relative location to parent dir

quizzes_params = [(quiz, ) for quiz in data["quizzes"].values[:puzzles_number]]
answers_params = [(index+1, answer, ) for index, answer in enumerate(data["solutions"].values[:puzzles_number])]

cur.executemany("INSERT INTO Quizzes(quiz) VALUES(?);", quizzes_params)
cur.executemany("INSERT INTO Answers VALUES(?, ?);", answers_params)
 
connection.commit() # commit changes
connection.close()
