try:
    import pygame
    import pygame.freetype
    import time
    import random
    import sqlite3
    from puzzleSolver import Solver
    import copy
except ImportError:
    print("pygame is not installed, open command prompt or the terminal "
          "and install the pygame library from \'pip install pygame\' and try again\n"
          "And make sure these files are in the same directory: "
          "puzzleSolver.py file, puzzles folder and fonts folder")
    quit(1)


class Database:
    def __init__(self, dbpath: str):
        self.databasePath = dbpath

        # connect to the database using sqlite3 library
        # And open the database in read-only mode because we will not insert anything
        # to the database
        connectionQuery = f"file:{self.databasePath}?mode=ro"
        self.connection = sqlite3.connect(connectionQuery, uri = True)

        # initialize the query executioner
        self.cursor = self.connection.cursor()
    
    def getPuzzleString(self, id: int) -> str:
        """
        This function reads a puzzle from the database and returns 
        it in string foramt
        """
        # get the puzzle that has 'id' index
        # 'execute()' function returns an iterable object that 
        # contains the output of the select statement 
        puzzleText = self.cursor.execute("SELECT quiz FROM Quizzes WHERE q_id = ?", [id])

        # since the q_id is a primary key in the database,
        # there will be only one object in 'puzzleText'
        # we get that object and reassign 'puzzleText' with it
        for i in puzzleText:
            puzzleText = i
        puzzleText = puzzleText[0]
        
        return puzzleText
    
    def getAnswerString(self, id: int) -> str:
        """
        This functions reads the answer of a certain puzzle and
        returns it in string format
        """
        answerText = self.cursor.execute("SELECT quiz FROM Answers WHERE a_id = ?", [id])

        for i in answerText:
            answerText = i
        answerText = answerText[0]

        return answerText

    def closeConnection(self):
        """Closes the connection of the database without commiting any changes"""
        self.connection.close()
    
    def closeConnectionWithCommit(self):
        """Closes the connection of the database and commits any changes"""
        self.connection.commit()
        self.closeConnection()
        # we didn't use this function since we only read from the database

class Rectangle(object):
    """
    A pygame rectangle that has a position, size and color
    """
    def __init__(self, attributes: tuple, win: pygame.Surface):
        self.attributes = attributes
        self.win = win
        self.NORMAL_COLOR = (230, 240, 255)
        self.SELECTED_COLOR = (190, 215, 255)
        self.DISABLED_COLOR = (117, 117, 117)
        self.Enable = True
        self.rect = pygame.Rect(attributes[0], attributes[1], attributes[2], attributes[3])
        if self.Enable:
            self.color = self.NORMAL_COLOR
        else:
            self.color = self.DISABLED_COLOR
    
    def drawRect(self):
        """
        Drawing the rectangle to the window with the color 
        that specified in 'color' tuple variable in position 
        attributes[0:2] with size attributes[2:]
        """
        if not self.Enable:
            self.color = self.DISABLED_COLOR
        pygame.draw.rect(self.win, self.color, self.rect)
    
    def drawText(self):
        pass

class Cell(Rectangle):
    """
    A cell is a rectangle that contains only a number in the middle of it. 
    The unit of the puzzle.
    """
    def __init__(self, number: int, attributes: tuple, win: pygame.Surface):
        super().__init__(attributes, win)
        self.selected = False
        self.empty = number == 0
        self.number = number

    def select(self) -> None:
        """
        Select or deselect the cell, selecting a cell means change its color
        to SELECTED_COLOR and deselecting a cell means return its color to NORMAL_COLOR
        """
        self.selected = not self.selected
        if not self.selected:
            self.color = self.NORMAL_COLOR
        else:
            self.color = self.SELECTED_COLOR
    
    def drawText(self, game_font: pygame.freetype.Font) -> None:
        """
        Drawing the cell text to the window, which is a single digit number 
        """
        if not self.empty:
            game_font.render_to(self.win, (self.attributes[0]+18, self.attributes[1]+16),
                                str(self.number), (0, 0, 0))
        elif self.number != 0:
            game_font.render_to(self.win, (self.attributes[0]+18, self.attributes[1]+16),
                                str(self.number), (255, 0, 0))

class Button(Rectangle):
    """
    A Button class is like the cell class, a pygame rectangle and a 
    text in the middle of that rectangle but it has different calculation
    for the position of the text
    """
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(attributes, win)
        self.text = text
        self.MOUSE_ON_COLOR = (190, 215, 255)
    
    def drawText(self, game_font: pygame.freetype.Font):
        padding = self.attributes[2] // 2
        padding -= len(self.text) * 4.5

        game_font.render_to(self.win, (self.attributes[0]+padding, self.attributes[1]+8),
                            self.text, (0, 0, 0))

    def onMouseEnter(self):
        """
        change the color of the cell if the mouse is hovering on the button
        """
        if self.Enable:
            self.color = self.MOUSE_ON_COLOR
    

    def onMouseExit(self):
        """
        Change the color back of the cell if the mouse was hovering on the button and leaved
        """
        if self.Enable:
            self.color = self.NORMAL_COLOR

# derived classes from the button class
class ShowAnswerButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)

class CheckValidButton(Button):
    def __init__(self, text: str, attributes: tuple, win: pygame.Surface):
        super().__init__(text, attributes, win)
    
    def isPuzzleValid(self, puzzle: list) -> bool:
        """
        Return true if the puzzle is correct and false otherwise, by calling
        the isThereOnce method in the Solver Class.
        the puzzle may have more that one solution, by checking if every number is
        not repeated more than once in its row, column and 3x3 square, we make sure that
        this answer is correct rather than checking if the puzzle is equal to the solved puzzle
        from the algorithm
        """
        if self.Enable:
            self.solver = Solver(puzzle)
            for i in range(9):
                for f in range(9):
                    if not self.solver.isThereOnce((i, f), puzzle[i][f]):
                        return False
            return True

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
        self.databaseConnection = Database("puzzles/puzzles.db")

    
    def getPuzzle(self, puzzleIndex: int) -> list:
        """Get the text puzzle from the database adn convert it to a list"""
        if self.Enable:

            # get the puzzle from the database as string
            puzzleText = self.databaseConnection.getPuzzleString(puzzleIndex)

            # convert that string to a list of list of integers
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

# board class
class Board(object):
    """
    This class is for managing the board: add a number to the puzzle , solve the puzzle, etc...
    """
    def __init__(self, puzzle: list, win: pygame.Surface):
        self.puzzle = puzzle
        self.OriginalPuzzle = copy.deepcopy(puzzle)
        """
        since python is not using calling by reference nor calling by value,
        OriginalPuzzle must be a new variable that has the same values as puzzle
        but it is not the same instance of puzzle
        print(self.OriginalPuzzle is puzzle) should output False

        using 'self.OriginalPuzzle = puzzle' will affect the OriginalPuzzle variable
        if we modified the puzzle variable and we don't want that
        """
        self.cells = []
        self.solved = False
        self.selectedCell = None
        self.indexOfSelectedCell = ()
        x = 0
        y = 0
        for i in range(9):
            if i % 3 == 0:
                y += 3
            innerList = []
            for j in range(9):
                if j % 3 == 0:
                    x += 3
                c = Cell(self.puzzle[i][j], (x+15, y+15, 50, 50), win)
                innerList.append(c)
                x += 51
            y += 51
            x = 0
            self.cells.append(innerList)
        
        # solve the puzzle and store it in a new variable using deepcopy
        self.solvedPuzzle = copy.deepcopy(self.OriginalPuzzle)
        solver = Solver(self.solvedPuzzle)
        solver.solve()
    
    def refreshCells(self) -> list:
        """insert the numbers of the puzzle to the cells and return the new cells"""
        for i in range(9):
            for j in range(9):
                number = self.puzzle[i][j]
                self.cells[i][j].number = number

    def isFull(self) -> bool:
        """check if the the puzzle is full"""
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    return False
        return True
    
    def clearSelection(self) -> None:
        """Deselect the selected cell and reset the selectedCell and indexOfSelectedCell variables"""
        if self.selectedCell is not None and self.selectedCell.selected:
            self.selectedCell.select()
        self.selectedCell = None
        self.indexOfSelectedCell = ()

def getTimeInString(seconds: int) -> str:
    """ 
    this function takes a number of seconds and convert it
    mm:ss foramt
    """
    minute = seconds // 60
    seconds -= minute*60
    
    second = seconds
    if minute < 10:
        returnString = "0" + str(minute)
    else:
        returnString = str(minute)
    if second < 10:
        returnString += ":0" + str(second)
    else:
        returnString += ":" + str(second)

    return returnString

def draw(win: pygame.Surface, game_font: pygame.freetype.Font) -> None:
    pass


def main():
    """
    Main function
    """
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
    # to be easier for drawing and changing the color
    buttons = [
        CheckValidButton("Check your answer", (550, 50, 200, 30), win),
        ShowAnswerButton("Show answer", (550, 150, 200, 30), win),
        ResetPuzzleButton("Reset", (550, 250, 200, 30), win),
        GetAnotherPuzzleButton("Next puzzle", (550, 450, 200, 30), win),
        HintButton("Hint", (550, 350, 200, 30), win),
    ]

    # load a random puzzle
    currentPuzzleIndex = random.randint(1, 100)
    puzzle = buttons[3].getPuzzle(currentPuzzleIndex)

    # initialize the cells
    board = Board(puzzle, win)
    
    # 3 hints only is allowed 
    hints = 3

    # notification system data 
    notificationString = ""
    showNotification = False
    notificationTimer = time.time()
    NOTIFICATION_PLACE1 = (550, 100) # Under the CheckValidButton
    NOTIFICATION_PLACE2 = (550, 400) # Under the HintButton
    # set the notificationPlace to be under the CheckValidButton as default value
    notificationPlace = NOTIFICATION_PLACE1

    # a timer to tell user how much time he spent
    timerStart = time.time()
    renderString = "00:00"
    timer = 0

    # start the background music
    pygame.mixer.music.load("sounds/background.mp3")
    pygame.mixer.music.play(-1) # infinite loop, play the music again after it finishes
    pygame.mixer.music.set_volume(0.3)

    # # load the correct sound effect
    # correctSound = pygame.mixer.Sound("sounds/correct.mp3")
    # correctSound.set_volume(0.5)

    # a black background color to fill the screen every frame
    BACKGROUND_COLOR = (0, 0, 0)

    # main loop
    running = True
    while running:

        # set FPS to 60
        clock.tick(60)

        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if the user closed the window then break the loop and close
                # the database connection
                running = False
                buttons[3].databaseConnection.closeConnection()
            
            # if the user clicked while the mouse is near the puzzle cells
            # then search for the cell that he selected
            # and store its row and column number
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos() > (14, 14) and pygame.mouse.get_pos() <= (484, 484):
                    for i, row in enumerate(board.cells):
                        breakPoint = False
                        for j, cell in enumerate(row):
                            if cell.rect.collidepoint(pygame.mouse.get_pos()) and cell.empty:
                                # if the mouse was clicked when clicking the mouse was colliding 
                                # with any of the cells, then select that cell
                                cell.select()
                                board.indexOfSelectedCell = (i, j)
                                if board.selectedCell is not None:
                                    board.selectedCell.select()
                                board.selectedCell = cell
                                breakPoint = True
                                break
                        if breakPoint:
                            break

                # if the user clicked in the area of of buttons
                # call 'onClicked' method of the clicked button
                elif pygame.mouse.get_pos() > (540, 0):

                    # check valid button
                    if buttons[0].rect.collidepoint(pygame.mouse.get_pos()) and buttons[0].Enable:
                        validPuzzle = buttons[0].isPuzzleValid(board.puzzle)

                        # notify the user if the puzzle is valid or not
                        if validPuzzle:
                            board.solved = True
                            notificationString = "Your answer is correct!!"
                            # correctSound.play()
                        else:
                            notificationString = "Think again"
                        notificationPlace = NOTIFICATION_PLACE1
                        showNotification = True
                        notificationTimer = time.time()

                    # show answer button
                    elif buttons[1].rect.collidepoint(pygame.mouse.get_pos()) and buttons[1].Enable:
                        board.puzzle = copy.deepcopy(board.solvedPuzzle)
                        board.refreshCells()
                        buttons[2].Enable = False
                        board.solved = True

                    # reset button
                    elif buttons[2].rect.collidepoint(pygame.mouse.get_pos()) and buttons[2].Enable:
                        board.puzzle = copy.deepcopy(board.OriginalPuzzle)
                        board.refreshCells()
                        board.clearSelection()

                    # next puzzle button
                    elif buttons[3].rect.collidepoint(pygame.mouse.get_pos()) and buttons[3].Enable:

                        # load a new random puzzle
                        newIndex = random.randint(1, 100)
                        while newIndex == currentPuzzleIndex:
                            newIndex = random.randint(1, 100)
                        currentPuzzleIndex = newIndex
                        puzzle = buttons[3].getPuzzle(currentPuzzleIndex)
                        
                        # create a new board with the new puzzle
                        board = Board(puzzle, win)

                        # reset the timer
                        timer = 0
                        renderString = "00:00"
                        timerStart = time.time()
                        # enable the reset button
                        buttons[2].Enable = True
                    
                    # hint button
                    elif buttons[4].rect.collidepoint(pygame.mouse.get_pos()):
                        # if that button is enabled and he selected a place 
                        if buttons[4].Enable:
                            if board.selectedCell is not None:
                                # then subtract the hints variable by 1
                                # and get the right number from board.solvedPuzzle list
                                hints -= 1
                                if hints <= 0:
                                    buttons[4].Enable = False
                                r, c = board.indexOfSelectedCell
                                board.puzzle[r][c] = board.solvedPuzzle[r][c]
                                board.refreshCells()
                            else:
                                notificationPlace = NOTIFICATION_PLACE2
                                notificationString = "Select a cell"
                                showNotification = True
                                notificationTimer = time.time()
                        else:
                            notificationPlace = NOTIFICATION_PLACE2
                            notificationString = "You are out of hints"
                            showNotification = True
                            notificationTimer = time.time()


            # if the user pressed a key on the keyboard
            elif event.type == pygame.KEYDOWN:
                # and that key is a num-pad key and the selected cell
                # is empty, then assign the number he pressed to that cell
                if pygame.K_KP1 <= event.key <= pygame.K_KP9:
                    if board.indexOfSelectedCell != ():
                        r, c = board.indexOfSelectedCell
                        if board.cells[r][c].empty:
                            board.puzzle[r][c] = event.key + 1 - pygame.K_KP1
                            board.refreshCells()
                
                # else if that key was an arrow key
                # then navigate in the cells by making the selected cell be
                # whatever the user selected with the arrows
                elif pygame.K_UP >= event.key >= pygame.K_RIGHT:
                    if board.selectedCell is not None:
                        if event.key == pygame.K_UP:
                            new_row = (board.indexOfSelectedCell[0] - 1) % 9
                            new_column = board.indexOfSelectedCell[1]
                        elif event.key == pygame.K_DOWN:
                            new_row = (board.indexOfSelectedCell[0] + 1) % 9
                            new_column = board.indexOfSelectedCell[1]
                        elif event.key == pygame.K_LEFT:
                            new_row = board.indexOfSelectedCell[0]
                            new_column = (board.indexOfSelectedCell[1] - 1 ) % 9
                        else:
                            new_row = board.indexOfSelectedCell[0]
                            new_column = (board.indexOfSelectedCell[1] + 1 ) % 9
                        if board.cells[new_row][new_column].empty:
                            board.selectedCell.select()
                            board.indexOfSelectedCell = (new_row, new_column)
                            board.selectedCell = board.cells[new_row][new_column]
                            board.selectedCell.select()
                        
        # change the color of any button of the mouse is standing over it
        if pygame.mouse.get_pos() > (540, 0):
            for button in buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.onMouseEnter()
                else:
                    button.onMouseExit()
                    
        # fill the screen with black to end the previous frame
        win.fill(BACKGROUND_COLOR)

        #-----drawing section-----#

        #drawing cells
        for rowOfCells in board.cells:
            for cell in rowOfCells:
                cell.drawRect()
                cell.drawText(game_font)
        
        #drawing buttons and their texts
        game_font.size = 20
        for button in buttons:
            button.drawRect()
            button.drawText(game_font)
        
        # instruction to the user
        game_font.render_to(win, (15, 500), "Select a square and enter a number", (255, 255, 255))
        game_font.render_to(win, (15, 530), "You can use the arrow keys to navigate", (255, 255, 255))

        # show the notification for 2 seconds only
        if showNotification:
            game_font.render_to(win, notificationPlace, notificationString, (255, 255, 255))
            notificationTimerEnd = time.time()
            if notificationTimerEnd - notificationTimer >= 2:
                showNotification = False
        
        #drawing timer text
        timerEnd = time.time()
        if timerEnd - timerStart >= 1 and board.solved == False:
            timer += 1
            renderString = getTimeInString(timer)
            timerStart = time.time()
        game_font.render_to(win, (435, 500), renderString, (255, 255, 255))

        #drawing hints text
        game_font.render_to(win, (435, 530), f"hints: {hints}", (255, 255, 255))

        # drawing my name :D
        game_font.render_to(win, (15, 560), "Made with love <3 by Andrew", (255, 82, 113))
        game_font.size = 36

        #update the screen
        pygame.display.flip()

    quit(0)

# if this file is imported, don't execute
if __name__ == "__main__":
    main()
