import pygame
import functions
from time import sleep
import settings


class Button:
    def __init__(
        self,
        text,
        width,
        height,
        x,
        y,
        font=settings.main_font_small,
        text_color=settings.colors.BLACK,
        color=settings.colors.WHITE,
        shadow_color=settings.colors.BLACK,
        active=False,
        inactive_color=settings.colors.GRAY,
    ):
        self.x = x
        self.y = y
        self.button = pygame.Rect(0, 0, width, height)
        self.shadow = pygame.Rect(0, 0, width, height)
        self.button.center = x, y
        self.shadow.center = x, y + 5
        self.border_radius = 5
        self.color = color
        self.shadow_color = shadow_color
        self.inactive_color = inactive_color
        self.text_color = text_color

        self.text = text
        self.font = font

        self.clicked = False
        self.active = active
        self.action = False

    def draw_down(self, screen):
        color = self.color if self.active else self.inactive_color
        self.button.center = self.x, self.y + 5
        pygame.draw.rect(
            screen, color, self.button, width=0, border_radius=self.border_radius
        )

    def draw_up(self, screen):
        color = self.color if self.active else self.inactive_color
        self.button.center = self.x, self.y
        pygame.draw.rect(
            screen, color, self.button, width=0, border_radius=self.border_radius
        )

    def check_clicked(self, event):
        action = False
        pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if self.button.collidepoint(pos) and left_click and not self.clicked:
            self.clicked = True

        if left_click == 0 and self.clicked:
            self.clicked = False
            action = True

        return action

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.shadow_color,
            self.shadow,
            width=0,
            border_radius=self.border_radius,
        )
        self.draw_down(screen) if self.clicked else self.draw_up(screen)
        functions.draw_text(
            text=self.text,
            text_color=self.text_color,
            font=self.font,
            x=self.button.center[0],
            y=self.button.center[1],
            screen=screen,
        )

    def animate(self, screen):
        self.draw(screen)
        pygame.display.update()
        sleep(settings.SLEEP_DURATION)


class CheckBoxLayout:
    def __init__(
        self,
        texts,
        active,
        height,
        width,
        x,
        y,
        distance,
        center=True,
        mode="vertical",
        inactive_color=settings.colors.GRAY,
    ) -> None:
        self.num_buttons = len(texts)
        self.buttons = []
        self.active_id = active
        self.start_x = x
        self.start_y = y

        if center:
            if mode == "horizontal":
                self.start_x = x - ((self.num_buttons - 1) * distance) / 2
            elif mode == "vertical":
                self.start_y = y - ((self.num_buttons - 1) * distance) / 2

        for i, text in enumerate(texts):
            self.buttons.append(
                Button(
                    text=str(text),
                    width=width,
                    height=height,
                    x=self.start_x,
                    y=self.start_y,
                    active=(i == active),
                    inactive_color=inactive_color,
                )
            )
            if mode == "horizontal":
                self.start_x += distance
            else:
                self.start_y += distance

    def display(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def update(self, event):
        for i, button in enumerate(self.buttons):
            if button.check_clicked(event):
                for j, button in enumerate(self.buttons):
                    if i == j:
                        button.active = True
                        self.active_id = i
                    else:
                        button.active = False
                break


class TextField:
    def __init__(
        self,
        font,
        width,
        height,
        text_color,
        active_color,
        inactive_color,
        x,
        y,
        prompt_text,
    ):
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
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    pass
                elif event.key == pygame.K_ESCAPE:
                    pass
                else:
                    self.user_input += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                    self.backspace_timer = pygame.time.get_ticks()

    def update(self, screen):
        if self.active:
            pygame.draw.rect(
                screen, self.active_color, self.input_field, border_radius=50
            )
        else:
            pygame.draw.rect(
                screen, self.inactive_color, self.input_field, border_radius=50
            )

        functions.draw_text(
            text=self.user_input,
            font=self.font,
            text_color=self.text_color,
            x=self.input_field.center[0],
            y=self.input_field.center[1],
            screen=screen,
        )

        self.handle_backspace()

    def handle_backspace(self):
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            if pygame.time.get_ticks() - self.backspace_timer > self.delete_wait:
                self.delete_wait = self.delete_speed
                self.backspace_timer = pygame.time.get_ticks()
                self.user_input = self.user_input[:-1]
        else:
            self.delete_wait = self.fast_delete_activation
