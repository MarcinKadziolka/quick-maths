import pygame

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
MIDDLE_WIDTH = SCREEN_WIDTH / 2
MIDDLE_HEIGHT = SCREEN_HEIGHT / 2

SLEEP_DURATION = 0.1

# main_font = pygame.font.Font("fonts/FFF_Tusj.ttf", 60)
# main_font_small = pygame.font.Font("fonts/FFF_Tusj.ttf", 40)
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
