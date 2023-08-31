import pygame

pygame.init()

SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 768
MID_WIDTH = SCREEN_WIDTH / 2
MID_HEIGHT = SCREEN_HEIGHT / 2
SCREEN_THIRDS = [SCREEN_WIDTH/6, SCREEN_WIDTH/2, SCREEN_WIDTH*5/6]

SLEEP_DURATION = 0.1

main_font = pygame.font.SysFont("rasa", 80)
main_font_small = pygame.font.SysFont("rasa", 50)
equation_font_small = pygame.font.SysFont("rasa", 70)
# COLORS
class COLORS:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND = (167, 199, 250)
    LIGHT_GREEN = (161, 210, 250)
    LIGHT_RED = (180, 190, 250)
    GRAY = (220,220,220)

colors = COLORS()
