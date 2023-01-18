from .Rectangle import *
from typing import Callable

class Button(Rectangle):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface, action_function: Callable, action_kwargs: dict):
        super().__init__(attributes, win)
        self._text = text
        self._action_function = action_function
        self._kwargs = action_kwargs
    
    def draw(self, game_font: pygame.freetype.Font):
        super()._draw_rect()
        padding = self.attributes[2] // 2
        padding -= len(self._text) * 4.5

        game_font.render_to(self.win, (self.attributes[0]+padding, self.attributes[1]+8),
                            self._text, (0, 0, 0))

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

    def execute_button_action(self):
        self._action_function(**self._kwargs)
