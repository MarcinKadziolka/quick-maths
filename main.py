import pygame
import settings
import functions
from classes import Button, TextField
import random
from time import sleep
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
    x = random.randint(0, 10)
    y = random.randint(0, 10)
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
    show_result_color = 100
    while run:
        if pygame.time.get_ticks() - last_answer_time < show_result_color:
            screen.fill(background_color)
        else:
            screen.fill(settings.colors.BACKGROUND)

        functions.draw_text("Game", settings.main_font, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 70, screen) 
        for event in pygame.event.get():
            input_field.get_event(event)
            
            # Because it sometimes triggers to fast, we wait some miliseconds
            if pygame.time.get_ticks() - last_answer_time > 100:
                if answer_button.check_clicked(event):
                    if check_equation(input_field.user_input, current_equation[-1]):
                        background_color = settings.colors.LIGHT_GREEN
                        try:
                            current_equation = next(equations)
                        except StopIteration as e:
                            results()
                    else:
                        background_color = settings.colors.LIGHT_RED
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

        pygame.display.update()

def results():
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
        screen.fill(settings.colors.BACKGROUND)
        functions.draw_text("Results", settings.main_font, settings.colors.BLACK, settings.SCREEN_WIDTH/2, 70, screen) 
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
