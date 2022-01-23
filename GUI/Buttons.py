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

class ResetPuzzleButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)


class HintButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)


class GetAnotherPuzzleButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)