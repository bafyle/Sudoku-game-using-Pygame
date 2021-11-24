from .Rectangle import *

class Cell(Rectangle):
    """
    A cell is a rectangle that contains one number in the middle.
    a cell can be empty if this cell represents an empty space in the puzzle
    """
    def __init__(self, number: int, attributes: tuple, win: pygame.Surface):
        super().__init__(attributes, win)
        self.selected = False
        self.empty = number == 0
        self.number = number

    def toggle_selection(self) -> None:
        """
        Select or deselect the cell, selecting a cell means change its color
        to SELECTED_COLOR and deselecting a cell means return its color to NORMAL_COLOR
        """
        self.selected = not self.selected
        if not self.selected:
            self.color = super().NORMAL_COLOR
        else:
            self.color = super().SELECTED_COLOR
    
    def draw_text(self, game_font: pygame.freetype.Font) -> None:
        """
        Drawing the cell text to the window, which is a single digit number 
        """
        if not self.empty:
            game_font.render_to(self.win, (self.attributes[0]+18, self.attributes[1]+16),
                                str(self.number), (0, 0, 0))
        elif self.number != 0:
            game_font.render_to(self.win, (self.attributes[0]+18, self.attributes[1]+16),
                                str(self.number), (255, 0, 0))
