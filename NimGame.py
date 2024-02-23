import pygame
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import random
import time



RADIUS = 100

WIDTH, HEIGHT = 750, 750
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHECKBOX_SIZE = 30
CHECKBOX_MARGIN = 5
NUM_ROWS = 3
NUM_COLS = 20
CHECKBOX_WIDTH = NUM_COLS * CHECKBOX_SIZE + (NUM_COLS - 1) * CHECKBOX_MARGIN
CHECKBOX_HEIGHT = NUM_ROWS * CHECKBOX_SIZE + (NUM_ROWS - 1) * CHECKBOX_MARGIN


BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_COLOR = (0, 150, 0)  # Green
BUTTON_TEXT_COLOR = WHITE
BUTTON_TEXT = "Reset game"
BUTTON_FONT_SIZE = 20




checkbox_state = [[False] * NUM_COLS for _ in range(NUM_ROWS)]

def draw_checkboxes():
        screen.fill(pygame.Color("white"))
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                rect = pygame.Rect((WIDTH - CHECKBOX_WIDTH) // 2 + j * (CHECKBOX_SIZE + CHECKBOX_MARGIN), (HEIGHT - CHECKBOX_HEIGHT) // 2 + i * (CHECKBOX_SIZE + CHECKBOX_MARGIN), CHECKBOX_SIZE, CHECKBOX_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
                # Fill checkbox with color if it's checked
                if checkbox_state[i][j]:
                    pygame.draw.rect(screen, "green", rect)

def toggle_checkbox(row, col):
    checkbox_state[row][col] = not checkbox_state[row][col]


def randomly_fill_checkboxes():
    # Reset all checkbox states to False
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            checkbox_state[i][j] = False

    # Randomly fill checkboxes
    for i in range(NUM_ROWS):
        num_to_fill = random.randint(1, NUM_COLS)  # Number of checkboxes to fill in current row
        # start_col = random.randint(0, NUM_COLS - num_to_fill)  # Starting column index for filling checkboxes
        start_col = 0
        for j in range(start_col, start_col + num_to_fill):
            checkbox_state[i][j] = True


# randomly_fill_checkboxes() # Filling randomly for the first time

# Deleting a range of columns selected by computer
def delete_column(row):
    end = NUM_COLS-1
    if(not checkbox_state[row][NUM_COLS-1]):
        end =  (checkbox_state[row]).index(False)

    no_column_remove = random.randint(1,end)
    print(end, "Column to remove: ",no_column_remove)
    for i in range(no_column_remove+1):
        checkbox_state[row][end-i] = False

    if(checkbox_state[0][0] == False and checkbox_state[1][0] == False and checkbox_state[2][0] == False):
        font = pygame.font.Font(None, 36)  # Use default system font, size 36
        text = font.render('Computer wins', True, (0, 0, 0))  # Render text
        text_rect = text.get_rect(center=(100, 100))
        screen.blit(text, text_rect)
        # Update the display
        pygame.display.update()
        time.sleep(2)

        print("Computer wins")


# This is the easy mode
def computer_move():
    print("computer played")
    if(checkbox_state[0][0] == False and checkbox_state[1][0] == False and checkbox_state[2][0] == False):
        font = pygame.font.Font(None, 36)  # Use default system font, size 36
        text = font.render('Player 1 wins!', True, (0, 0, 0))  # Render text
        text_rect = text.get_rect(center=(100, 100))
        screen.blit(text, text_rect)
        # Update the display
        pygame.display.update()
        time.sleep(2)
    
        print("Player wins")
        
    # Computer chooses a column to click on
    if(checkbox_state[0][0] == True):
        delete_column(0)
    elif(checkbox_state[1][0] == True):
        delete_column(1)
    elif(checkbox_state[2][0] == True):
        delete_column(2)
    

# Making a Reset game button
def draw_button():
    BUTTON_FONT = pygame.font.SysFont(None, BUTTON_FONT_SIZE)
    button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    button_text = BUTTON_FONT.render(BUTTON_TEXT, True, BUTTON_TEXT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)



screen = pygame.display.set_mode((WIDTH, HEIGHT))

class NimGame:
    
    def __init__(self):
        # set up clock for managing the frame rate.
        self.clock = pygame.time.Clock()
    
    # The main game loop.
    def run(self):
        self.running = True
        screen = pygame.display.get_surface()
        # width = screen.get_width()
        # height = screen.get_height()
        width = WIDTH
        height = HEIGHT
        dirty = []
        dirty.append(pygame.draw.rect(screen, (255, 255, 255),pygame.Rect(0, 0, width, height)))
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
                    button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
                    if button_rect.collidepoint(x, y):
                        randomly_fill_checkboxes()
                    for i in range(NUM_ROWS):
                        for j in range(NUM_COLS):
                            rect = pygame.Rect((WIDTH - CHECKBOX_WIDTH) // 2 + j * (CHECKBOX_SIZE + CHECKBOX_MARGIN), (HEIGHT - CHECKBOX_HEIGHT) // 2 + i * (CHECKBOX_SIZE + CHECKBOX_MARGIN), CHECKBOX_SIZE, CHECKBOX_SIZE)
                            if rect.collidepoint(x, y):
                                if not checkbox_state[i][j]:
                                    print("Wrong move")
                                    break
                                checkbox_state[i][j] = not checkbox_state[i][j]
                                if not checkbox_state[i][j]:
                                    for k in range(j, NUM_COLS):
                                        checkbox_state[i][k] = False
                                    print(i,j,checkbox_state[i][j])
                                draw_checkboxes() #Updating player move
                                computer_move()
                                break

            screen.fill(WHITE)
            draw_checkboxes()
            draw_button()
            # pygame.display.update()
            pygame.display.flip()

def main():
    pygame.init()
    # pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = NimGame()
    game.run()
    
if __name__ == '__main__':
    main()