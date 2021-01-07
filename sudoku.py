try:
    import pygame
    import pygame.freetype
    import time
    from puzzleSolver import Solver
except ImportError:
    print("Pygame is not installed, open command prompt and install the pygame\n"
          "library from \'pip install pygame\' and try again\n"
          "And make these files are in the same directory: puzzle.txt, puzzleSolver.py")

# cell class wich is a rectangle with some attributes
class cell(object):
    def __init__(self, number: int, attributes: tuple, win: pygame.Surface):
        self.number = number
        self.empty = number == 0
        self.attributes = attributes
        self.selected = False
        self.color = (230, 240, 255)
        self.rect = pygame.Rect(attributes[0], attributes[1],attributes[2],attributes[3])
        self.win = win

    def select(self) -> None:
        self.selected = not self.selected
        if not self.selected:
            self.color = (230, 240, 255)
        else:
            self.color = (190, 215, 255)
    
    def drawText(self, game_font: pygame.freetype.Font) -> None:
        if not self.empty:
            game_font.render_to(self.win, (self.attributes[0]+18, self.attributes[1]+16),
                                str(self.number), (0, 0, 0))
        elif self.number != 0:
            game_font.render_to(self.win, (self.attributes[0]+18, self.attributes[1]+16),
                                str(self.number), (255, 0, 0))
    def drawRect(self):
        pygame.draw.rect(self.win, self.color, self.rect)

# base button class
# to override onClicked method
class Button(object):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        self.text = text
        self.attributes = attributes
        self.win = win
        self.NORMAL_COLOR = (230, 240, 255)
        self.MOUSE_ON_COLOR = (190, 215, 255)
        self.DISABLED_COLOR = (117, 117, 117)
        self.Enable = True
        self.rect = pygame.Rect(attributes[0], attributes[1],attributes[2],attributes[3])
        self.solver = Solver([])
        if self.Enable:
            self.color = self.NORMAL_COLOR
        else:
            self.color = self.DISABLED_COLOR

    def onClicked(self, puzzle: list) -> bool:
        pass
    
    def drawButton(self):
        if not self.Enable:
            self.color = self.DISABLED_COLOR
        pygame.draw.rect(self.win, self.color, self.rect)
        
    
    def drawText(self, game_font: pygame.freetype.Font):
        padding = self.attributes[2] // 2
        padding -= len(self.text) * 4.5

        game_font.render_to(self.win, (self.attributes[0]+padding, self.attributes[1]+8),
                            self.text, (0, 0, 0))
    
    def onMouseEnter(self):
        if self.Enable:
            self.color = self.MOUSE_ON_COLOR
    
    def onMouseExit(self):
        if self.Enable:
            self.color = self.NORMAL_COLOR

# derived classes
class ShowAnswerButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)

    def onClicked(self, puzzle: list) -> None:
        if self.Enable:
            self.solver = Solver(puzzle)
            self.solver.solve()

class CheckValidButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)
        self.Enable = False
    
    def onClicked(self, puzzle: list) -> bool:
        if self.Enable:
            self.solver = Solver(puzzle)
            for i in range(9):
                for f in range(9):
                    if not self.solver.isValidNotInList((i, f), puzzle[i][f]):
                        return False
            return True
class ResetPuzzleButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)
    
    def onClicked(self, puzzle: list) -> list:
        puzzle = Solver.getPuzzleFromFile("puzzle.txt")
        return puzzle


def initializeBoard(puzzleList: list, cellsList: list, win: pygame.Surface):
    
    # intialize the 'cellsList' varaible with cells if it's empty
    # if it's not empty then we re-assign the new numbers from 'puzzleList'
    # to each cell
    if len(cellsList) == 0:
        x = 0
        y = 0
        for i in range(9):
            if i % 3 == 0:
                y += 3
            innerList = []
            for j in range(9):
                if j % 3 == 0:
                    x += 3
                c = cell(puzzleList[i][j], (x+15, y+15, 50, 50), win)
                innerList.append(c)
                x += 51
            y += 51
            x = 0
            cellsList.append(innerList)
    else:
        for i in range(9):
            for j in range(9):
                cellsList[i][j].number = puzzleList[i][j]


def isFull(puzzle: list) -> bool:
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return False
    return True

def draw(win: pygame.Surface, game_font: pygame.freetype.Font) -> None:
    pass

def main():
    pygame.init()

    # framerate clock
    clock = pygame.time.Clock()

    resolution = (800, 600)
    win = pygame.display.set_mode(resolution)

    # loading the font and size of texts
    game_font = pygame.freetype.Font("fonts/BRLNSR.ttf", 36)

    # setting a caption for the window
    pygame.display.set_caption("Sudoku")

    # load our puzzle
    originalPuzzle = Solver.getPuzzleFromFile("puzzle.txt")
    puzzle = Solver.getPuzzleFromFile("puzzle.txt")

    # initialize the cells
    cells = []
    initializeBoard(puzzle, cells, win)

    # buttons list
    buttons = [
        CheckValidButton("Check your answer", (550, 50, 200, 30), win),
        ShowAnswerButton("Show answer", (550, 150, 200, 30), win),
        ResetPuzzleButton("Reset", (550, 250, 200, 30), win),
    ]

    selectedCell = None
    indexOfCurrentCell = tuple()

    notificationString = ""
    showNotification = False
    start_time = time.time()
    # main loop
    running = True
    while running:

        # set FPS to 60
        clock.tick(60)

        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # if the user clicked while the mouse is near the puzzle cells
            # then search for the cell that he selected
            # and store its row and column number
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos() > (14, 14) and pygame.mouse.get_pos() <= (484, 484):
                    for i, row in enumerate(cells):
                        breakPoint = False
                        for j, cell in enumerate(row):
                            if cell.rect.collidepoint(pygame.mouse.get_pos()) and cell.empty:
                                cell.select()
                                indexOfCurrentCell = (i, j)
                                if selectedCell is not None:
                                    selectedCell.select()
                                selectedCell = cell
                                breakPoint = True
                                break
                        if breakPoint:
                            break
                # if the user clicked in the area of of buttons
                # call 'onClicked' method of the clicked button
                elif pygame.mouse.get_pos() > (540, 0):
                    if buttons[0].rect.collidepoint(pygame.mouse.get_pos()) and buttons[0].Enable:
                        returnFromButton = buttons[0].onClicked(puzzle)
                        if returnFromButton:
                            notificationString = "Your answer is correct!!"
                        else:
                            notificationString = "Think again"
                        showNotification = True
                        start_time = time.time()
                        initializeBoard(puzzle, cells, win)

                    elif buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                        puzzle = originalPuzzle
                        buttons[1].onClicked(puzzle)
                        initializeBoard(puzzle, cells, win)

                    elif buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
                        puzzle = buttons[2].onClicked(puzzle)
                        initializeBoard(puzzle, cells, win)

            # if the user pressed a key on the keyboard
            # and that key is 1 -> 9 numpad key and the selected cell
            # is empty, then assign the number he pressed to that cell
            elif event.type == pygame.KEYDOWN:
                if pygame.K_KP1 <= event.key <= pygame.K_KP9:
                    if indexOfCurrentCell != ():
                        r = indexOfCurrentCell[0]
                        c = indexOfCurrentCell[1]
                        if cells[r][c].empty:
                            puzzle[r][c] = event.key + 1 - pygame.K_KP1
                            initializeBoard(puzzle, cells, win)
                            if isFull(puzzle):
                                buttons[0].Enable = True

        
        if pygame.mouse.get_pos() > (540, 0):
            for button in buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.onMouseEnter()
                else:
                    button.onMouseExit()
        win.fill((0, 0, 0))

        #-----drawing section-----#

        #drawing cells
        for cell in cells:
            for c in cell:
                c.drawRect()
                c.drawText(game_font)
        
        #drawing buttons and their texts
        game_font.size = 20
        for button in buttons:
            button.drawButton()
            button.drawText(game_font)
        
        # instruction to the user
        game_font.render_to(win, (15, 500), "Select a cell and enter a number", (255, 255, 255))

        #drawing the notification
        if showNotification:
            game_font.render_to(win, (550, 100), notificationString, (255, 255, 255))
            end_time = time.time()
            if end_time - start_time >= 2:
                showNotification = False
            
        game_font.render_to(win, (15, 560), "Made with love <3 by Andrew", (255, 82, 113))
        game_font.size = 36

        #update the screen
        pygame.display.flip()


# if we imported this file don't execute it
if __name__ == "__main__":
    main()
