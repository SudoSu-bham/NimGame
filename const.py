import pygame
RADIUS = 100

WIDTH, HEIGHT = 1024, 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHECKBOX_SIZE = 30
CHECKBOX_MARGIN = 5
NUM_ROWS = 3
NUM_COLS = 21
CHECKBOX_WIDTH = NUM_COLS * CHECKBOX_SIZE + (NUM_COLS - 1) * CHECKBOX_MARGIN
CHECKBOX_HEIGHT = NUM_ROWS * CHECKBOX_SIZE + (NUM_ROWS - 1) * CHECKBOX_MARGIN

# colors
GUNMETAL = (129, 133, 137)  # Gunmetal Gray

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 70
BUTTON_TEXT = "Reset Game"
BUTTON_FONT_SIZE = 40


LINE_SPACING = 20
MARGIN = 30
GAME_RULE = [
    "The game board consists of three rows of checkboxes.",
    "Every time you click on a checked box,checks on this"
    "one and all boxes to the right are removed.",
    "It's you against your computer. The one who removes the last check wins.",
    "Computer responds immediately after you made your move."
]
HELP_SYMBOL = "?"


def init():
    global WIN, WIDTH, HEIGHT
    WIN = pygame.display.get_surface()
