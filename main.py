import pygame
import settings
import functions
from classes import Button, TextField
import random
import time
pygame.init()


screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Quick Maths")


def main_menu():
    run = True
    
    training_button = Button(text="Training", 
                             font=settings.main_font_small, 
                             width=200, 
                             height=50, 
                             color=settings.colors.WHITE, 
                             text_color=settings.colors.BLACK, 
                             shadow_color=settings.colors.BLACK, 
                             x=settings.SCREEN_WIDTH/2, 
                             y=250,
                             active=True)
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
                          width=200, 
                          height=50, 
                          color=settings.colors.WHITE, 
                          text_color=settings.colors.BLACK, 
                          shadow_color=settings.colors.BLACK, 
                          x=settings.SCREEN_WIDTH/2, 
                          y=settings.SCREEN_HEIGHT/2,
                          active=True)
    while run:
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text("Training", settings.main_font, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 70, screen) 
        for event in pygame.event.get():
            if start_button.check_clicked(event):
                start_button.animate(screen)
                game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
        start_button.draw(screen)
        pygame.display.update()


def get_equation():
    x = random.randint(10, 100)
    y = random.randint(10, 100)
    result = x + y
    return x, y, result

def check_equation(answer, result):
    if answer != '':
        return int(answer) == result

def game():

    input_field = TextField(font=settings.main_font_small, 
                            width=200,
                            height=70,
                            text_color=settings.colors.BLACK,
                            active_color=settings.colors.WHITE,
                            inactive_color=settings.colors.BLACK,
                            x=settings.SCREEN_WIDTH/2,
                            y=500,
                            prompt_text='')

    answer_button = Button(text="Answer", 
                             font=settings.main_font_small, 
                             width=200, 
                             height=50, 
                             color=settings.colors.WHITE, 
                             text_color=settings.colors.BLACK, 
                             shadow_color=settings.colors.BLACK, 
                             x=settings.SCREEN_WIDTH/2, 
                             y=700,
                             active=True,
                             function=None)
    run = True
    n = 10
    equations = iter([get_equation() for _ in range(n)])
    current_equation = next(equations)
    last_answer_time = 0
    background_color = list(settings.colors.BACKGROUND)
    red_step = int((background_color[0])/n) 
    green_step = int((255 - background_color[1])/n) 

    start = time.time()

    while run:
        elapsed_time = f'{time.time() - start:.2f}'
        screen.fill(background_color)
        functions.draw_text("Game", settings.main_font, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 70, screen) 
        for event in pygame.event.get():
            input_field.get_event(event)
            
            # Because it sometimes triggers to fast, we wait some miliseconds
            if pygame.time.get_ticks() - last_answer_time > 100:
                if answer_button.check_clicked(event):
                    if check_equation(input_field.user_input, current_equation[-1]):
                        background_color[0] = max(background_color[0] - green_step, 0)
                        background_color[1] = min(background_color[1] + green_step, 255)
                        background_color[2] = max(background_color[2] - green_step, 0)
                        try:
                            current_equation = next(equations)
                        except StopIteration as e:
                            results(background_color, elapsed_time)
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
        functions.draw_text(f"{current_equation[0]} + {current_equation[1]}", settings.main_font_small, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 300, screen)
        functions.draw_text(elapsed_time, settings.main_font_small, settings.colors.BLACK, 100, 30, screen, center=False)

        pygame.display.update()

def results(background_color, elapsed_time):
    run = True
    
    try_again_button = Button(text="Try again", 
                             font=settings.main_font_small, 
                             width=200, 
                             height=50, 
                             color=settings.colors.WHITE, 
                             text_color=settings.colors.BLACK, 
                             shadow_color=settings.colors.BLACK, 
                             x=settings.SCREEN_WIDTH/2, 
                             y=250,
                             active=True)
    while run:
        screen.fill(background_color)
        functions.draw_text(elapsed_time, settings.main_font, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 70, screen) 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
        try_again_button.draw(screen)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main_menu()
