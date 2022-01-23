import unittest
from puzzle_solver.solver import Solver
import sqlite3 as sql

class PuzzleSolverTest(unittest.TestCase):
    def test_puzzle_solver(self):

        connector = sql.connect(r"./puzzles.db")
        cursor = connector.cursor()

        puzzles_query = cursor.execute("SELECT quiz from Quizzes;")
        solved_puzzles = list()
        puzzles_from_db = list()

        for puzzle in puzzles_query:
            unsolved_puzzles = self._convert_puzzle_string_to_list(puzzle[0])
            solver = Solver(unsolved_puzzles)
            solved_puzzle, _ = solver.solve_out_place()
            solved_puzzles.append(solved_puzzle)
        
        answers_query = cursor.execute("SELECT answer from Answers;")
        for puzzle in answers_query:
            puzzles_from_db.append(self._convert_puzzle_string_to_list(puzzle[0]))
        
        connector.close()
        self.assertEqual(puzzles_from_db, solved_puzzles)

        
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