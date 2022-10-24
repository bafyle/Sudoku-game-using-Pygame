from .Rectangle import *


class Button(Rectangle):
    """
    A Button class is like the cell class but it has a text in the middle
    insted of one number and it has different size and it has a reaction with the mouse
    """
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(attributes, win)
        self.text = text
    
    def draw(self, game_font: pygame.freetype.Font):
        super()._draw_rect()
        padding = self.attributes[2] // 2
        padding -= len(self.text) * 4.5

        game_font.render_to(self.win, (self.attributes[0]+padding, self.attributes[1]+8),
                            self.text, (0, 0, 0))

    def on_mouse_enter(self):
        """
        change the color of the cell if the mouse is hovering on the button
        """
        if self.Enable:
            self.color = RectangleColor.MOUSE_ON_COLOR.value
    

    def on_mouse_exit(self):
        """
        Change the color back of the cell if the mouse was hovering on the button and leaved
        """
        if self.Enable:
            self.color = RectangleColor.NORMAL_COLOR.value

    
