from abc import ABC, abstractmethod
import pygame

class Rectangle(ABC):
    """
    Pygame rectangle that has 3 attributes: position, size and color
    """
    def __init__(self, attributes: tuple, win: pygame.Surface):
        self.attributes = attributes
        self.win = win
        self.Enable = True
        self.rect = pygame.Rect(attributes[0], attributes[1], attributes[2], attributes[3])
        if self.Enable:
            self.color = Rectangle.NORMAL_COLOR
        else:
            self.color = Rectangle.DISABLED_COLOR
    
    def draw_rect(self):
        """
        Drawing the rectangle to the window with the color 
        that specified in 'color' tuple variable in position 
        attributes[0:2] with size attributes[2:]
        """
        if not self.Enable:
            self.color = Rectangle.DISABLED_COLOR
        pygame.draw.rect(self.win, self.color, self.rect)
    
    @abstractmethod
    def draw_text(self):
        pass
    
    NORMAL_COLOR = (230, 240, 255)
    SELECTED_COLOR = (190, 215, 255)
    DISABLED_COLOR = (117, 117, 117)