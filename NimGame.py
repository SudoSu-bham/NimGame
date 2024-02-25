import pygame
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import random
import const as c


class NimGame:
    
    def __init__(self):
        self.checkbox_state = [[False] * c.NUM_COLS for _ in range(c.NUM_ROWS)]
        self.winner_player = None # To reduce
        self.game_status = None
        self.need_help = False

        self.clock = pygame.time.Clock() # set up clock for managing the frame rate.
        self.randomly_fill_checkboxes()

    def winner(self, name):
        self.winner_player = name
        font = pygame.font.Font(None, 36)
        win_text = "You won!"
        if(name == None): return
        elif(name == 0):
            win_text = "Computer won! Better Luck next time :("

        win_surf = font.render(win_text,True,"white")
        rec_surf = win_surf.get_rect(center = (c.WIDTH-c.WIDTH//2, c.HEIGHT-c.HEIGHT//2+100))
        c.WIN.blit(win_surf,rec_surf)    

        # self.game_status = "done"

    def draw_checkboxes(self):
        # c.WIN.fill(pygame.Color(129, 133, 137))

        for i in range(c.NUM_ROWS):
            for j in range(c.NUM_COLS):
                rect = pygame.Rect((c.WIDTH - c.CHECKBOX_WIDTH) // 2 + j * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), (c.HEIGHT - c.CHECKBOX_HEIGHT) // 2 + i * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), c.CHECKBOX_SIZE, c.CHECKBOX_SIZE)
                pygame.draw.rect(c.WIN, c.BLACK, rect, 2)
                # Fill checkbox with color if it's checked
                if self.checkbox_state[i][j]:
                    pygame.draw.rect(c.WIN, "green", rect)

    def toggle_checkbox(self, row, col):
        self.checkbox_state[row][col] = not self.checkbox_state[row][col]


    def randomly_fill_checkboxes(self):
        # Reset all checkbox states to False
        for i in range(c.NUM_ROWS):
            for j in range(c.NUM_COLS):
                self.checkbox_state[i][j] = False

        # Randomly fill checkboxes
        for i in range(c.NUM_ROWS):
            num_to_fill = random.randint(1, c.NUM_COLS)  # Number of checkboxes to fill in current row
            start_col = 0
            for j in range(start_col, start_col + num_to_fill):
                self.checkbox_state[i][j] = True

    # Deleting a range of columns selected by computer
    def delete_column(self, row):
        end = c.NUM_COLS-1
        if(not self.checkbox_state[row][c.NUM_COLS-1]):
            end =  (self.checkbox_state[row]).index(False)

        no_column_remove = random.randint(1,end)
        for i in range(no_column_remove+1):
            self.checkbox_state[row][end-i] = False

        if(self.checkbox_state[0][0] == False and self.checkbox_state[1][0] == False and self.checkbox_state[2][0] == False):
            self.winner(0)

    # This is the easy mode
    def computer_move(self):
        if(self.checkbox_state[0][0] == False and self.checkbox_state[1][0] == False and self.checkbox_state[2][0] == False):
            self.winner(1)
            
        # Computer chooses a column to click on
        if(self.checkbox_state[0][0] == True):
            self.delete_column(0)
        elif(self.checkbox_state[1][0] == True):
            self.delete_column(1)
        elif(self.checkbox_state[2][0] == True):
            self.delete_column(2)

    # Making a Reset game button
    def draw(self):
        if self.need_help == True:
            c.HELP_SYMBOL = "X"
            y = c.MARGIN
            font = pygame.font.Font(None, 26)
            for line in c.GAME_RULE:
                text_surface = font.render(line, True, "white")
                text_rect = text_surface.get_rect(topleft=(c.MARGIN, y))
                c.WIN.blit(text_surface, text_rect)
                y += c.LINE_SPACING

        BUTTON_FONT = pygame.font.SysFont(None, c.BUTTON_FONT_SIZE)
        self.button_rect = pygame.Rect((c.WIDTH - c.BUTTON_WIDTH) // 2, c.HEIGHT - 150, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
        pygame.draw.rect(c.WIN, c.BUTTON_COLOR, self.button_rect,0,border_radius=20)
        button_text = BUTTON_FONT.render(c.BUTTON_TEXT, True, c.BUTTON_TEXT_COLOR)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        c.WIN.blit(button_text, text_rect)

        HELP_FONT = pygame.font.SysFont(None, 80)
        self.help_cicle = pygame.draw.circle(c.WIN,"white",[c.WIDTH - 100, c.HEIGHT-(c.HEIGHT)+100], 40,40)
        help_text = HELP_FONT.render(c.HELP_SYMBOL, True, (129, 133, 137))
        help_rect = help_text.get_rect(center=self.help_cicle.center)
        c.WIN.blit(help_text,help_rect)


    # Handling events of mouse clicks on boxes
    def player_move(self, x, y):
        for i in range(c.NUM_ROWS):
            for j in range(c.NUM_COLS):
                rect = pygame.Rect((c.WIDTH - c.CHECKBOX_WIDTH) // 2 + j * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), (c.HEIGHT - c.CHECKBOX_HEIGHT) // 2 + i * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), c.CHECKBOX_SIZE, c.CHECKBOX_SIZE)
                if rect.collidepoint(x, y):
                    if not self.checkbox_state[i][j]:
                        break
                    self.checkbox_state[i][j] = not self.checkbox_state[i][j]
                    if not self.checkbox_state[i][j]:
                        for k in range(j, c.NUM_COLS):
                            self.checkbox_state[i][k] = False
                    self.computer_move()
                    break

    # The main game loop.
    def run(self):
        self.running = True
        c.init()
        while self.running:
            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((c.WIDTH, c.HEIGHT), pygame.RESIZABLE)
                    self.game_status = None # This will update screen when changing window size after winning
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    # button_rect = pygame.Rect((c.WIDTH - c.BUTTON_WIDTH) // 2, c.HEIGHT - 100, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
                    # help_cicle = pygame.draw.circle(c.WIN,"green",[c.WIDTH - 100, c.HEIGHT-(c.HEIGHT)+100], 30,30)

                    if self.button_rect.collidepoint(x, y):
                        self.randomly_fill_checkboxes()
                        self.winner_player = None
                        self.game_status = None
                        break
                    elif self.help_cicle.collidepoint(x,y):
                        self.need_help = not self.need_help
                        c.HELP_SYMBOL = "?"
                        self.game_status = None
                        self.draw()

                    if self.game_status == "done": # If the game is completed. No need to go further
                        break

                    self.player_move(x, y)

            if(self.game_status == None):
                c.WIN.fill(pygame.Color(129, 133, 137))
                self.draw_checkboxes()
                self.draw()
                self.winner(self.winner_player)
                pygame.display.update()

                if(self.winner_player != None):
                    self.game_status = "done"
            self.clock.tick(30)

def main():
    pygame.init()
    pygame.display.set_mode((c.WIDTH, c.HEIGHT), pygame.RESIZABLE)
    game = NimGame()
    game.run()
    
if __name__ == '__main__':
    main()