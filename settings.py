from dataclasses import dataclass
import pygame

pygame.init()


@dataclass
class ScreenSize:
    x: int
    y: int

    @property
    def mid_x(self) -> float:
        return self.x / 2

    @property
    def mid_y(self) -> float:
        return self.y / 2

    @property
    def left_third(self) -> float:
        return self.x / 6

    @property
    def middle_third(self) -> float:
        return self.x / 2

    @property
    def right_third(self) -> float:
        return self.x * 5 / 6


SCREEN_SIZE = ScreenSize(1366, 768)

DISTANCE = 80
SLEEP_DURATION = 0.1

main_font = pygame.font.SysFont("rasa", 80)
main_font_small = pygame.font.SysFont("rasa", 50)
equation_font_small = pygame.font.SysFont("rasa", 70)


class COLORS:
    WHITE = [255, 255, 255]
    BLACK = [0, 0, 0]
    BACKGROUND = [167, 199, 250]
    GREEN = [127, 255, 212]
    LIGHT_GREEN = [179, 255, 230]
    LIGHT_RED = [180, 190, 250]
    GRAY = [220, 220, 220]


colors = COLORS()
