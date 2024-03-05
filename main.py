import pygame
import settings
import functions
from classes import (
    Button,
    TextField,
    CheckBoxLayout,
    Navigation,
    ButtonLayout,
    Orientation,
)
import random
import time
import datetime
from collections import defaultdict
import sqlite3

pygame.init()


screen = pygame.display.set_mode((settings.SCREEN_SIZE.x, settings.SCREEN_SIZE.y))
pygame.display.set_caption("Quick Maths")


def main_menu():
    run = True
    first_button_y = 250
    training_button = Button(
        text="Time trial",
        width=400,
        height=50,
        x=settings.SCREEN_SIZE.mid_x,
        y=first_button_y,
        active=True,
    )

    countdown_button = Button(
        text="Countdown",
        width=400,
        height=50,
        x=settings.SCREEN_SIZE.mid_x,
        y=first_button_y + settings.DISTANCE,
        active=True,
    )
    button_layout = ButtonLayout([training_button, countdown_button])
    layout = Navigation([button_layout])
    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text(
            text="QuickMaths",
            font=settings.main_font,
            x=settings.SCREEN_SIZE.mid_x,
            y=70,
            screen=screen,
        )
        for event in pygame.event.get():
            layout.update(event)
            if training_button.check_action(event):
                time_trial_menu()
            if countdown_button.check_action(event):
                countdown_menu()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
        training_button.draw(screen)
        countdown_button.draw(screen)
        pygame.display.update()
    pygame.quit()


def time_trial_menu():
    run = True

    start_button = Button(
        text="Start",
        width=400,
        height=50,
        x=settings.SCREEN_SIZE.mid_x,
        y=600,
        active=True,
    )

    options_layout = CheckBoxLayout(
        ["Addition", "Subtraction", "Multiplication"],
        active=0,
        height=50,
        width=400,
        x=settings.SCREEN_SIZE.mid_x,
        y=200,
        center=False,
        distance=settings.DISTANCE,
    )

    checkboxes_x = settings.SCREEN_SIZE.right_third
    checkboxes_y = 200
    rounds_layout = CheckBoxLayout(
        texts=["5", "10", "15", "20", "∞"],
        active=1,
        height=50,
        width=50,
        x=checkboxes_x,
        y=checkboxes_y,
        distance=settings.DISTANCE,
        orientation=Orientation.HORIZONTAL,
    )
    digits_layout = CheckBoxLayout(
        texts=["1", "2", "3", "4"],
        active=1,
        height=50,
        width=50,
        x=checkboxes_x,
        y=checkboxes_y + settings.DISTANCE * 2,
        distance=settings.DISTANCE,
        orientation=Orientation.HORIZONTAL,
    )
    blind_layout = CheckBoxLayout(
        texts=["off", "0.5", "1", "2"],
        active=0,
        height=50,
        width=60,
        x=checkboxes_x,
        y=checkboxes_y + settings.DISTANCE * 4,
        distance=settings.DISTANCE,
        orientation=Orientation.HORIZONTAL,
    )
    button_layout = ButtonLayout([start_button])
    """
                    2 rounds_layout
    1 options_layout
                    3 digits_layout
                    4 blind layout
    0 start_button
    """
    nav = {
        # start_button nav
        (0, 0, pygame.K_UP): (1, 2),
        (0, 0, pygame.K_RIGHT): (4, 0),
        # options_layout nav
        (1, 0, pygame.K_RIGHT): (2, 0),
        (1, 2, pygame.K_RIGHT): (3, 0),
        (1, 2, pygame.K_DOWN): (0, 0),
        # digits_layout nav
        (3, 0, pygame.K_LEFT): (1, 2),
        (3, 0, pygame.K_DOWN): (4, 0),
        (3, 1, pygame.K_DOWN): (4, 1),
        (3, 2, pygame.K_DOWN): (4, 2),
        (3, 3, pygame.K_DOWN): (4, 3),
        (3, 0, pygame.K_UP): (2, 0),
        (3, 1, pygame.K_UP): (2, 1),
        (3, 2, pygame.K_UP): (2, 2),
        (3, 3, pygame.K_UP): (2, 3),
        # blind_layout nav
        (4, 0, pygame.K_DOWN): (0, 0),
        (4, 1, pygame.K_DOWN): (0, 0),
        (4, 2, pygame.K_DOWN): (0, 0),
        (4, 3, pygame.K_DOWN): (0, 0),
        (4, 0, pygame.K_UP): (3, 0),
        (4, 1, pygame.K_UP): (3, 1),
        (4, 2, pygame.K_UP): (3, 2),
        (4, 3, pygame.K_UP): (3, 3),
        (4, 0, pygame.K_LEFT): (0, 0),
        # rounds_layout nav
        (2, 0, pygame.K_LEFT): (1, 0),
        (2, 0, pygame.K_DOWN): (3, 0),
        (2, 1, pygame.K_DOWN): (3, 1),
        (2, 2, pygame.K_DOWN): (3, 2),
        (2, 3, pygame.K_DOWN): (3, 3),
        (2, 4, pygame.K_DOWN): (3, 3),
    }
    d_navigation = defaultdict(tuple, nav)
    navigation = Navigation(
        [button_layout, options_layout, rounds_layout, digits_layout, blind_layout],
        navigation=d_navigation,
    )
    game_args = {}
    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text(
            text="Time trial",
            font=settings.main_font,
            x=settings.SCREEN_SIZE.mid_x,
            y=70,
            screen=screen,
        )

        functions.draw_text(
            text="Leaderboard",
            font=settings.main_font_small,
            x=settings.SCREEN_SIZE.left_third,
            y=80,
            screen=screen,
        )

        functions.draw_text(
            text="Blind mode",
            font=settings.main_font_small,
            x=checkboxes_x,
            y=checkboxes_y + settings.DISTANCE * 3,
            screen=screen,
        )

        for event in pygame.event.get():
            navigation.update(event)
            digits_layout.update(event)
            options_layout.update(event)
            rounds_layout.update(event)
            blind_layout.update(event)
            if start_button.check_action(event):
                loading(seconds=3)
                time_trial(game_args)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False

        functions.draw_text(
            text="Operations",
            x=checkboxes_x,
            y=120,
            screen=screen,
        )
        functions.draw_text(
            text="Digits",
            x=checkboxes_x,
            y=280,
            screen=screen,
        )

        digits_layout.display(screen)
        options_layout.display(screen)
        rounds_layout.display(screen)
        blind_layout.display(screen)
        start_button.draw(screen)

        game_args["mode"] = options_layout.buttons[
            options_layout.active_id
        ].text.lower()
        game_args["num_operations"] = int(
            rounds_layout.buttons[rounds_layout.active_id].text
        )
        game_args["num_digits"] = int(
            digits_layout.buttons[digits_layout.active_id].text
        )
        game_args["blind"] = blind_layout.buttons[blind_layout.active_id].text

        show_leaderboard(
            game_args=game_args, screen=screen, x=settings.SCREEN_SIZE.left_third, y=150
        )
        pygame.display.update()


def show_leaderboard(game_args, screen, x, y):
    leaderboard = read_results(game_args)
    show_leaderboard = min(10, len(leaderboard))

    for i in range(show_leaderboard):
        functions.draw_text(
            text=f"{i+1}. {leaderboard[i][0]} {leaderboard[i][1]}",
            x=x,
            y=y + i * 50,
            screen=screen,
        )


def get_equation(operator, digits):
    if operator == "*" and digits == 1:
        # don't multiply by one
        random_digits = "".join([str(random.randint(2, 9)) for _ in range(2 * digits)])
    else:
        random_digits = "".join([str(random.randint(1, 9)) for _ in range(2 * digits)])

    x = int(random_digits[:digits])
    y = int(random_digits[digits:])
    result = None
    if operator == "+":
        result = x + y
    elif operator == "-":
        result = abs(x - y)
    elif operator == "*":
        result = x * y
    return x, y, result, operator


def get_all_equations(mode, n, digits):
    all_equations = []
    if mode == "addition":
        for _ in range(n):
            all_equations.append(get_equation("+", digits))
    elif mode == "subtraction":
        for _ in range(n):
            all_equations.append(get_equation("-", digits))
    elif mode == "multiplication":
        for _ in range(n):
            all_equations.append(get_equation("*", digits))

    return all_equations


def check_equation(answer, result):
    if answer == "":
        return
    try:
        integer_answer = int(answer)
    except ValueError as _:
        return False
    return integer_answer == result


def loading(seconds):
    if seconds <= 1:
        raise Exception("Time must be an integer")
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    counter = seconds
    run = True
    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text(
            text=counter,
            font=settings.main_font,
            x=settings.SCREEN_SIZE.mid_x,
            y=settings.SCREEN_SIZE.y - 500,
            screen=screen,
            center=True,
        )
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == timer_event:
                counter -= 1
                if counter == 0:
                    pygame.time.set_timer(timer_event, 0)
                    return
        pygame.display.update()
    pygame.quit()


def time_trial(game_args):
    input_field = TextField(
        font=settings.equation_font_small,
        width=400,
        height=60,
        text_color=settings.colors.BLACK,
        active_color=settings.colors.WHITE,
        inactive_color=settings.colors.BLACK,
        x=settings.SCREEN_SIZE.mid_x,
        y=settings.SCREEN_SIZE.y - 300,
        prompt_text="",
        numeric_only=True,
    )

    answer_button = Button(
        text="Answer",
        width=400,
        height=50,
        x=settings.SCREEN_SIZE.mid_x,
        y=settings.SCREEN_SIZE.y - 200,
        active=True,
    )
    run = True
    n = game_args["num_operations"]
    blind_time = game_args["blind"]
    if blind_time == "off":
        blind_time = 999
    else:
        blind_time = float(blind_time)

    equations = iter(get_all_equations(game_args["mode"], n, game_args["num_digits"]))
    current_equation = next(equations)
    background_color = list(settings.colors.BACKGROUND)
    red_step = int((background_color[0]) / n)
    green_step = int((255 - background_color[1]) / n)

    start = time.time()

    num_equations = n
    current_equation_index = 1

    answer_button.current = True
    blind_timer = time.time()
    while run:
        elapsed_time = f"{time.time() - start:.2f}"
        screen.fill(background_color)
        functions.draw_text(
            text="Time trial",
            font=settings.main_font,
            x=settings.SCREEN_SIZE.mid_x,
            y=70,
            screen=screen,
        )
        for event in pygame.event.get():
            input_field.get_event(event)
            if answer_button.check_action(event):
                if input_field.user_input == "":
                    pass
                elif check_equation(input_field.user_input, current_equation[2]):
                    background_color[0] = max(background_color[0] - green_step, 0)
                    background_color[1] = min(background_color[1] + green_step, 255)
                    background_color[2] = max(background_color[2] - green_step, 0)
                    current_equation_index += 1
                    try:
                        blind_timer = time.time()
                        current_equation = next(equations)
                    except StopIteration as _:
                        run = results(background_color, elapsed_time, game_args)
                else:
                    background_color[0] = min(background_color[0] + red_step, 255)
                    background_color[1] = max(background_color[1] - red_step, 0)
                    background_color[2] = max(background_color[2] - red_step, 0)

                input_field.user_input = ""

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False

        input_field.update(screen)
        answer_button.draw(screen)

        functions.draw_text(
            text=f"{current_equation_index}/{num_equations}",
            x=settings.SCREEN_SIZE.right_third,
            y=70,
            screen=screen,
        )

        if time.time() - blind_timer < blind_time:
            functions.draw_text(
                text=f"{current_equation[0]} {current_equation[3]} {current_equation[1]}",
                font=settings.equation_font_small,
                x=settings.SCREEN_SIZE.mid_x,
                y=settings.SCREEN_SIZE.y - 500,
                screen=screen,
            )
        functions.draw_text(
            elapsed_time,
            x=settings.SCREEN_SIZE.left_third,
            y=70,
            screen=screen,
        )

        pygame.display.update()


def save(game_args, username, result):
    database = sqlite3.connect("scores.db")
    cursor = database.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    category_id = functions.select_category_id(cursor, game_args)
    cursor.execute(
        f"""
                   SELECT COUNT(1) FROM score WHERE name = ? AND result = ? AND date = ? AND category_id = ?
                   """,
        (username, result, date, category_id),
    )
    exists = cursor.fetchall()[0][0]
    if exists:
        return
    cursor.execute(
        f"""
            INSERT INTO score (name, result, date, category_id) VALUES (?, ?, ?, ?)
        """,
        (username, result, date, category_id),
    )
    database.commit()
    database.close()


def read_results(game_args):
    database = sqlite3.connect("scores.db")
    cursor = database.cursor()
    category_id = functions.select_category_id(cursor, game_args)
    cursor.execute(f"SELECT * FROM score WHERE category_id = {category_id}")
    results = cursor.fetchall()
    to_show = [(result[1], result[2]) for result in results]
    to_show_sorted = sorted(to_show, key=lambda x: x[1])[:10]
    database.close()
    return to_show_sorted


def results(background_color, elapsed_time, game_args):
    run = True

    first_button_y = settings.SCREEN_SIZE.y - 300
    input_field = TextField(
        font=settings.main_font_small,
        width=400,
        height=50,
        text_color=settings.colors.BLACK,
        active_color=settings.colors.WHITE,
        inactive_color=settings.colors.BLACK,
        x=settings.SCREEN_SIZE.mid_x,
        y=first_button_y,
        prompt_text="",
    )
    save_button = Button(
        text="Save result",
        width=400,
        height=50,
        x=settings.SCREEN_SIZE.mid_x,
        y=first_button_y + settings.DISTANCE,
        active=True,
    )
    try_again_button = Button(
        text="Try again",
        width=400,
        height=50,
        x=settings.SCREEN_SIZE.mid_x,
        y=first_button_y + settings.DISTANCE * 2,
        active=True,
    )
    button_layout = ButtonLayout([save_button, try_again_button])
    navigation = Navigation([button_layout])
    while run:
        screen.fill(background_color)
        functions.draw_text(
            text=elapsed_time,
            font=settings.main_font,
            x=settings.SCREEN_SIZE.mid_x,
            y=70,
            screen=screen,
        )
        for event in pygame.event.get():
            navigation.update(event)
            input_field.get_event(event)
            if save_button.check_action(event):
                save(game_args, input_field.user_input, elapsed_time)
                save_button.active = False
            if try_again_button.check_action(event):
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False

        input_field.update(screen)
        functions.draw_text(
            text="Leaderboard",
            font=settings.main_font_small,
            x=settings.SCREEN_SIZE.left_third,
            y=80,
            screen=screen,
        )

        show_leaderboard(
            game_args=game_args, screen=screen, x=settings.SCREEN_SIZE.left_third, y=150
        )

        try_again_button.draw(screen)
        save_button.draw(screen)
        pygame.display.update()

    pygame.quit()


def countdown_menu():
    run = True
    options_layout = CheckBoxLayout(
        ["0", "1", "2", "3", "4"],
        active=2,
        height=80,
        width=80,
        x=settings.SCREEN_SIZE.mid_x,
        y=settings.SCREEN_SIZE.mid_y,
        distance=100,
        orientation=Orientation.HORIZONTAL,
    )

    start_button = Button(
        "Start",
        width=400,
        height=50,
        x=settings.SCREEN_SIZE.mid_x,
        y=settings.SCREEN_SIZE.mid_y + 200,
        active=True,
    )
    start_layout = ButtonLayout([start_button])
    """
    options_layout
        start
    """
    # start nav
    nav = {
        (0, 0, pygame.K_UP): (1, 2),
        # options_layout nav
        (1, 0, pygame.K_DOWN): (0, 0),
        (1, 1, pygame.K_DOWN): (0, 0),
        (1, 2, pygame.K_DOWN): (0, 0),
        (1, 3, pygame.K_DOWN): (0, 0),
        (1, 4, pygame.K_DOWN): (0, 0),
    }
    navigation = defaultdict(tuple, nav)
    layout = Navigation([start_layout, options_layout], navigation)
    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text(
            text="Countdown",
            font=settings.main_font,
            x=settings.SCREEN_SIZE.mid_x,
            y=70,
            screen=screen,
        )

        functions.draw_text(
            text="How many big numbers?",
            x=settings.SCREEN_SIZE.mid_x,
            y=170,
            screen=screen,
        )

        for event in pygame.event.get():
            if start_button.check_action(event):
                n_big = int(options_layout.buttons[options_layout.active_id].text)
                loading(seconds=3)
                countdown(n_big)
            options_layout.update(event)

            layout.update(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
        options_layout.display(screen)
        start_button.draw(screen)
        pygame.display.update()


def countdown(n_big):
    run = True
    nums = random.sample([25, 50, 75, 100], n_big)
    small_nums = random.sample(range(1, 11), counts=[2 for _ in range(10)], k=6 - n_big)
    nums.extend(small_nums)
    random.shuffle(nums)
    target = random.randint(101, 999)

    numbers_layout = CheckBoxLayout(
        texts=nums,
        active=-1,
        height=80,
        width=80,
        x=settings.SCREEN_SIZE.mid_x,
        y=settings.SCREEN_SIZE.mid_y,
        distance=100,
        orientation=Orientation.HORIZONTAL,
        inactive_color=settings.colors.WHITE,
    )

    next_button = Button(
        text="Next",
        width=400,
        height=50,
        x=settings.SCREEN_SIZE.mid_x,
        y=settings.SCREEN_SIZE.mid_y + 200,
        active=True,
    )

    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    counter = 30
    background_color = settings.colors.BACKGROUND
    button_layout = ButtonLayout([next_button])
    navigation = Navigation([button_layout])
    while run:
        screen.fill(background_color)
        functions.draw_text(
            text="Countdown",
            font=settings.main_font,
            x=settings.SCREEN_SIZE.mid_x,
            y=70,
            screen=screen,
        )

        functions.draw_text(
            text=target,
            font=settings.main_font,
            x=settings.SCREEN_SIZE.mid_x,
            y=settings.SCREEN_SIZE.mid_y - 100,
            screen=screen,
        )

        functions.draw_text(
            text=counter,
            font=settings.main_font,
            x=200,
            y=100,
            screen=screen,
        )
        for event in pygame.event.get():
            if next_button.check_action(event):
                return
            navigation.update(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == timer_event:
                counter -= 1
                if counter == 0:
                    pygame.time.set_timer(timer_event, 0)
                    background_color = settings.colors.GRAY
        numbers_layout.display(screen)
        next_button.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
