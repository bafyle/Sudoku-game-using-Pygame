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
(keep in mind that the game is semi-working, i am still working on it while learning)

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

tests.py file is for testing the algorithm and comparing the solution that is generated from the algorithm against the provided solution from the dataset.

## Puzzles:
All puzzles are stored in puzzles.db file which is a SQLite database.

I used pandas to read the CSV file and extract the puzzles and solutions from it.

- Installing pandas:
~~~
$ pip3 install pandas
~~~
- Download the dataset (about 162MB) in puzzles folder using this link: https://www.kaggle.com/bryanpark/sudoku and extract the zip file  in puzzles folder.

- Move or rename puzzles.db which is located in the root directory of the repo. don't delete the database.

- Open create_database.py which is located in database directory and change 'puzzles_number' to anything you want. This variable indicates how many puzzles the database will store
~~~
import pandas as pd
import sqlite3 as sql

puzzles_number = 100
...
~~~

- Run the script and wait 2 seconds (I have HDD, not SSD), and you should see a new database file created.

- If you want to use your own dataset, you have to change more than just the number of the puzzle in the script file in order to extract the puzzles and the solution from it


All puzzles must be in string format and the missing numbers are zeros. Example:
~~~
004300209005009001070060043006002087190007400050083000600000105003508690042910300
~~~

## Game images:
![alt screenshot 1](./docs/images/1.PNG)
![alt screenshot 2](./docs/images/2.PNG)