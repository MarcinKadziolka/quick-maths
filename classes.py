import pygame
from pygame.display import update
import functions
from time import sleep
import settings

# if clicked of enter:
# draw draw down
# when released
# draw up
# execute

#button class
class Button:
    def __init__(self, text, font, width, height, text_color, color, shadow_color, x, y, active=False, function=None, inactive_color=None):
        self.button = pygame.Rect(0, 0, width, height)  
        self.button.center = x, y
        self.shadow = pygame.Rect(0, 0, width, height)
        self.shadow.center = x, y+5
        self.color = color
        self.shadow_color = shadow_color
        self.clicked = False 
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.text_color = text_color
        self.active = active
        self.action = False
        self.function = function
        self.inactive_color = inactive_color

    def draw_down(self, screen):
        color = self.color if self.active else self.inactive_color
        self.button.center = self.x, self.y+5
        pygame.draw.rect(screen, color, self.button, width=0, border_radius=5)

    def draw_up(self, screen):
        color = self.color if self.active else self.inactive_color
        self.button.center = self.x, self.y
        pygame.draw.rect(screen, color, self.button, width=0, border_radius=5)

    def check_clicked(self, event):
        action = False
        pos = pygame.mouse.get_pos()
        if self.button.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                if self.active:
                    self.active = False
                else:
                    self.active = True
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
            self.clicked = False
            action = True


        if self.active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.clicked = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                self.clicked = False 
                action = True
        return action

    def draw(self, screen):
        pygame.draw.rect(screen, self.shadow_color, self.shadow, width=0, border_radius=5)
        if self.clicked:
            self.draw_down(screen)
        else:
            self.draw_up(screen)
        functions.draw_text(text=self.text, text_color=self.text_color, font=self.font, x=self.button.center[0], y=self.button.center[1], screen=screen)
    
    def animate(self, screen):
        self.draw(screen)
        pygame.display.update()
        sleep(settings.SLEEP_DURATION)

    def execute(self):
        if self.function is not None:
            self.function()

class TextField:
    def __init__(self, font, width, height, text_color, active_color, inactive_color, x, y, prompt_text):
        self.active = True
        self.user_input = prompt_text
        self.input_field = pygame.Rect(x, y, width, height)
        self.input_field.center = x, y
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.font = font
       
        self.fast_delete_activation = 500
        self.delete_speed = 50
        self.delete_wait = self.fast_delete_activation

    def get_event(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    self.user_input += event.unicode
                elif event.key == pygame.K_MINUS:
                    self.user_input += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                    self.backspace_timer = pygame.time.get_ticks()

    def update(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.active_color, self.input_field)
        else:
            pygame.draw.rect(screen, self.inactive_color, self.input_field)

        functions.draw_text(self.user_input, self.font, self.text_color, self.input_field.center[0], self.input_field.center[1], screen)

        self.handle_backspace()

    def handle_backspace(self):
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            if pygame.time.get_ticks() - self.backspace_timer > self.delete_wait:
                self.delete_wait = self.delete_speed
                self.backspace_timer = pygame.time.get_ticks()
                self.user_input = self.user_input[:-1]
        else: 
            self.delete_wait = self.fast_delete_activation 
