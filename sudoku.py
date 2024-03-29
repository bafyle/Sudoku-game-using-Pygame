import time
import random
import copy
import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

try:
    import pygame.freetype
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

    def _check_answer_button_action(self):
        valid_puzzle = self.check_valid_puzzle()
        if valid_puzzle:
            self.board.solved = True
            self.notification.invoke_notification("Your answer is correct!!", 0)
        else:
            self.notification.invoke_notification("Think again", 0)
    
    def _show_answer_button_action(self):
        self.show_answer()
        self.buttons_list[2].Enable = False # disable the reset button
    
    def _next_puzzle_button_action(self):
        self.get_next_puzzle_action()
        self.reset_game_timer()
        self.reset_hints()
        self.notification.kill_notification()
        self.buttons_list[2].Enable = True # enable the reset button
        
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Sudoku")

        self.resolution = (800, 600)
        self.win = pygame.display.set_mode(self.resolution)
        self.game_font = pygame.freetype.Font("fonts/BRLNSR.ttf", 36)
        self.buttons_list = [
            Buttons.Button("Check your answer", (550, 50, 200, 30), self.win, self._check_answer_button_action, {}),
            Buttons.Button("Show answer", (550, 150, 200, 30), self.win, self._show_answer_button_action, {}),
            Buttons.Button("Clear board", (550, 250, 200, 30), self.win, self.reset_board, {}),
            Buttons.Button("Next puzzle", (550, 450, 200, 30), self.win, self._next_puzzle_button_action, {}),
            Buttons.Button("Hint", (550, 350, 200, 30), self.win, self._hint_button_action, {}),
        ]
        self.database_connection = Database("./puzzles.db")
        self.number_of_puzzles = self.database_connection.get_number_of_puzzles()
        self.current_puzzle_index = random.randint(1, self.number_of_puzzles-1)
        self.puzzle = self.get_new_puzzle_from_db_as_list()

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
        pygame.mixer.music.play(-1) # repeat forever
        pygame.mixer.music.set_volume(0.3)

        self.game_running = True
        self.clock = pygame.time.Clock()

    def get_new_puzzle_from_db_as_list(self) -> list:
        """
        This function converts a puzzle that is brought from the db to a list
        """
        puzzle_text = self.database_connection.get_puzzle_string(self.current_puzzle_index)

        # convert that string to a 2D list of integers
        new_puzzle = list()
        inner_list = list()
        for index, char in enumerate(puzzle_text):
            if index % 9 == 0 and index != 0:
                new_puzzle.append(inner_list)
                inner_list = list()
            inner_list.append(int(char))
        new_puzzle.append(inner_list)

        return new_puzzle

    
    def get_next_puzzle_action(self):
        """
        Updates the puzzle ID and gets new puzzle from the database
        """
        self.current_puzzle_index = ((self.current_puzzle_index) % self.number_of_puzzles) + 1
        self.puzzle = self.get_new_puzzle_from_db_as_list()
        self.board = Board.Board(self.puzzle, self.win)
        
    
    def close_database(self) -> None:
        Database.close_connection()

    def check_valid_puzzle(self):
        """
        Return true if the puzzle is correct and false otherwise
        """
        for i in range(9):
            for f in range(9):
                if self.puzzle[i][f] == 0 or not Solver.is_there_once((i, f), self.puzzle[i][f], self.puzzle):
                    return False
        return True

    def reset_game_timer(self) -> None:
        
        self.timer_render_string = "00:00"
        self.timer = 0
        self.timer_start = time.time()
    
    def show_answer(self):
        self.board.puzzle = copy.deepcopy(self.board.solved_puzzle)
        self.puzzle = self.board.puzzle
        self.board.refresh_cells()
        self.board.solved = True
    
    def _hint_button_action(self):
        """
        Action function for the hint button
        """
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
        """
        Clear all guessed numbers from the players, unselect the current bard cell and show a notification
        to the player that the board is cleared.
        """
        self.board.puzzle = copy.deepcopy(self.board.original_puzzle)
        self.board.refresh_cells()
        self.board.deselect_cell()
        self.notification.invoke_notification("Board cleared", 1)

    def reset_hints(self):
        self.hints = 3
        self.buttons_list[4].Enable = True
        
    def get_time(self) -> str:
        """ 
        Convert time from seconds to minutes and seconds format e.g: 1574 seconds -> 26:14
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
                    self.close_database()
                    self.game_running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._mouse_button_pressed_event_handling(event)

                elif event.type == pygame.KEYDOWN:
                    self._keyboard_key_pressed_event_handling(event)
            
            # change the color of any button if the mouse is hovering over it
            if pygame.mouse.get_pos() > (540, 0):
                for button in self.buttons_list:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.on_mouse_enter()
                    else:
                        button.on_mouse_exit()

            #-------------drawing section-------------#

            self.win.fill(Game.BACKGROUND_COLOR) # black background

            for rowOfCells in self.board.cells:
                for cell in rowOfCells:
                    cell.draw(self.game_font)
            
            self.game_font.size = 20
            for button in self.buttons_list:
                button.draw(self.game_font)
            
            self.game_font.render_to(self.win, (15, 500), "Select a square and enter a number", (255, 255, 255))
            self.game_font.render_to(self.win, (15, 530), "You can use the arrow keys and tab to navigate", (255, 255, 255))
            
            self.game_font.render_to(self.win, (15, 560), "Music volume can be changed using mouse wheel", (255, 255, 255))
            self.game_font.size = 20

            self.notification.draw(self.win, self.game_font)

            timerEnd = time.time()
            if timerEnd - self.timer_start >= 1 and self.board.solved == False:
                self.timer += 1
                self.timer_render_string = self.get_time()
                self.timer_start = time.time()
            self.game_font.render_to(self.win, (435, 500), self.timer_render_string, (255, 255, 255))

            self.game_font.render_to(self.win, (435, 530), f"hints: {self.hints}", (255, 255, 255))
            self.game_font.render_to(self.win, (545, 580), "Made with love <3 by Andrew", (255, 82, 113))
            self.game_font.size = 36

            pygame.display.flip()

        sys.exit(0)

    def _mouse_button_pressed_event_handling(self, event):
        if event.button == 1:
            if pygame.mouse.get_pos() > (14, 14) and pygame.mouse.get_pos() <= (484, 484):
                self._mouse_button_1_pressed_on_board(event)

            # if the user clicked in buttons area
            # execute the action function of the pressed button
            elif pygame.mouse.get_pos() > (540, 0):
                self._mouse_button_1_pressed_on_buttons(event)
        
        # change volume using mouse wheel
        elif event.button == 4:
            if pygame.mixer.music.get_volume() != 1:
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
        elif event.button == 5:
            if pygame.mixer.music.get_volume() <= 0.1:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
    
    def _keyboard_key_pressed_event_handling(self, event):
        if (pygame.K_KP1 <= event.key <= pygame.K_KP9) or (pygame.K_1 <= event.key <= pygame.K_9):
            self._keyboard_number_pressed(event)
        
        if pygame.K_UP >= event.key >= pygame.K_RIGHT:
            self._keyboard_arrows_pressed(event)

        if pygame.K_TAB == event.key:
            self._keyboard_tab_pressed(event)

    def _keyboard_number_pressed(self, event):
        # inserting a number from the num-pad to an empty cell
        if self.board.position_of_selected_cell == ():
            return
        r, c = self.board.position_of_selected_cell
        if not self.board.cells[r][c].empty:
            return
        if pygame.K_KP1 <= event.key <= pygame.K_KP9:
            self.board.puzzle[r][c] = event.key + 1 - pygame.K_KP1
        elif pygame.K_1 <= event.key <= pygame.K_9:
            self.board.puzzle[r][c] = event.key - pygame.K_0
        self.board.refresh_cells()
    
    def _keyboard_arrows_pressed(self, event):
        # navigate the board using arrows keys
        if self.board.selected_cell is None:
            return
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
    
    def _keyboard_tab_pressed(self, event):
        # go to the next empty cell using tab
        if self.board.selected_cell is None:
            return
        r, c = self.board.get_next_empty_cell()
        if r != -1:
            self.board.select_cell(r, c)
    
    def _mouse_button_1_pressed_on_board(self, event):
        for i, row in enumerate(self.board.cells):
            for j, cell in enumerate(row):
                if cell.rect.collidepoint(pygame.mouse.get_pos()) and cell.empty:
                    if self.board.selected_cell == cell:
                        self.board.deselect_cell()
                    else:
                        self.board.select_cell(i, j)
                    return
    
    def _mouse_button_1_pressed_on_buttons(self, event):
        for button in self.buttons_list:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and button.Enable:
                button.execute_button_action()

def main():
    game = Game()
    game.game_main_loop()

if __name__ == "__main__":
    main()
