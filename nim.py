import pygame as pg
import sys
import random
import time


pg.init()
screen_size = 750,750
# screen = pg.display.set_mode(screen_size)

# win = pg.display.set_mode((800, 600))

pg.display.set_caption("Nim game")

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
BUTTON_FONT = pg.font.SysFont(None, BUTTON_FONT_SIZE)



checkbox_state = [[False] * NUM_COLS for _ in range(NUM_ROWS)]


def draw_checkboxes():
    screen.fill(pg.Color("white"))
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            rect = pg.Rect((WIDTH - CHECKBOX_WIDTH) // 2 + j * (CHECKBOX_SIZE + CHECKBOX_MARGIN), (HEIGHT - CHECKBOX_HEIGHT) // 2 + i * (CHECKBOX_SIZE + CHECKBOX_MARGIN), CHECKBOX_SIZE, CHECKBOX_SIZE)
            pg.draw.rect(screen, BLACK, rect, 1)
            # Fill checkbox with color if it's checked
            if checkbox_state[i][j]:
                pg.draw.rect(screen, "green", rect)

def toggle_checkbox(row, col):
    checkbox_state[row][col] = not checkbox_state[row][col]

# def game_loop():
#     for event in pg.event.get():
#         if event.type == pg.QUIT: sys.exit()
    
#     draw_background()
#     pg.display.flip()

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


randomly_fill_checkboxes()

def delete_column(row):
    end = NUM_COLS-1
    if(not checkbox_state[row][NUM_COLS-1]):
        end =  (checkbox_state[row]).index(False)

    no_column_remove = random.randint(1,end)
    print(end, "Column to remove: ",no_column_remove)
    for i in range(no_column_remove+1):
        checkbox_state[row][end-i] = False

def computer_move():
    print("computer played")
    if(checkbox_state[0][0] == False and checkbox_state[1][0] == False and checkbox_state[2][0] == False):
        font = pg.font.Font(None, 36)  # Use default system font, size 36
        text = font.render('Hello, Pygame!', True, (0, 0, 0))  # Render text with black color
        text_rect = text.get_rect(center=(100, 100))
        screen.blit(text, text_rect)
        # Update the display
        pg.display.update()
        time.sleep(2)
    
        print("Player Has won")
        
    #Computer chooses a column to click on
    if(checkbox_state[0][0] == True):
        delete_column(0)
    elif(checkbox_state[1][0] == True):
        delete_column(1)
    elif(checkbox_state[2][0] == True):
        delete_column(2)


def draw_button():
    button_rect = pg.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
    pg.draw.rect(screen, BUTTON_COLOR, button_rect)
    button_text = BUTTON_FONT.render(BUTTON_TEXT, True, BUTTON_TEXT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)


screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Checkbox Example")


running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pg.mouse.get_pos()
            button_rect = pg.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
            if button_rect.collidepoint(x, y):
                randomly_fill_checkboxes()
            for i in range(NUM_ROWS):
                for j in range(NUM_COLS):
                    rect = pg.Rect((WIDTH - CHECKBOX_WIDTH) // 2 + j * (CHECKBOX_SIZE + CHECKBOX_MARGIN), (HEIGHT - CHECKBOX_HEIGHT) // 2 + i * (CHECKBOX_SIZE + CHECKBOX_MARGIN), CHECKBOX_SIZE, CHECKBOX_SIZE)
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
    pg.display.update()
    # pg.display.flip()

pg.quit()
sys.exit()

# while True:
#     game_loop()
