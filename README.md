# Sudoku Using Pygame


## Content:
* [General Info](#general-info)
* [Technologies](#technologies)
* [Running the game](#running-the-game)
* [Solving algorithm](#solving-algorithm)
* [Puzzles](#puzzles)

## General Info
Simple Sudoku game created with Python and Pygame

The game comes with 100 puzzle (not used yet)

Thanks for https://www.kaggle.com/bryanpark/sudoku for providing a 1 million puzzle dataset with answers, i just used the first 100.

## Technologies:
- Python                3.7.2
- Pygame                2.0.0
- Pandas                1.1.5 (not required to run the game)
- SQLite3               3.32.2 (not required to run the game)
- DB Browser for SQLite 3.12 (not required to run the game)

## Running the game
To run the game you need to install Pygame using pip:
~~~
pip install pygame
~~~
After the installation is complete you can run the game from:
~~~
python sudoku.py
~~~

## Solving algorithm:
i used backtracking algorithm to solve the puzzle

you can find the code in puzzleSolver.py file

## Puzzles
The dataset is a .csv file. I used pandas library to get the puzzles and sqlite3 connector to store the puzzles into the database

You can run the code for yourself by:
- installing pandas:
~~~
pip install pandas
~~~
- And numpy
~~~
pip install numpy
~~~
- Download the dataset from this link: https://www.kaggle.com/bryanpark/sudoku and extract the zip file (about 162MB)

- Create a database file from DB Browser For SQLite and name it 'puzzels.db' or any name you like, just don't forget to rename it in the Python code

- Change the number of puzzles that you want to store from the dataset and run the getPuzzles.py file and you good to go

