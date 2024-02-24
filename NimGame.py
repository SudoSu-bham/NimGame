import pygame
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import random
import time

import const as c



checkbox_state = [[False] * c.NUM_COLS for _ in range(c.NUM_ROWS)]

# screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

class NimGame:
    
    def __init__(self):
        # set up clock for managing the frame rate.
        self.clock = pygame.time.Clock()


    def draw_checkboxes(self):
        c.WIN.fill(pygame.Color("white"))
        for i in range(c.NUM_ROWS):
            for j in range(c.NUM_COLS):
                rect = pygame.Rect((c.WIDTH - c.CHECKBOX_WIDTH) // 2 + j * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), (c.HEIGHT - c.CHECKBOX_HEIGHT) // 2 + i * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), c.CHECKBOX_SIZE, c.CHECKBOX_SIZE)
                pygame.draw.rect(c.WIN, c.BLACK, rect, 1)
                # Fill checkbox with color if it's checked
                if checkbox_state[i][j]:
                    pygame.draw.rect(c.WIN, "green", rect)

    def toggle_checkbox(self, row, col):
        checkbox_state[row][col] = not checkbox_state[row][col]


    def randomly_fill_checkboxes(self):
        # Reset all checkbox states to False
        for i in range(c.NUM_ROWS):
            for j in range(c.NUM_COLS):
                checkbox_state[i][j] = False

        # Randomly fill checkboxes
        for i in range(c.NUM_ROWS):
            num_to_fill = random.randint(1, c.NUM_COLS)  # Number of checkboxes to fill in current row
            start_col = 0
            for j in range(start_col, start_col + num_to_fill):
                checkbox_state[i][j] = True


    # self.randomly_fill_checkboxes() # Filling randomly for the first time

    # Deleting a range of columns selected by computer
    def delete_column(self, row):
        end = c.NUM_COLS-1
        if(not checkbox_state[row][c.NUM_COLS-1]):
            end =  (checkbox_state[row]).index(False)

        no_column_remove = random.randint(1,end)
        print(end, "Column to remove: ",no_column_remove)
        for i in range(no_column_remove+1):
            checkbox_state[row][end-i] = False

        if(checkbox_state[0][0] == False and checkbox_state[1][0] == False and checkbox_state[2][0] == False):
            font = pygame.font.Font(None, 36)  # Use default system font, size 36
            text = font.render('Computer wins', True, (0, 0, 0))  # Render text
            text_rect = text.get_rect(center=(100, 100))
            c.WIN.blit(text, text_rect)
            # Update the display
            pygame.display.update()
            time.sleep(2)

            print("Computer wins")


    # This is the easy mode
    def computer_move(self):
        print("computer played")
        if(checkbox_state[0][0] == False and checkbox_state[1][0] == False and checkbox_state[2][0] == False):
            font = pygame.font.Font(None, 36)  # Use default system font, size 36
            text = font.render('Player 1 wins!', True, (0, 0, 0))  # Render text
            text_rect = text.get_rect(center=(100, 100))
            c.WIN.blit(text, text_rect)
            # Update the display
            pygame.display.update()
            time.sleep(2)
        
            print("Player wins")
            
        # Computer chooses a column to click on
        if(checkbox_state[0][0] == True):
            self.delete_column(0)
        elif(checkbox_state[1][0] == True):
            self.delete_column(1)
        elif(checkbox_state[2][0] == True):
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
        # screen = pygame.display.get_surface()
        # width = c.WIN.get_width()
        # height = c.WIN.get_height()
        width = c.WIDTH
        height = c.HEIGHT
        dirty = []
        dirty.append(pygame.draw.rect(c.WIN, (255, 255, 255),pygame.Rect(0, 0, width, height)))
        pygame.display.update(dirty)

        while self.running:
            dirty = []

            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    button_rect = pygame.Rect((c.WIDTH - c.BUTTON_WIDTH) // 2, c.HEIGHT - 100, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
                    if button_rect.collidepoint(x, y):
                        self.randomly_fill_checkboxes()
                    for i in range(c.NUM_ROWS):
                        for j in range(c.NUM_COLS):
                            rect = pygame.Rect((c.WIDTH - c.CHECKBOX_WIDTH) // 2 + j * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), (c.HEIGHT - c.CHECKBOX_HEIGHT) // 2 + i * (c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN), c.CHECKBOX_SIZE, c.CHECKBOX_SIZE)
                            if rect.collidepoint(x, y):
                                if not checkbox_state[i][j]:
                                    print("Wrong move")
                                    break
                                checkbox_state[i][j] = not checkbox_state[i][j]
                                if not checkbox_state[i][j]:
                                    for k in range(j, c.NUM_COLS):
                                        checkbox_state[i][k] = False
                                    print(i,j,checkbox_state[i][j])
                                self.draw_checkboxes() #Updating player move
                                self.computer_move()
                                break

            c.WIN.fill(c.WHITE)
            self.draw_checkboxes()
            self.draw_button()
            # pygame.display.update()
            pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = NimGame()
    game.run()
    
if __name__ == '__main__':
    main()