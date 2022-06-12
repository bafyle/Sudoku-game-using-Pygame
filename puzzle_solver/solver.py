
class Solver(object):
    def __init__(self, puzzle: list):
        self.puzzle = puzzle

    def is_valid(self, index: tuple, guess: int, puzzle: list[list[int]] = None) -> bool:
        """
        Return True if the guessed number is in the correct place and False otherwise.
        This function is used to compare the guessed number with its row, column
        and 3x3 square in the puzzle with empty cells
        """
        if puzzle:
            puzzle_to_check = puzzle
        else:
            puzzle_to_check = self.puzzle
        
        row, col = index
        if guess in puzzle_to_check[row]:
            return False
        
        if guess in [puzzle_to_check[i][col] for i in range(9)]:
            return False

        # sub-square checking 
        r = (row // 3) * 3
        c = (col // 3) * 3
        
        for i in range(r, r+3):
            for j in range(c, c+3):
                if puzzle_to_check[i][j] == guess:
                        return False

        return True
    
    @staticmethod
    def is_there_once(index: tuple, guess: int, puzzle: list[list[int]] = None) -> bool:
        """
        Return True if the guessed number is in its row, column or 3x3 square only once.
        """
        
        row, col = index
        for i, value in enumerate(puzzle[row]):
            if guess == value and i != col:
                return False
        
        
        this_column_values = [puzzle[i][col] for i in range(9)]
        for i, value in enumerate(this_column_values):
            if guess == value and i != row:
                return False
        
       
        r = (row // 3) * 3
        c = (col // 3) * 3
        
        found = False
        for i in range(r, r+3):
            for j in range(c, c+3):
                if puzzle[i][j] == guess:
                    if found:
                        return False
                    found = True
        return True

    def solve_in_place(self) -> bool:
        """
        This function is used to solve a sudoku puzzle using backtracking.
        Returns True if the puzzle is solved and False if the puzzle cannot be solved
        """
        empty_places = self._get_empty_cells(self.puzzle)
        length_of_empty_places = len(empty_places)

        if length_of_empty_places == 0:
            return False
        
        empty_place_index = 0
        while empty_place_index < length_of_empty_places:
            r, c = empty_places[empty_place_index]
            value = self.puzzle[r][c]
            while value < 9:
                value += 1
                if self.is_valid(empty_places[empty_place_index], value):
                    self.puzzle[r][c] = value
                    empty_place_index += 1
                    break
            else:
                value = 0
                self.puzzle[r][c] = value
                empty_place_index -= 1
                
            if empty_place_index <= -1:
                return False
        return True
    
    def _get_empty_cells(self, puzzle: list[list[int]]) -> list:
        """
        Return a list of the indices of the empty places in the puzzle
        """
        return [(i//9, i%9) for i in range(81) if puzzle[i//9][i%9] == 0]
