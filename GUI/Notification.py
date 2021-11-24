import time
class Notification:

    """
    Class Notification is for informing the player about any information
    """
    def __init__(self):
        self.message = ""
        self.timer = time.time()
        self.positions = list()
        self.invoked = False
        self.currentPosition = tuple()
        self.displayTime = 2
    
    def add_position(self, newPoisition: tuple) -> None:
        """
        This method takes a tuple of 2 integers and store them
        to a list of position.
        """
        self.positions.append(newPoisition)

    def invoke_notification(self, message: str, i: int) -> None:
        if i < len(self.positions):
            self.currentPosition = self.positions[i]
        else:
            print(f"index out of range")
            return
        self.message = message
        self.timer = time.time()
        self.invoked = True

    def draw(self, win, game_font) -> None:
        if self.invoked:
            game_font.render_to(win, self.currentPosition, self.message, (255, 255, 255))
            notificationEndTime = time.time()
            if notificationEndTime - self.timer >= self.displayTime:
                self.invoked = False
        