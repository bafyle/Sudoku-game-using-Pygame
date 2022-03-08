
class Solver(object):
    def __init__(self, puzzle: list):
        self.puzzle = puzzle

    def is_valid(self, index: tuple, guess: int, puzzle: list[list[int]] = None) -> bool:
        """
        Return True if the guessed number is in a correct place and False otherwise.
        This function is used to compare the guess number with its row, column
        and 3x3 square in the puzzle with empty cells
        """
        if puzzle:
            check_puzzle = puzzle
        else:
            check_puzzle = self.puzzle
        
        row, col = index
        if guess in check_puzzle[row]:
            return False
        
        if guess in [check_puzzle[i][col] for i in range(9)]:
            return False

        # sub-square checking 
        r = (row // 3) * 3
        c = (col // 3) * 3
        
        for i in range(r, r+3):
            for j in range(c, c+3):
                if check_puzzle[i][j] == guess:
                        return False

        return True
    
    def is_there_once(self, index: tuple, guess: int, puzzle: list[list[int]] = None) -> bool:
        """
        Return True if the guessed number is its row, column or 3x3 square only once.
        """
        if puzzle:
            check_puzzle = puzzle
        else:
            check_puzzle = self.puzzle
        row, col = index
        for i, value in enumerate(check_puzzle[row]):
            if guess == value and i != col:
                return False
        
        
        this_column_values = [check_puzzle[i][col] for i in range(9)]
        for i, value in enumerate(this_column_values):
            if guess == value and i != row:
                return False
        
       
        r = (row // 3) * 3
        c = (col // 3) * 3
        
        found = False
        for i in range(r, r+3):
            for j in range(c, c+3):
                if check_puzzle[i][j] == guess:
                    if found:
                        return False
                    found = True
        return True

    def solve_in_place(self) -> bool:
        """
        This function is used to solve a sudoku puzzle using backtracking.
        """
        empty_places = self._get_empty_cells()
        length_of_empty_places = len(empty_places)

        if length_of_empty_places == 0:
            return False
        
        current_index = 0
        
        while True:
            r, c = empty_places[current_index]
            value = self.puzzle[r][c]
            while True:
                if value == 0:
                    value = 1
                elif value < 9:
                    value += 1
                else:
                    value = 0
                    self.puzzle[r][c] = value
                    current_index -= 1
                    break

                if self.is_valid(empty_places[current_index], value):
                    self.puzzle[r][c] = value
                    current_index += 1
                    break

            if current_index >= length_of_empty_places:
                return True

            if current_index <= -1:
                return False
    

    def solve_out_place(self) -> tuple:
        """
        This function is used to solve a sudoku puzzle using backtracking.
        It returns a tuple with the puzzle and boolean value indicating if the puzzle is solved or not
        """
        from copy import deepcopy
        empty_places = self._get_empty_cells()
        empty_places_len = len(empty_places)
        new_puzzle = deepcopy(self.puzzle)

        if empty_places_len == 0:
            return new_puzzle, False
        current_index = 0
        while True:
            r, c = empty_places[current_index]
            value = new_puzzle[r][c]
            while True:
                if value == 0:
                    value = 1
                
                elif value < 9:
                    value += 1
                else:
                    value = 0
                    new_puzzle[r][c] = value
                    current_index -= 1
                    break

                if self.is_valid(empty_places[current_index], value, new_puzzle):
                    new_puzzle[r][c] = value
                    current_index += 1
                    break
            if current_index >= empty_places_len:
                return new_puzzle, True
            elif current_index <= -1:
                return new_puzzle, False
    
    def _get_empty_cells(self) -> list:
        """
        Return a list of the indices of the empty places in the puzzle
        """
        empty_places = []
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    empty_places.append((i, j))
        return empty_places