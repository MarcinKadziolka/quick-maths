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
        on_hover=True,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button = pygame.Rect(0, 0, width, height)
        self.shadow = pygame.Rect(0, 0, width, height)
        self.hitbox = pygame.Rect(0, 0, width, height)
        self.hitbox.center = x, y
        self.button.center = x, y
        self.shadow.center = x, y + 5
        self.border_radius = 5

        self.color = color
        self.shadow_color = shadow_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.current_color = settings.COLORS.GREEN
        self.text = text
        self.font = font

        self.clicked = False
        self.active = active
        self.current = False

        if on_hover:
            self.hover_size = 2
            self.hover_pop = 2
        else:
            self.hover_size = 0
            self.hover_pop = 0

    def set_color(self):
        self.color_to_display = (
            self.current_color
            if self.current
            else self.color
            if self.active
            else self.inactive_color
        )

    def draw_down(self, screen):
        self.button.center = self.x, self.y + 5 - self.hover_pop
        pygame.draw.rect(
            screen,
            self.color_to_display,
            self.button,
            width=0,
            border_radius=self.border_radius,
        )

    def draw_up(self, screen):
        pos = pygame.mouse.get_pos()

        if self.hitbox.collidepoint(pos):
            self.button = pygame.Rect(
                0, 0, self.width + self.hover_size, self.height + self.hover_size
            )
            self.shadow = pygame.Rect(
                0, 0, self.width + self.hover_size, self.height + self.hover_size
            )
            self.button.center = self.x, self.y - self.hover_pop
            self.shadow.center = self.x, self.y + 5  # - self.hover_pop

        else:
            self.button = pygame.Rect(0, 0, self.width, self.height)
            self.shadow = pygame.Rect(0, 0, self.width, self.height)
            self.button.center = self.x, self.y
            self.shadow.center = self.x, self.y + 5

        pygame.draw.rect(
            screen,
            self.shadow_color,
            self.shadow,
            width=0,
            border_radius=self.border_radius,
        )
        pygame.draw.rect(
            screen,
            self.color_to_display,
            self.button,
            width=0,
            border_radius=self.border_radius,
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
        self.set_color()
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


class Layout:
    def __init__(self, layouts):
        self.curr_layout_id = 0
        self.curr_inside_id = 0
        self.layouts = layouts
        self.layouts[0].buttons[0].current = True
        pass


class ButtonLayout:
    def __init__(self, buttons) -> None:
        self.buttons = buttons


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
            half_length = ((self.num_buttons - 1) * distance) / 2
            if mode == "horizontal":
                self.start_x = x - half_length
            elif mode == "vertical":
                self.start_y = y - half_length

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
                self.active_id = i
                for other_button in self.buttons:
                    other_button.active = button == other_button
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
        numeric_only=False,
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

        self.dont_register = [pygame.K_RETURN, pygame.K_BACKSPACE, pygame.K_ESCAPE]
        self.numeric_only = numeric_only

    def get_event(self, event):
        if not self.active or event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
            self.backspace_timer = pygame.time.get_ticks()

        if event.key in self.dont_register:
            return

        if self.numeric_only and event.unicode.isnumeric():
            self.user_input += event.unicode
        else:
            self.user_input += event.unicode

    def update(self, screen):
        color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(screen, color, self.input_field, border_radius=50)

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
