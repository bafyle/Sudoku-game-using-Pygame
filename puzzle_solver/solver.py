
class Solver(object):
    def __init__(self, puzzle: list):
        self.puzzle = puzzle

    def is_valid(self, index: tuple, guess: int, puzzle: list[list[int]] = None) -> bool:
        """
        Returning a True if the guess is in a correct place and False otherwise.
        This function is used to compare the guess number with its row, column
        and 3x3 square in the puzzle with empty cells
        """
        if puzzle:
            check_puzzle = puzzle
        else:
            check_puzzle = self.puzzle
        
        # first: check if the guess is already exist in its row
        row, col = index
        if guess in check_puzzle[row]:
            return False
        
        # second: check if the guess is already exist in its column
        # we need to get the values of that column first to compare with
        if guess in [check_puzzle[i][col] for i in range(9)]:
            return False

        # third: check if the guess exists in the 3x3 square
        # 1- find what square we try search in by using the floor division operator
        # which will give us the standard division results
        # but floored to the nearest positive real number
        # example: 9/6 = 1.5 -> floor(1.5) = 1
        r = (row // 3) * 3
        c = (col // 3) * 3
        
        # 2- we multiply the result by 3 to get the index of top left cell in that square
        # and we search in that square if the guess is already exists
        for i in range(r, r+3):
            for j in range(c, c+3):
                if check_puzzle[i][j] == guess:
                        return False

        # if the guess doesn't exist in the row, column or the 3x3 square, then return True
        return True
    
    def is_there_once(self, index: tuple, guess: int, puzzle: list[list[int]] = None) -> bool:

        """
        Returning a True if the guess is in the row, column or 3x3 square once only
        and false otherwise. This function is used to compare a guess number in
        a full puzzle with no empty places
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
        it returns True if the puzzle is solved and False if the puzzle is unsolvable.
        """
        empty_places = self._get_empty_cells()
        empty_places_len = len(empty_places)

        if empty_places_len == 0:
            return False
        
        # we will start from the first empty cell which will be in the index 0 in our list
        current_index = 0
        
        # main algorithm
        while True:
            
            # we first get the the row and the column of the empty cell
            r, c = empty_places[current_index]

            # let 'value' be equal to 0
            value = self.puzzle[r][c]

            while True:
                
                # if 'value' is equal to 0, set it to 1
                if value == 0:
                    value = 1
                
                # if 'value' is less that 9, increase it by 1
                elif value < 9:
                    value += 1
                
                # if 'value' is bigger than 9 then backtrack
                # reset 'value' and the cell to 0 to decrease 'currentIndex' by 1
                # to make it points to the empty cell before this one
                # and break from the loop to go the previous cell
                else:
                    value = 0
                    self.puzzle[r][c] = value
                    current_index -= 1
                    break
                    
                # if 'value' which is the guessed number is valid in that cell
                # set the cell to the guessed number and increase the 'currentIndex' by 1
                # to make it points to the next empty cell
                # and break from the loop to go the next cell 
                if self.is_valid(empty_places[current_index], value):
                    self.puzzle[r][c] = value
                    current_index += 1
                    break
                # notice that we check the the row, column and the 3x3 square
                # before we set the cell with our guessed number
            
            # if we are in the last empty cell and we guessed it correctly (We solved it)
            # then 'currentIndex' will be bigger than the length of the list
            # we return True in this case
            if current_index >= empty_places_len:
                return True
            
            # if 'currentIndex' is equal to -1 then the puzzle doesn't have a solution
            # we return False in this case
            elif current_index <= -1:
                return False
            
            # the 'currentIndex' variable will be less than 0 if we backtracked
            # all the empty cell and none of guessed number is correct.
            # when we try every possible number from 1 to 9 and none of them
            # is valid for the first empty cell then 'currentIndex' will be equal to -1
    

    def solve_out_place(self) -> list:
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
        Return a list full of the indices of the empty places in the puzzle
        """
        empty_places = []
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    empty_places.append((i, j))
        return empty_places