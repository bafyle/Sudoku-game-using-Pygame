# Sudoku Using Pygame
Simple Sudoku game and solver created with Python and Pygame library.

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
I used iterative backtracking algorithm to solve the puzzle.
You can see the algorithm itself in the puzzleSolver for more details.

## Puzzles:
All puzzles are stored in puzzles.db file which is a SQLite database.

You can change the puzzles or try to insert the puzzles from the dataset to the database by:

- installing pandas:
~~~
$ pip3 install pandas
~~~
- Download the dataset from this link: https://www.kaggle.com/bryanpark/sudoku and extract the zip file (about 162MB)

- Create an empty database file from DB Browser For SQLite using the 'Table Creation.sql' file (located in puzzles folder) and name it 'puzzels.db'.

- Change the number of puzzles that you want to store from the dataset:
~~~
puzzlesNumber = 100 # number of puzzles
~~~
- run the 'getPuzzles.py' file

You can use any dataset, but you have to make sure that all puzzles are in string format and the missing numbers are zeros. Example:
~~~
004300209005009001070060043006002087190007400050083000600000105003508690042910300
~~~