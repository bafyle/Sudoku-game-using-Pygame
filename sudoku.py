try:
    import pygame
    import pygame.freetype
    import time
    import random
    import sqlite3
    from puzzleSolver import Solver
except ImportError:
    print("Pygame is not installed, open command prompt and install the pygame\n"
          "library from \'pip install pygame\' and try again\n"
          "And make these files are in the same directory: puzzle.txt, puzzleSolver.py")
    quit(1)

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

    # the function which derived classes will override
    def onClicked(self, puzzle: list):
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

    def onClicked(self, puzzle: list) -> list:
        if self.Enable:
            self.solver = Solver(puzzle)
            self.solver.solve()

class CheckValidButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)
    
    def onClicked(self, puzzle: list) -> bool:
        if self.Enable:
            self.solver = Solver(puzzle)
            for i in range(9):
                for f in range(9):
                    if not self.solver.isValidOnce((i, f), puzzle[i][f]):
                        return False
            return True

class ResetPuzzleButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)

class GetAnotherPuzzleButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)
        
        # connect to the database using sqlite3 library
        # And open the database in read-only mode because we will not insert anythin
        # to the database
        self.connection = sqlite3.connect('file:puzzles/puzzles.db?mode=ro', uri = True)

        # initialize the query executioner
        self.cursor = self.connection.cursor()

    # return the a new list full of the new puzzle
    def onClicked(self, puzzleIndex: int) -> list:

        # get the puzzle that has 'puzzleIndex' index
        # 'execute()' function returns an iterable object that contains the output of the select statement 
        puzzleText = self.cursor.execute("SELECT quiz FROM Quizzes WHERE q_id = ?", [puzzleIndex])

        # since the q_id is a primary key in the database,
        # there will be only one object in 'puzzleText'
        # we get that object and reassign 'puzzleText\ with it
        for i in puzzleText:
            puzzleText = i
        puzzleText = puzzleText[0]

        # the puzzle now in 'puzzleText' but it is a string
        # we convert that string to a list of list of integers
        newPuzzle = []
        innerList = []
        for i in range(81):
            if i % 9 == 0 and i != 0:
                newPuzzle.append(innerList)
                innerList = []
            innerList.append(int(puzzleText[i]))
        newPuzzle.append(innerList)

        # return the new puzzle
        return newPuzzle

    def closeConnection(self):
        self.connection.close()
    
    def closeConnectionWithCommit(self):
        self.connection.commit()
        self.closeConnection()

def initializeBoard(puzzleList: list, win: pygame.Surface):
    
    # intialize the 'cellsList' varaible with cells if it's empty
    # if it's not empty then we re-assign the new numbers from 'puzzleList'
    # to each cell
    newCellsList = []
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
        newCellsList.append(innerList)
    # else:
    #     for i in range(9):
    #         for j in range(9):
    #             number = puzzleList[i][j]
    #             cellsList[i][j].number = number
    return newCellsList

def refreshBoard(cellsList: list, puzzle: list) -> list:
    for i in range(9):
        for j in range(9):
            number = puzzle[i][j]
            cellsList[i][j].number = number
    return cellsList

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

    # buttons list
    buttons = [
        CheckValidButton("Check your answer", (550, 50, 200, 30), win),
        ShowAnswerButton("Show answer", (550, 150, 200, 30), win),
        ResetPuzzleButton("Reset", (550, 250, 200, 30), win),
        GetAnotherPuzzleButton("Next puzzle", (550, 350, 200, 30), win),
    ]


    # load a random puzzle
    currentPuzzleIndex = random.randint(1, 100)
    originalPuzzle = buttons[3].onClicked(currentPuzzleIndex)
    puzzle = list(originalPuzzle)

    # initialize the cells
    cells = []
    cells = initializeBoard(puzzle, win)

    selectedCell = None
    indexOfCurrentCell = tuple()

    notificationString = ""
    showNotification = False
    notificationTimer = time.time()


    # main loop
    running = True
    while running:

        # set FPS to 60
        clock.tick(60)

        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                buttons[3].closeConnection()
            
            # if the user clicked while the mouse is near the puzzle cells
            # then search for the cell that he selected
            # and store its row and column number
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos() > (14, 14) and pygame.mouse.get_pos() <= (484, 484):
                    for i, row in enumerate(cells):
                        breakPoint = False
                        for j, cell in enumerate(row):
                            if cell.rect.collidepoint(pygame.mouse.get_pos()):
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

                    # check valid button
                    if buttons[0].rect.collidepoint(pygame.mouse.get_pos()) and buttons[0].Enable:
                        returnFromButton = buttons[0].onClicked(puzzle)
                        if returnFromButton:
                            notificationString = "Your answer is correct!!"
                        else:
                            notificationString = "Think again"
                        showNotification = True
                        notificationTimer = time.time()

                    # show answer button
                    elif buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                        puzzle = list(originalPuzzle)
                        buttons[1].onClicked(puzzle)
                        cells = refreshBoard(cells, puzzle)

                    # reset button
                    elif buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
                        puzzle = buttons[3].onClicked(currentPuzzleIndex)
                        originalPuzzle = list(puzzle)
                        cells = initializeBoard(puzzle, win)

                    # next puzzle button
                    elif buttons[3].rect.collidepoint(pygame.mouse.get_pos()):
                        newIndex = random.randint(1, 100)
                        while newIndex == currentPuzzleIndex:
                            newIndex = random.randint(1, 100)
                        currentPuzzleIndex = newIndex
                        originalPuzzle = buttons[3].onClicked(newIndex)
                        puzzle = list(originalPuzzle)
                        cells = initializeBoard(puzzle, win)

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
                            cells = refreshBoard(cells, puzzle)
                            if isFull(puzzle):
                                buttons[0].Enable = True
                            else:
                                buttons[0].Enable = False

        
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
            notificationTimerEnd = time.time()
            if notificationTimerEnd - notificationTimer >= 2:
                showNotification = False
            
        game_font.render_to(win, (15, 560), "Made with love <3 by Andrew", (255, 82, 113))
        game_font.size = 36

        #update the screen
        pygame.display.flip()


# if we imported this file don't execute it
if __name__ == "__main__":
    main()
