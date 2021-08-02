# Sudoku Using Pygame
Simple Sudoku game and solver created with Python and Pygame library.

## Content:
* [General Info](#general-info)
* [Technologies](#technologies)
* [Running the game](#running-the-game)
* [Solving algorithm](#solving-algorithm)
* [Puzzles](#puzzles)
* [Game images](#game-images)

## General Info:
Old Sudoku game

9x9 Board with missing numbers and you have to figure out what these numbers are, no number appears twice in row, column or 3x3 subregions of the board

The game has 100 puzzle to play with and solving algorithm using backtracking 
(keep in mind that the game is semi-working, iam still working on it while learning)

Thanks for https://www.kaggle.com/bryanpark/sudoku for providing a 1 million puzzle dataset with answers, i just used the first 100.

## Technologies:
To run the game you need:
- Python                    3.6+
- Pygame                    2.0.0

Go to [Running the game](#running-the-game) section to run the game

Other libraries for creating your own database 
- Pandas                    1.1.5

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

You can change the puzzles or try to insert new puzzles from a dataset by:

- Installing pandas:
~~~
$ pip3 install pandas
~~~
- Download your dataset in puzzles folder OR
use this link: https://www.kaggle.com/bryanpark/sudoku and extract the zip file (about 162MB) in puzzles folder

- Move puzzles.db file from puzzles directory (deleting the file is not recommended because if something wrong happened, the game will not run)

- Open getPuzzles.py and change 'puzzleNumber' variable if you want
~~~
import pandas as pd
import sqlite3 as sql

puzzlesNumber = 100
...
~~~

- If you used your own dataset, you have to change the body of the loop or the entire script to suite your data

- If not then, run 'getPuzzles.py' file and wait couple seconds and you should see a new database file

All puzzles must be in string format and the missing numbers are zeros. Example:
~~~
004300209005009001070060043006002087190007400050083000600000105003508690042910300
~~~

## Game images:
![alt screenshot 1](./docs/images/1.PNG)
![alt screenshot 2](./docs/images/2.PNG)