import time
import logging
class Notification:

    """
    Class Notification is for informing the player about any information
    """
    DISPLAY_TIME = 2

    def __init__(self, color: tuple = (255, 255, 255)):
        self.message = ""
        self.timer = time.time()
        self.positions = list()
        self.invoked = False
        self.currentPosition = tuple()
        self.color = color
    
    def add_position(self, new_position: tuple) -> None:
        """
        This method takes a tuple of 2 integers and store them
        to a list of position.
        """
        self.positions.append(new_position)

    def invoke_notification(self, message: str, i: int) -> None:
        if i < len(self.positions):
            self.currentPosition = self.positions[i]
        else:
            logging.warning(f"position index out of range")
            return
        self.message = message
        self.timer = time.time()
        self.invoked = True

    def kill_notification(self):
        self.invoked = False
    
    def draw(self, win, game_font) -> None:
        if not self.invoked:
            return
        game_font.render_to(win, self.currentPosition, self.message, self.color)
        notificationEndTime = time.time()
        if notificationEndTime - self.timer >= Notification.DISPLAY_TIME:
            self.invoked = False
        