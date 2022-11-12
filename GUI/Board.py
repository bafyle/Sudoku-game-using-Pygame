import copy
from .Cell import *
from puzzle_solver.solver import Solver

class Board:
    """
    This class is for managing the board: add a number to the puzzle , solve the puzzle, etc...
    """
    def __init__(self, puzzle: list, win: pygame.Surface):
        self.puzzle = puzzle
        self.original_puzzle = copy.deepcopy(puzzle)
        """
        since python is not using calling by reference nor calling by value,
        original_puzzle must be a new variable that has the same values as puzzle
        but it is not the same instance of puzzle.
        print(self.original_puzzle is puzzle) should output False

        using 'self.original_puzzle = puzzle' will affect the original_puzzle
        if we modified 'puzzle' and we don't want that, so we use deepcopy to copy all values of inner
        lists to new inner lists and create new big list to store these new inner lists
        """
        self.cells = []
        self.solved = False
        self.selected_cell = None
        self.position_of_selected_cell = (-1, -1)
        self.index_of_selected_cell = -1
        
        self._prepare_board(win)
        self.solved_puzzle = copy.deepcopy(self.original_puzzle)
        solver = Solver(self.solved_puzzle)
        solver.solve_in_place()
    
    def _prepare_board(self, win: pygame.Surface):
        x = y = 0
        for i in range(9):
            if i % 3 == 0:
                y += 3
            innerList = []
            for j in range(9):
                if j % 3 == 0:
                    x += 3
                c = Cell(self.puzzle[i][j], (x+15, y+15, 50, 50), win)
                innerList.append(c)
                x += 51
            y += 51
            x = 0
            self.cells.append(innerList)

    def refresh_cells(self) -> None:
        """Re-insert all numbers from the board to cells"""
        for i in range(9):
            for j in range(9):
                number = self.puzzle[i][j]
                self.cells[i][j].number = number
    
    def clear_selection(self) -> None:
        """Deselect the selected cell and reset the selectedCell and indexOfSelectedCell variables"""
        if self.selected_cell is not None and self.selected_cell.selected:
            self.selected_cell.toggle_selection()
        self.selected_cell = None
        self.position_of_selected_cell = (-1, -1)
    
    def select_cell(self, row: int, col: int) -> None:
        """
        Select or deselect a cell from the board 
        """
        if 0 <= row < 9 and 0 <= col < 9:
            if self.selected_cell is not None:
                self.selected_cell.toggle_selection()
            self.selected_cell = self.cells[row][col]
            self.selected_cell.toggle_selection()
            self.position_of_selected_cell = (row, col)
    
    def get_next_empty_cell(self) -> tuple:
        """
        This method returns the position (row, column) of
        the next editable cell in tuple
        It is used when the tab button is pressed
        """
        r, c = self.position_of_selected_cell
        if r != -1:
            startPosition = 0
            for i in range(r, 9):
                if i == r: startPosition = c + 1
                else: startPosition = 0
                for f in range(startPosition, 9):
                    if self.cells[i][f].empty:
                        return i, f
        for i in range(9):
            for f in range(9):
                if self.cells[i][f].empty:
                        return i, f
        return -1, -1