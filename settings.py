# settings for Snake game
import pygame as pg

# highscore file
HS_FILE = "highscore.txt"

# screen settings
WIDTH = 520
HEIGHT = 520
FPS = 45

# game layers
PLAYER_LAYER = 1
WALL_LAYER = 2
FOOD_LAYER = 0

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (117, 20, 20)
BRIGHT_RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 91, 175)
GREY = (211, 211, 211)
MID_RED = (180, 50, 50)
BLINK_ALPHA = [val for val in range(0, 255, 35)]

# fonts
GABRIOLA = pg.font.match_font("Gabriola")
TIMES = pg.font.match_font("Times New Roman")
