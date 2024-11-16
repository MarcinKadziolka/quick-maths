import settings
import random
import pygame
from database import read_results

operation_to_operator = {"addition": "+", "subtraction": "-", "multiplication": "*"}
digit_id_to_num = {0: 5, 1: 10, 2: 99999}


def draw_text(
    text,
    screen: pygame.Surface,
    x: int = settings.SCREEN_SIZE.mid_x,
    y: int = settings.SCREEN_SIZE.mid_y,
    center: bool = True,
    text_color: tuple[int, int, int] = settings.Color.BLACK.value,
    font: pygame.font.FontType = settings.main_font_small,
):
    text_obj = font.render(str(text), True, text_color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    if center:
        text_rect.center = x, y
    screen.blit(text_obj, text_rect)


def show_leaderboard(game_args: dict, screen, x: int, y: int):
    leaderboard = read_results(game_args)
    show_leaderboard = min(10, len(leaderboard))

    for i in range(show_leaderboard):
        draw_text(
            text=f"{i+1}. {leaderboard[i][0]} {leaderboard[i][1]}",
            x=x,
            y=y + i * 50,
            screen=screen,
        )


def get_equation(operator, digits: int) -> tuple[int, int, int, str]:
    if operator == "*" and digits == 1:
        # don't multiply by one
        random_digits = "".join([str(random.randint(2, 9)) for _ in range(2 * digits)])
    else:
        random_digits = "".join([str(random.randint(1, 9)) for _ in range(2 * digits)])

    x = int(random_digits[:digits])
    y = int(random_digits[digits:])
    result = 0
    if operator == "+":
        result = x + y
    elif operator == "-":
        result = abs(x - y)
    elif operator == "*":
        result = x * y
    return x, y, result, operator


def get_all_equations(operator, n: int, digits: int) -> list[tuple]:
    return [get_equation(operator, digits) for _ in range(n)]


# TODO: validate answer
def check_equation(answer: str, result: int) -> bool:
    if answer == "":
        return False
    try:
        integer_answer = int(answer)
    except ValueError as _:
        return False
    return integer_answer == result
