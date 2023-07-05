import pygame
import settings
import functions
from classes import Button, TextField
import random
import time
import random
import json
import datetime
import os
from time import sleep
pygame.init()


screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Quick Maths")


def main_menu():
    run = True
    
    training_button = Button(text="Training", 
                             font=settings.main_font_small, 
                             width=400, 
                             height=50, 
                             color=settings.colors.WHITE, 
                             text_color=settings.colors.BLACK, 
                             shadow_color=settings.colors.BLACK, 
                             x=settings.SCREEN_WIDTH/2, 
                             y=250,
                             active=True,
                             inactive_color=settings.colors.WHITE)

    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text("QuickMaths", settings.main_font, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 70, screen) 
        for event in pygame.event.get():
            if training_button.check_clicked(event):
                training_button.animate(screen)
                training_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
        training_button.draw(screen)
        pygame.display.update()
        
    pygame.quit()

def training_menu():
    run = True
    
    start_button = Button(text="Start", 
                          font=settings.main_font_small, 
                          width=400, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=settings.SCREEN_WIDTH/2, 
                          y=700,
                          active=True,
                          inactive_color=settings.colors.WHITE)


    addition_button = Button(text="Addition", 
                          font=settings.main_font_small, 
                          width=400, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=settings.SCREEN_WIDTH/2, 
                          y=300,
                          active=True,
                          inactive_color=settings.colors.GRAY)

    subtraction_button = Button(text="Subtraction", 
                          font=settings.main_font_small, 
                          width=400, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=settings.SCREEN_WIDTH/2, 
                          y=400,
                          active=False,
                          inactive_color=settings.colors.GRAY)


    multiplication_button = Button(text="Multiplication", 
                          font=settings.main_font_small, 
                          width=400, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=settings.SCREEN_WIDTH/2, 
                          y=500,
                          active=False,
                          inactive_color=settings.colors.GRAY)
     
    five_button = Button(text="5", 
                          font=settings.main_font_small, 
                          width=50, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=1500, 
                          y=300,
                          active=False,
                          inactive_color=settings.colors.GRAY)

    ten_button = Button(text="10", 
                          font=settings.main_font_small, 
                          width=50, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=1600, 
                          y=300,
                          active=True,
                          inactive_color=settings.colors.GRAY)

    fifteen_button = Button(text="15", 
                          font=settings.main_font_small, 
                          width=50, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=1700, 
                          y=300,
                          active=False,
                          inactive_color=settings.colors.GRAY)

    twenty_button = Button(text="20", 
                          font=settings.main_font_small, 
                          width=50, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=1800, 
                          y=300,
                          active=False,
                          inactive_color=settings.colors.GRAY)

    
    one_digit_button = Button(text="1", 
                          font=settings.main_font_small, 
                          width=50, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=1500, 
                          y=500,
                          active=False,
                          inactive_color=settings.colors.GRAY)

    two_digit_button = Button(text="2", 
                          font=settings.main_font_small, 
                          width=50, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=1600, 
                          y=500,
                          active=True,
                          inactive_color=settings.colors.GRAY)

    three_digit_button = Button(text="3", 
                          font=settings.main_font_small, 
                          width=50, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=1700, 
                          y=500,
                          active=False,
                          inactive_color=settings.colors.GRAY)

    four_digit_button = Button(text="4", 
                          font=settings.main_font_small, 
                          width=50, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=1800, 
                          y=500,
                          active=False,
                          inactive_color=settings.colors.GRAY)
    
    game_args = {}
    last_answer_time = 0
    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text("Training", settings.main_font, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 70, screen) 

        if pygame.time.get_ticks() - last_answer_time > 100:
            last_answer_time = pygame.time.get_ticks()
            for event in pygame.event.get():

                addition_button.check_clicked(event)
                subtraction_button.check_clicked(event)
                multiplication_button.check_clicked(event)

                if five_button.check_clicked(event):
                    five_button.active = True
                    ten_button.active = False
                    twenty_button.active = False
                    fifteen_button.active = False
                if ten_button.check_clicked(event):
                    ten_button.active = True
                    five_button.active = False
                    twenty_button.active = False
                    fifteen_button.active = False
                if twenty_button.check_clicked(event):
                    twenty_button.active = True
                    five_button.active = False
                    ten_button.active = False
                    fifteen_button.active = False
                if fifteen_button.check_clicked(event):
                    fifteen_button.active = True
                    five_button.active = False
                    ten_button.active = False
                    twenty_button.active = False
                
                if one_digit_button.check_clicked(event):
                    one_digit_button.active = True
                    two_digit_button.active = False
                    three_digit_button.active = False
                    four_digit_button.active = False
                if two_digit_button.check_clicked(event):
                    two_digit_button.active = True
                    one_digit_button.active = False
                    three_digit_button.active = False
                    four_digit_button.active = False
                if three_digit_button.check_clicked(event):
                    three_digit_button.active = True
                    one_digit_button.active = False
                    two_digit_button.active = False
                    four_digit_button.active = False
                if four_digit_button.check_clicked(event):
                    four_digit_button.active = True
                    one_digit_button.active = False
                    two_digit_button.active = False
                    three_digit_button.active = False

                if start_button.check_clicked(event):
                    num_operations = [int(button.text) for button in [five_button, ten_button, fifteen_button, twenty_button] if button.active][0]
                    game_args['mode'] = [addition_button.active, subtraction_button.active, multiplication_button.active]
                    game_args['num_operations'] = num_operations
                    game_args['num_digits'] = [int(button.text) for button in [one_digit_button, two_digit_button, three_digit_button, four_digit_button] if button.active][0]
                    start_button.animate(screen)
                    time_trial(game_args)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.QUIT:
                    run = False


        
        start_button.draw(screen)
        addition_button.draw(screen)
        subtraction_button.draw(screen)
        multiplication_button.draw(screen)

        functions.draw_text("Number of operations", settings.main_font_small, settings.colors.BLACK, 1600, 200, screen)
        five_button.draw(screen)
        ten_button.draw(screen)
        fifteen_button.draw(screen)
        twenty_button.draw(screen)
        functions.draw_text("Number of digits", settings.main_font_small, settings.colors.BLACK, 1600, 400, screen)
        one_digit_button.draw(screen)
        two_digit_button.draw(screen)
        three_digit_button.draw(screen)
        four_digit_button.draw(screen)


        num_operations = [int(button.text) for button in [five_button, ten_button, fifteen_button, twenty_button] if button.active][0]
        game_args['mode'] = [addition_button.active, subtraction_button.active, multiplication_button.active]
        game_args['num_operations'] = num_operations
        game_args['num_digits'] = [int(button.text) for button in [one_digit_button, two_digit_button, three_digit_button, four_digit_button] if button.active][0]
        leaderboard = read_results(game_args)
        show_leaderboard = min(10, len(leaderboard))

        for i in range(show_leaderboard):
            functions.draw_text(f"{i+1}. {leaderboard[i][0]} {leaderboard[i][1]}", settings.main_font_small, settings.colors.BLACK, 300, 200+i*50, screen)

        pygame.display.update()


def get_equation(operator, digits):
    if digits == 1:
        x = random.randint(1, 9)
        y = random.randint(1, 9)
    elif digits == 2:
        x = random.randint(10, 99)
        y = random.randint(10, 99)
    elif digits == 3:
        x = random.randint(100, 999)
        y = random.randint(100, 999)
    elif digits == 4:
        x = random.randint(1000, 9999)
        y = random.randint(1000, 9999)

    if operator == '+':
        result = x + y
    elif operator == '-':
        result = abs(x - y)
    elif operator == '*':
        result = x * y
    return x, y, result, operator 

def get_all_equations(mode, n, digits):
    addition, subtraction, multiplication = mode[0], mode[1], mode[2]
    count = sum([1 for i in mode if i == True])
    n_for_operation = n // count
    print(n_for_operation)
    all_equations = []

    if addition:
        for _ in range(n_for_operation):
            all_equations.append(get_equation('+', digits))
    if subtraction:
        for _ in range(n_for_operation):
            all_equations.append(get_equation('-', digits))
    if multiplication:
        for _ in range(n_for_operation):
            all_equations.append(get_equation('*', digits))

    while len(all_equations) < n:
        operator = random.choice(['+', '-', '*'])
        all_equations.append(get_equation(operator, digits))

    random.shuffle(all_equations)
    print(len(all_equations))
    return all_equations

def check_equation(answer, result):
    if answer != '':
        try:
            integer_answer = int(answer)
        except ValueError as e:
            return False
        return integer_answer == result

def time_trial(game_args):

    input_field = TextField(font=settings.equation_font_small, 
                            width=400,
                            height=70,
                            text_color=settings.colors.BLACK,
                            active_color=settings.colors.WHITE,
                            inactive_color=settings.colors.BLACK,
                            x=settings.SCREEN_WIDTH/2,
                            y=500,
                            prompt_text='')

    answer_button = Button(text="Answer", 
                             font=settings.main_font_small, 
                             width=400, 
                             height=50, 
                             color=settings.colors.WHITE, 
                             text_color=settings.colors.BLACK, 
                             shadow_color=settings.colors.BLACK, 
                             x=settings.SCREEN_WIDTH/2, 
                             y=700,
                             active=True,
                             function=None)
    run = True
    n = game_args['num_operations']

    equations = iter(get_all_equations(game_args['mode'], n, game_args['num_digits']))
    current_equation = next(equations)
    last_answer_time = 0
    background_color = list(settings.colors.BACKGROUND)
    red_step = int((background_color[0])/n) 
    green_step = int((255 - background_color[1])/n) 

    start = time.time()

    num_equations = n 
    current_equation_index = 1
    while run:
        elapsed_time = f'{time.time() - start:.2f}'
        screen.fill(background_color)
        functions.draw_text("Game", settings.main_font, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 70, screen) 
        for event in pygame.event.get():
            
            input_field.get_event(event)
            
            # Because it sometimes triggers to fast, we wait some miliseconds
            if pygame.time.get_ticks() - last_answer_time > 100:
                if answer_button.check_clicked(event):
                    if check_equation(input_field.user_input, current_equation[2]):
                        background_color[0] = max(background_color[0] - green_step, 0)
                        background_color[1] = min(background_color[1] + green_step, 255)
                        background_color[2] = max(background_color[2] - green_step, 0)
                        current_equation_index += 1
                        try:
                            current_equation = next(equations)
                        except StopIteration as e:
                            run = results(background_color, elapsed_time, game_args)
                    else:
                        background_color[0] = min(background_color[0] + red_step, 255)
                        background_color[1] = max(background_color[1] - red_step, 0)
                        background_color[2] = max(background_color[2] - red_step, 0)

                    input_field.user_input = ''
                    last_answer_time = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False

        input_field.update(screen)
        answer_button.draw(screen)

        functions.draw_text(f"{current_equation_index}/{num_equations}", settings.main_font_small, settings.colors.BLACK, 1500, 30, screen, center=False)
        functions.draw_text(f"{current_equation[0]} {current_equation[3]} {current_equation[1]}", settings.equation_font_small, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 300, screen)
        functions.draw_text(elapsed_time, settings.main_font_small, settings.colors.BLACK, 100, 30, screen, center=False)

        pygame.display.update()

def save(game_args, name, result):
    # save to csv 
    file_name = f"{game_args['mode']}_{game_args['num_operations']}_{game_args['num_digits']}"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists('results'):
        os.makedirs('results')
    if not os.path.exists(f"results/{game_args['mode']}_{game_args['num_operations']}.csv"):
        with open(f"results/{game_args['mode']}_{game_args['num_operations']}.csv", 'w') as f:
            f.write(f"{name},{result},{date}\n")    
        return
    leaderboard = read_results(game_args)      
    # check if entry already exists
    # if it does return
    for i, entry in enumerate(leaderboard):
        if entry[0] == name and entry[1] == result:
            return
    
    with open(f"results/{file_name}.csv", 'a') as f:
        f.write(f"{name},{result},{date}\n")

def read_results(game_args):
    file_name = f"{game_args['mode']}_{game_args['num_operations']}_{game_args['num_digits']}"
    if not os.path.exists(f"results/{file_name}.csv"):
        return []
    with open(f"results/{file_name}.csv", 'r') as f:
        results = f.readlines()
        results = [result.strip().split(',') for result in results]
        print("Before sort")
        print(results)
        results = sorted(results, key=lambda x: float(x[1]))
        print("After sort")
        print(results)
        return results


def results(background_color, elapsed_time, game_args):
    run = True
    
    leaderboard = read_results(game_args)


    input_field = TextField(font=settings.main_font_small, 
                            width=700,
                            height=70,
                            text_color=settings.colors.BLACK,
                            active_color=settings.colors.WHITE,
                            inactive_color=settings.colors.BLACK,
                            x=settings.SCREEN_WIDTH/2,
                            y=730,
                            prompt_text='')
    
    try_again_button = Button(text="Try again", 
                             font=settings.main_font_small, 
                             width=400, 
                             height=50, 
                             color=settings.colors.WHITE, 
                             text_color=settings.colors.BLACK, 
                             shadow_color=settings.colors.BLACK, 
                             x=settings.SCREEN_WIDTH/2, 
                             y=930,
                             active=False,
                             inactive_color=settings.colors.WHITE) 

    save_button = Button(text="Save result", 
                             font=settings.main_font_small, 
                             width=400, 
                             height=50, 
                             color=settings.colors.WHITE, 
                             text_color=settings.colors.BLACK, 
                             shadow_color=settings.colors.BLACK, 
                             x=settings.SCREEN_WIDTH/2, 
                             y=830,
                             active=False,
                             inactive_color=settings.colors.WHITE)
    show_leaderboard = min(10, len(leaderboard))
    while run:
        screen.fill(background_color)
        functions.draw_text(elapsed_time, settings.main_font, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 70, screen) 
        for event in pygame.event.get():
            input_field.get_event(event)
            if save_button.check_clicked(event):
                save(game_args, input_field.user_input, elapsed_time)
                sleep(0.5)
                leaderboard = read_results(game_args)
                show_leaderboard = min(10, len(leaderboard))
                save_button.active = False
                
            if try_again_button.check_clicked(event):
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
        input_field.update(screen)

        for i in range(show_leaderboard):
            functions.draw_text(f"{i+1}. {leaderboard[i][0]} {leaderboard[i][1]}", settings.main_font_small, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 200+i*50, screen)

        try_again_button.draw(screen)
        save_button.draw(screen)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main_menu()
