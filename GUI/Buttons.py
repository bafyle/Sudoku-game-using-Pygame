from .Rectangle import *
class Button(Rectangle):
    """
    A Button class is like the cell class but it has a text in the middle
    insted of one number and it has different size and it has a reaction with the mouse
    """
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(attributes, win)
        self.text = text
    
    def draw_text(self, game_font: pygame.freetype.Font):
        padding = self.attributes[2] // 2
        padding -= len(self.text) * 4.5

        game_font.render_to(self.win, (self.attributes[0]+padding, self.attributes[1]+8),
                            self.text, (0, 0, 0))

    def on_mouse_enter(self):
        """
        change the color of the cell if the mouse is hovering on the button
        """
        if self.Enable:
            self.color = Button.MOUSE_ON_COLOR
    

    def on_mouse_exit(self):
        """
        Change the color back of the cell if the mouse was hovering on the button and leaved
        """
        if self.Enable:
            self.color = Button.NORMAL_COLOR

    MOUSE_ON_COLOR = (190, 215, 255)


# derived classes from the button class
class ShowAnswerButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)

class CheckValidButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)
    
    # def is_puzzle_valid(self, puzzle: list) -> bool:
    #     """
    #     Return true if the puzzle is correct and false otherwise, by calling
    #     the isThereOnce method in the Solver Class.
    #     the puzzle may have more that one solution, by checking if every number is
    #     not repeated more than once in its row, column and 3x3 square, we make sure that
    #     this answer is correct rather than checking if the puzzle is equal to the solved puzzle
    #     from the algorithm
    #     """
    #     if self.Enable:
    #         self.solver = Solver(puzzle)
    #         for i in range(9):
    #             for f in range(9):
    #                 if puzzle[i][f] == 0 or not self.solver.is_there_once((i, f), puzzle[i][f]):
    #                     return False
    #         return True

class ResetPuzzleButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)


class HintButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)


class GetAnotherPuzzleButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)
        
        # create instance of database class with the path to the database
    #     self.database_connection = Database("puzzles.db")

    
    # def get_puzzle(self, puzzle_index: int) -> list:
    #     """Get the text puzzle from the database adn convert it to a list"""
    #     if self.Enable:

    #         # get the puzzle from the database as string
    #         puzzle_text = self.database_connection.get_puzzle_string(puzzle_index)

    #         # convert that string to a list of list of integers
    #         new_puzzle = list()
    #         inner_list = list()
    #         for index, char in enumerate(puzzle_text):
    #             if index % 9 == 0 and index != 0:
    #                 new_puzzle.append(inner_list)
    #                 inner_list = list()
    #             inner_list.append(int(char))
    #         new_puzzle.append(inner_list)

    #         # return the new puzzle
    #         return new_puzzle
