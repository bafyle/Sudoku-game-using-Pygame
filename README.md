# Sudoku Using Pygame
Simple Sudoku game and solver created with Python and Pygame

## Content:
* [General Info](#general-info)
* [Technologies](#technologies)
* [Running the game](#running-the-game)
* [Solving algorithm](#solving-algorithm)
* [Puzzles](#puzzles)

## General Info:
Old Sudoku game

9x9 Board with missing numbers and you have to figure out what these numbers are, no number appears twice in row, column or 3x3 subregions of the board

The game has 100 puzzle to play with and solving algorithm using backtracking 
(keep in mind that the game is semi-working, iam still working on it while learning)

Thanks for https://www.kaggle.com/bryanpark/sudoku for providing a 1 million puzzle dataset with answers, i just used the first 100.

## Technologies:
Technologies that were used to create the game and works just fine with them:
- Python                    3.7.9
- Pygame                    2.0.0
- Pandas                    1.1.5 (not required to run the game)
- SQLite3 DB-API Interface  (already installed in Python)
- DB Browser for SQLite     3.12 (not required to run the game)

## Running the game:
To run the game you need to install Pygame library using pip:
~~~
$ pip3 install pygame
~~~
After the installation is complete, go to the game folder and run the game from this command:
~~~
$ python3 sudoku.py
~~~

## Solving algorithm:
I used backtracking algorithm to solve the puzzle

You can find the code in puzzleSolver.py file

## Puzzles:
All puzzles are stored in a .csv file. I used pandas library to get top 100 puzzle and sqlite3 connector to insert these puzzles into the database


You can run the code for yourself by:
- installing pandas:
~~~
$ pip3 install pandas
~~~
- And numpy
~~~
$ pip3 install numpy
~~~
- Download the dataset from this link: https://www.kaggle.com/bryanpark/sudoku and extract the zip file (about 162MB)

- Create an empty database from DB Browser For SQLite using the 'Table Creation.sql' file and name it 'puzzels.db' or any name you like, just don't forget to rename it in the Python code.

- Change the number of puzzles that you want to store from the dataset 
~~~
puzzlesNumber = 100 # number of puzzles
~~~
and run the getPuzzles.py file

- You can use any dataset you want. To make sure everything works correctly, the dataset must have the puzzles in a string format and the empty cells in the puzzle must be zero.

