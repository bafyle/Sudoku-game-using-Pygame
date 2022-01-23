# importing necessary libraries
import time
import random
import copy
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
try:
    # importing pygame library
    import pygame.freetype

    # import the Solver class from puzzle_solver module file

    # import Database class from database module
    from database.database import Database

    from GUI import Buttons, Notification, Board
    from puzzle_solver.solver import Solver

except ImportError as error: # catch any import issues
    print(
        "One of the modules or libraries are missing, Please check if Pygame is installed on the current environment, "
        "and check if the current directory has the following: 'database/' 'fonts/' 'GUI/' 'puzzle_solver/' 'sounds/' and 'puzzles.db'"
        )
    print(error)
    sys.exit(1)
    

class Game:
    BACKGROUND_COLOR = (0, 0, 0)

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Sudoku")

        self.resolution = (800, 600)
        self.win = pygame.display.set_mode(self.resolution)
        self.game_font = pygame.freetype.Font("fonts/BRLNSR.ttf", 36)
        self.buttons_list = [
            Buttons.CheckValidButton("Check your answer", (550, 50, 200, 30), self.win),
            Buttons.ShowAnswerButton("Show answer", (550, 150, 200, 30), self.win),
            Buttons.ResetPuzzleButton("Clear", (550, 250, 200, 30), self.win),
            Buttons.GetAnotherPuzzleButton("Next puzzle", (550, 450, 200, 30), self.win),
            Buttons.HintButton("Hint", (550, 350, 200, 30), self.win),
        ]
        self.database_connection = Database("./puzzles.db")
        self.current_puzzle_index = random.randint(1, 100)
        self.puzzle = self.get_new_puzzle()

        self.board = Board.Board(self.puzzle, self.win)
        self.hints = 3

        self.notification = Notification.Notification()
        self.notification.add_position((550, 100)) # add position under the check validation button
        self.notification.add_position((550, 300)) # add position under the resert button
        self.notification.add_position((550, 400)) # add postion under the hint button

        self.timer_start = time.time()
        self.timer_render_string = "00:00"
        self.timer = 0

        pygame.mixer.music.load("./sounds/background.mp3")
        pygame.mixer.music.play(-1) # infinite loop, play the music again after it finishes
        pygame.mixer.music.set_volume(0.3)

        self.game_running = True
        self.clock = pygame.time.Clock()

    def get_new_puzzle(self) -> list:
        """
        This function converts a puzzle that is brought from the db to a list
        """
        puzzle_text = self.database_connection.get_puzzle_string(self.current_puzzle_index)

        # convert that string to a list of list of integers
        new_puzzle = list()
        inner_list = list()
        for index, char in enumerate(puzzle_text):
            if index % 9 == 0 and index != 0:
                new_puzzle.append(inner_list)
                inner_list = list()
            inner_list.append(int(char))
        new_puzzle.append(inner_list)

        # return the new puzzle
        return new_puzzle

    
    def get_next_puzzle_action(self):
        self.current_puzzle_index = ((self.current_puzzle_index + 1) % 101) + 1
        self.puzzle = self.get_new_puzzle()

        # create a new board with the new puzzle
        self.board = Board.Board(self.puzzle, self.win)

        # reset the timer
        self.reset_game_timer()
        self.buttons_list[2].Enable = True # enable the reset button
    
    def close_database(self) -> None:
        Database.close_connection()

    def check_valid_puzzle_action(self):
        """
        Return true if the puzzle is correct and false otherwise, by calling
        the isThereOnce method in the Solver Class.
        the puzzle may have more that one solution, by checking if every number is
        not repeated more than once in its row, column and 3x3 square, we make sure that
        this answer is correct rather than checking if the puzzle is equal to the solved puzzle
        from the algorithm
        """
        solver = Solver(self.puzzle)
        for i in range(9):
            for f in range(9):
                if self.puzzle[i][f] == 0 or not solver.is_there_once((i, f), self.puzzle[i][f]):
                    return False
        return True

    def reset_game_timer(self) -> None:
        self.timer_start = time.time()
        self.timer_render_string = "00:00"
        self.timer = 0
    
    def show_answer_action(self):
        self.board.puzzle = copy.deepcopy(self.board.solved_puzzle)
        self.puzzle = self.board.puzzle
        self.board.refresh_cells()
        self.buttons_list[2].Enable = False
        self.board.solved = True
    
    def hint_action(self):
        if self.buttons_list[4].Enable:
            if self.board.selected_cell is not None:
                self.hints -= 1
                if self.hints <= 0:
                    self.buttons_list[4].Enable = False
                r, c = self.board.position_of_selected_cell
                self.board.puzzle[r][c] = self.board.solved_puzzle[r][c]
                self.board.refresh_cells()
            else:
                self.notification.invoke_notification("Select a cell", 2)
        else:
            self.notification.invoke_notification("You are out of hints", 2)
    
    def reset_board(self):
        self.board.puzzle = copy.deepcopy(self.board.original_puzzle)
        self.board.refresh_cells()
        self.board.clear_selection()
        self.notification.invoke_notification("Board cleared", 1)
    
    def get_time(self) -> str:
        """ 
        this function takes a number of seconds and convert it
        mm:ss format.
        """
        seconds = self.timer
        minutes = seconds // 60
        seconds -= minutes * 60
        
        second = seconds
        if minutes < 10:
            output = "0" + str(minutes)
        else:
            output = str(minutes)
        if second < 10:
            output += ":0" + str(second)
        else:
            output += ":" + str(second)

        return output

    def game_main_loop(self):
        while self.game_running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # if the user closed the window then break the loop and close
                    # the database connection
                    self.close_database()
                    self.game_running = False

                # if the user clicked while the mouse is near the puzzle cells
                # then search for the cell that he selected
                # and store its row and column number
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if pygame.mouse.get_pos() > (14, 14) and pygame.mouse.get_pos() <= (484, 484):
                            for i, row in enumerate(self.board.cells):
                                breakPoint = False
                                for j, cell in enumerate(row):
                                    if cell.rect.collidepoint(pygame.mouse.get_pos()) and cell.empty:
                                        # if the mouse was clicked when clicking the mouse was colliding 
                                        # with any of the cells, then select that cell
                                        self.board.select_cell(i, j)
                                        breakPoint = True
                                        break
                                if breakPoint:
                                    break

                        # if the user clicked in the area of of buttons
                        # call 'onClicked' method of the clicked button
                        elif pygame.mouse.get_pos() > (540, 0):
                            # check valid button
                            if self.buttons_list[0].rect.collidepoint(pygame.mouse.get_pos()) and self.buttons_list[0].Enable:
                                valid_puzzle = self.check_valid_puzzle_action()

                                # notify the user if the puzzle is valid or not
                                if valid_puzzle:
                                    self.board.solved = True
                                    self.notification.invoke_notification("Your answer is correct!!", 0)
                                else:
                                    self.notification.invoke_notification("Think again", 0)
                                
                            # show answer button
                            elif self.buttons_list[1].rect.collidepoint(pygame.mouse.get_pos()) and self.buttons_list[1].Enable:
                                self.show_answer_action()

                            # reset button
                            elif self.buttons_list[2].rect.collidepoint(pygame.mouse.get_pos()) and self.buttons_list[2].Enable:
                                self.reset_board()

                            # next puzzle button
                            elif self.buttons_list[3].rect.collidepoint(pygame.mouse.get_pos()) and self.buttons_list[3].Enable:
                                self.get_next_puzzle_action()
                            
                            # hint button
                            elif self.buttons_list[4].rect.collidepoint(pygame.mouse.get_pos()):
                                self.hint_action()
                    
                    # change volume using mouse wheel
                    elif event.button == 4:
                        if pygame.mixer.music.get_volume() != 1:
                            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
                    elif event.button == 5:
                        if pygame.mixer.music.get_volume() <= 0.1:
                            pygame.mixer.music.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)

                # if the user pressed a key on the keyboard
                elif event.type == pygame.KEYDOWN:
                    # and that key is a num-pad key and the selected cell
                    # is empty, then assign the number he pressed to that cell
                    if pygame.K_KP1 <= event.key <= pygame.K_KP9:
                        if self.board.position_of_selected_cell != ():
                            r, c = self.board.position_of_selected_cell
                            if self.board.cells[r][c].empty:
                                self.board.puzzle[r][c] = event.key + 1 - pygame.K_KP1
                                self.board.refresh_cells()
                    
                    # else if that key was an arrow key
                    # then navigate in the cells by making the selected cell be
                    # whatever the user selected with the arrows
                    elif pygame.K_UP >= event.key >= pygame.K_RIGHT:
                        if self.board.selected_cell is not None:
                            if event.key == pygame.K_UP:
                                new_row = (self.board.position_of_selected_cell[0] - 1) % 9
                                new_column = self.board.position_of_selected_cell[1]
                            elif event.key == pygame.K_DOWN:
                                new_row = (self.board.position_of_selected_cell[0] + 1) % 9
                                new_column = self.board.position_of_selected_cell[1]
                            elif event.key == pygame.K_LEFT:
                                new_row = self.board.position_of_selected_cell[0]
                                new_column = (self.board.position_of_selected_cell[1] - 1 ) % 9
                            else:
                                new_row = self.board.position_of_selected_cell[0]
                                new_column = (self.board.position_of_selected_cell[1] + 1 ) % 9
                            if self.board.cells[new_row][new_column].empty:
                                self.board.select_cell(new_row, new_column)

                    # get the next empty cell by pressing tab
                    elif pygame.K_TAB == event.key:
                        if self.board.selected_cell is not None:
                            r, c = self.board.next_empty_cell()
                            if r != -1:
                                self.board.select_cell(r, c)
            # change the color of any button if the mouse is hovering over it
            if pygame.mouse.get_pos() > (540, 0):
                for button in self.buttons_list:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.on_mouse_enter()
                    else:
                        button.on_mouse_exit()
                        
            # fill the screen with black to end the previous frame
            self.win.fill(Game.BACKGROUND_COLOR)

            #-------------drawing section-------------#

            # drawing cells
            for rowOfCells in self.board.cells:
                for cell in rowOfCells:
                    cell.draw_rect()
                    cell.draw_text(self.game_font)
            
            # drawing buttons and their texts
            self.game_font.size = 20
            for button in self.buttons_list:
                button.draw_rect()
                button.draw_text(self.game_font)
            
            # instruction to the user
            self.game_font.render_to(self.win, (15, 500), "Select a square and enter a number", (255, 255, 255))
            self.game_font.render_to(self.win, (15, 530), "You can use the arrow keys or tab to navigate", (255, 255, 255))
            self.game_font.size = 18
            self.game_font.render_to(self.win, (420, 580), "Music volume can be changed using mouse wheel", (255, 255, 255))
            self.game_font.size = 20
            # show the notification for 2 seconds only
            self.notification.draw(self.win, self.game_font)

            # drawing timer text
            timerEnd = time.time()
            if timerEnd - self.timer_start >= 1 and self.board.solved == False:
                self.timer += 1
                self.timer_render_string = self.get_time()
                self.timer_start = time.time()
            self.game_font.render_to(self.win, (435, 500), self.timer_render_string, (255, 255, 255))

            self.game_font.render_to(self.win, (435, 530), f"hints: {self.hints}", (255, 255, 255))
            self.game_font.render_to(self.win, (15, 560), "Made with love <3 by Andrew", (255, 82, 113))
            self.game_font.size = 36

            # update the screen
            pygame.display.flip()

        sys.exit(0)
                


def main():
    game = Game()
    game.game_main_loop()

if __name__ == "__main__":
    main()
