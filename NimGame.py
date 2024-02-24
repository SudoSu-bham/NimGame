import pygame
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import random
import const as c


class NimGame:
    
    def __init__(self):
        self.checkbox_state = [[False] * c.NUM_COLS for _ in range(c.NUM_ROWS)]
        self.winner_player = None
        self.clock = pygame.time.Clock() # set up clock for managing the frame rate.
        self.randomly_fill_checkboxes()

    def winner(self, name):
        self.winner_player = name
        font = pygame.font.Font(None, 36)
        
        if(name == None): pass
        
        elif(name == 0):
            win_surf = font.render("Computer won!",True,(0, 0, 0))
            rec_surf = win_surf.get_rect(center = (c.WIDTH//10,c.HEIGHT//10))
            c.WIN.blit(win_surf,rec_surf)
        
        else:
            win_surf = font.render("You won!",True,(0, 0, 0))
            rec_surf = win_surf.get_rect(center = (100,100))
            c.WIN.blit(win_surf,rec_surf)    


    def draw_checkboxes(self):
        c.WIN.fill(pygame.Color("white"))
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
        print(end, "Column to remove: ",no_column_remove)
        for i in range(no_column_remove+1):
            self.checkbox_state[row][end-i] = False

        if(self.checkbox_state[0][0] == False and self.checkbox_state[1][0] == False and self.checkbox_state[2][0] == False):
            self.winner(0)

    # This is the easy mode
    def computer_move(self):
        print("computer played")
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
    def draw_button(self):
        BUTTON_FONT = pygame.font.SysFont(None, c.BUTTON_FONT_SIZE)
        button_rect = pygame.Rect((c.WIDTH - c.BUTTON_WIDTH) // 2, c.HEIGHT - 100, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
        pygame.draw.rect(c.WIN, c.BUTTON_COLOR, button_rect)
        button_text = BUTTON_FONT.render(c.BUTTON_TEXT, True, c.BUTTON_TEXT_COLOR)
        text_rect = button_text.get_rect(center=button_rect.center)
        c.WIN.blit(button_text, text_rect)

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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    button_rect = pygame.Rect((c.WIDTH - c.BUTTON_WIDTH) // 2, c.HEIGHT - 100, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
                    if button_rect.collidepoint(x, y):
                        c.BUTTON_TEXT="Reset Game"
                        self.randomly_fill_checkboxes()
                        self.winner_player = None
                        break
                    # elif self.winner_player != None:
                    #     self.winner(self.winner_player)
                    #     print("calling winner")
                    #     break
                    for i in range(c.NUM_ROWS):
                        for j in range(c.NUM_COLS):
                            rect = pygame.Rect((c.WIDTH - c.CHECKBOX_WIDTH) // 2 + j * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), (c.HEIGHT - c.CHECKBOX_HEIGHT) // 2 + i * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), c.CHECKBOX_SIZE, c.CHECKBOX_SIZE)
                            if rect.collidepoint(x, y):
                                if not self.checkbox_state[i][j]:
                                    print("Wrong move")
                                    break
                                self.checkbox_state[i][j] = not self.checkbox_state[i][j]
                                if not self.checkbox_state[i][j]:
                                    for k in range(j, c.NUM_COLS):
                                        self.checkbox_state[i][k] = False
                                    print(i,j,self.checkbox_state[i][j])
                                self.draw_checkboxes() #Updating player move
                                self.computer_move()
                                # pygame.display.update()
                                # time.sleep(1)
                                break

            # c.WIN.fill(c.WHITE)
            self.draw_checkboxes()
            self.draw_button()
            self.winner(self.winner_player)
            pygame.display.update()
            # pygame.display.flip()
            self.clock.tick(30)

def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = NimGame()
    game.run()
    
if __name__ == '__main__':
    main()