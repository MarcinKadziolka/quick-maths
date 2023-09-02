import pygame
import settings
import functions
from classes import Button, TextField, CheckBoxLayout
import random
import time
import datetime
import os

pygame.init()


screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Quick Maths")


def main_menu():
    run = True
    first_button_y = 250
    training_button = Button(
        text="Time trial",
        width=400,
        height=50,
        x=settings.MID_WIDTH,
        y=first_button_y,
        active=True,
    )

    countdown_button = Button(
        text="Countdown",
        width=400,
        height=50,
        x=settings.MID_WIDTH,
        y=first_button_y + settings.DISTANCE,
        active=True,
    )

    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text(
            text="QuickMaths",
            font=settings.main_font,
            x=settings.MID_WIDTH,
            y=70,
            screen=screen,
        )
        for event in pygame.event.get():
            if training_button.check_clicked(event):
                training_button.animate(screen)
                time_trial_menu()
            if countdown_button.check_clicked(event):
                countdown_button.animate(screen)
                countdown_settings()

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
        x=settings.MID_WIDTH,
        y=600,
        active=True,
    )

    options_layout = CheckBoxLayout(
        ["Addition", "Subtraction", "Multiplication"],
        active=0,
        height=50,
        width=400,
        x=settings.MID_WIDTH,
        y=200,
        center=False,
        distance=settings.DISTANCE,
    )

    checkboxes_x = settings.SCREEN_THIRDS[2]
    checkboxes_y = 200
    rounds_layout = CheckBoxLayout(
        texts=["5", "10", "15", "20"],
        active=1,
        height=50,
        width=50,
        x=checkboxes_x,
        y=checkboxes_y,
        distance=settings.DISTANCE,
        mode="horizontal",
    )
    digits_layout = CheckBoxLayout(
        texts=["1", "2", "3", "4"],
        active=1,
        height=50,
        width=50,
        x=checkboxes_x,
        y=checkboxes_y + settings.DISTANCE * 2,
        distance=settings.DISTANCE,
        mode="horizontal",
    )

    game_args = {}
    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text(
            text="Time trial",
            font=settings.main_font,
            x=settings.MID_WIDTH,
            y=70,
            screen=screen,
        )

        functions.draw_text(
            text="Leaderboard",
            font=settings.main_font_small,
            x=settings.SCREEN_THIRDS[0],
            y=80,
            screen=screen,
        )

        for event in pygame.event.get():
            options_layout.update(event)
            digits_layout.update(event)
            rounds_layout.update(event)

            if start_button.check_clicked(event):
                start_button.animate(screen)
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

        start_button.draw(screen)
        rounds_layout.display(screen)
        digits_layout.display(screen)
        options_layout.display(screen)

        game_args["mode"] = options_layout.buttons[
            options_layout.active_id
        ].text.lower()
        game_args["num_operations"] = int(
            rounds_layout.buttons[rounds_layout.active_id].text
        )
        game_args["num_digits"] = int(
            digits_layout.buttons[digits_layout.active_id].text
        )
        show_leaderboard(game_args=game_args, screen=screen, x=settings.SCREEN_THIRDS[0], y=150)
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
        random_digits = "".join([str(random.randint(2, 9)) for _ in range(2 * digits)])
    else:
        random_digits = "".join([str(random.randint(1, 9)) for _ in range(2 * digits)])
    x = int(random_digits[:digits])
    y = int(random_digits[digits:])

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


def time_trial(game_args):
    input_field = TextField(
        font=settings.equation_font_small,
        width=400,
        height=60,
        text_color=settings.colors.BLACK,
        active_color=settings.colors.WHITE,
        inactive_color=settings.colors.BLACK,
        x=settings.MID_WIDTH,
        y=settings.SCREEN_HEIGHT - 300,
        prompt_text="",
        numeric_only=True,
    )

    answer_button = Button(
        text="Answer",
        width=400,
        height=50,
        x=settings.MID_WIDTH,
        y=settings.SCREEN_HEIGHT - 200,
        active=True,
    )
    run = True
    n = game_args["num_operations"]

    equations = iter(get_all_equations(game_args["mode"], n, game_args["num_digits"]))
    current_equation = next(equations)
    background_color = list(settings.colors.BACKGROUND)
    red_step = int((background_color[0]) / n)
    green_step = int((255 - background_color[1]) / n)

    start = time.time()

    num_equations = n
    current_equation_index = 1
    while run:
        elapsed_time = f"{time.time() - start:.2f}"
        screen.fill(background_color)
        functions.draw_text(
            text="Game",
            font=settings.main_font,
            x=settings.MID_WIDTH,
            y=70,
            screen=screen,
        )
        for event in pygame.event.get():
            input_field.get_event(event)

            if answer_button.check_clicked(event):
                if input_field.user_input == "":
                    pass
                elif check_equation(input_field.user_input, current_equation[2]):
                    background_color[0] = max(background_color[0] - green_step, 0)
                    background_color[1] = min(background_color[1] + green_step, 255)
                    background_color[2] = max(background_color[2] - green_step, 0)
                    current_equation_index += 1
                    try:
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
            x=settings.SCREEN_WIDTH - 100,
            y=30,
            screen=screen,
            center=False,
        )
        functions.draw_text(
            text=f"{current_equation[0]} {current_equation[3]} {current_equation[1]}",
            font=settings.equation_font_small,
            x=settings.MID_WIDTH,
            y=settings.SCREEN_HEIGHT - 500,
            screen=screen,
        )
        functions.draw_text(
            elapsed_time,
            x=100,
            y=30,
            screen=screen,
            center=False,
        )

        pygame.display.update()


def save(game_args, name, result):
    # save to csv
    file_name = (
        f"{game_args['mode']}_no_{game_args['num_operations']}_nd_{game_args['num_digits']}"
    )
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists("results"):
        os.makedirs("results")
    if not os.path.exists(
        f"results/{game_args['mode']}_{game_args['num_operations']}.csv"
    ):
        with open(
            f"results/{game_args['mode']}_{game_args['num_operations']}.csv", "w"
        ) as f:
            f.write(f"{name},{result},{date}\n")
        return
    leaderboard = read_results(game_args)
    # check if entry already exists
    # if it does return
    for _, entry in enumerate(leaderboard):
        if entry[0] == name and entry[1] == result:
            return

    with open(f"results/{file_name}.csv", "a") as f:
        f.write(f"{name},{result},{date}\n")


def read_results(game_args):
    file_name = f"{game_args['mode']}_no_{game_args['num_operations']}_nd_{game_args['num_digits']}"
    if not os.path.exists(f"results/{file_name}.csv"):
        return []
    with open(f"results/{file_name}.csv", "r") as f:
        results = f.readlines()
        results = [result.strip().split(",") for result in results]
        results = sorted(results, key=lambda x: float(x[1]))

    return results


def results(background_color, elapsed_time, game_args):
    run = True

    first_button_y = settings.SCREEN_HEIGHT - 300
    input_field = TextField(
        font=settings.main_font_small,
        width=400,
        height=50,
        text_color=settings.colors.BLACK,
        active_color=settings.colors.WHITE,
        inactive_color=settings.colors.BLACK,
        x=settings.MID_WIDTH,
        y=first_button_y,
        prompt_text="",
    )
    save_button = Button(
        text="Save result",
        width=400,
        height=50,
        x=settings.MID_WIDTH,
        y=first_button_y + settings.DISTANCE,
        active=True,
    )
    try_again_button = Button(
        text="Try again",
        width=400,
        height=50,
        x=settings.MID_WIDTH,
        y=first_button_y + settings.DISTANCE * 2,
        active=True,
    )
    while run:
        screen.fill(background_color)
        functions.draw_text(
            text=elapsed_time,
            font=settings.main_font,
            x=settings.MID_WIDTH,
            y=70,
            screen=screen,
        )
        for event in pygame.event.get():
            input_field.get_event(event)
            if save_button.check_clicked(event):
                save(game_args, input_field.user_input, elapsed_time)
                save_button.active = False

            if try_again_button.check_clicked(event):
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
            x=settings.SCREEN_THIRDS[0],
            y=80,
            screen=screen,
        )

        show_leaderboard(game_args=game_args, screen=screen, x=settings.SCREEN_THIRDS[0], y=150)

        try_again_button.draw(screen)
        save_button.draw(screen)
        pygame.display.update()

    pygame.quit()


def countdown_settings():
    run = True
    options_layout = CheckBoxLayout(
        ["0", "1", "2", "3", "4"],
        active=2,
        height=80,
        width=80,
        x=settings.MID_WIDTH,
        y=settings.MID_HEIGHT,
        distance=100,
        mode="horizontal",
    )

    start_button = Button(
        "Start",
        width=400,
        height=50,
        x=settings.MID_WIDTH,
        y=settings.MID_HEIGHT + 200,
        active=True,
    )

    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text(
            text="Countdown",
            font=settings.main_font,
            x=settings.MID_WIDTH,
            y=70,
            screen=screen,
        )

        functions.draw_text(
            text="How many big numbers?",
            x=settings.MID_WIDTH,
            y=170,
            screen=screen,
        )

        for event in pygame.event.get():
            options_layout.update(event)

            if start_button.check_clicked(event):
                start_button.animate(screen)
                n_big = int(options_layout.buttons[options_layout.active_id].text)
                countdown(n_big)

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
        x=settings.MID_WIDTH,
        y=settings.MID_HEIGHT,
        distance=100,
        mode="horizontal",
        inactive_color=settings.colors.WHITE,
    )

    next_button = Button(
        text="Next",
        width=400,
        height=50,
        x=settings.MID_WIDTH,
        y=settings.MID_HEIGHT + 200,
        active=True,
    )

    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    counter = 30
    background_color = settings.colors.BACKGROUND
    while run:
        screen.fill(background_color)
        functions.draw_text(
            text="Countdown",
            font=settings.main_font,
            x=settings.MID_WIDTH,
            y=70,
            screen=screen,
        )

        functions.draw_text(
            text=target,
            font=settings.main_font,
            x=settings.MID_WIDTH,
            y=settings.MID_HEIGHT - 100,
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
            if next_button.check_clicked(event):
                next_button.animate(screen)
                return
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
