import unittest
from puzzle_solver.solver import Solver
import sqlite3 as sql

class PuzzleSolverTest(unittest.TestCase):

    def setUp(self) -> None:
        self.connector = sql.connect(r"./puzzles.db")
        self.cursor = self.connector.cursor()
    
    def test_puzzle_solver(self):

        solved_puzzles = list()
        puzzles_from_db = list()

        puzzles_query = self.cursor.execute("SELECT quiz from Quizzes;")
        for puzzle in puzzles_query:
            unsolved_puzzles = self._convert_puzzle_string_to_list(puzzle[0])
            solver = Solver(unsolved_puzzles)
            solver.solve_in_place()
            solved_puzzles.append(solver.puzzle)
        
        answers_query = self.cursor.execute("SELECT answer from Answers;")
        for puzzle in answers_query:
            puzzles_from_db.append(self._convert_puzzle_string_to_list(puzzle[0]))

        for index, puzzle in enumerate(solved_puzzles):
            for row_index in range(len(puzzle)):
                self.assertListEqual(puzzles_from_db[index][row_index], solved_puzzles[index][row_index])

        self.addCleanup(self.cleanUp)
    
    def cleanUp(self):
        self.connector.close()
    
    def _convert_puzzle_string_to_list(self, puzzle_text):
        new_puzzle = list()
        inner_list = list()
        for index, char in enumerate(puzzle_text):
            if index % 9 == 0 and index != 0:
                new_puzzle.append(inner_list)
                inner_list = list()
            inner_list.append(int(char))
        new_puzzle.append(inner_list)
        return new_puzzle

if __name__ == "__main__":
    unittest.main()