import pygame
import functions
import settings
from enum import Enum
from collections import defaultdict


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
        inactive_color=settings.colors.GRAY,
        current_color=settings.colors.GREEN,
        active_and_current_color=settings.colors.LIGHT_GREEN,
        active=False,
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

        self.active_color = color
        self.shadow_color = shadow_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.current_color = current_color
        self.active_and_current_color = active_and_current_color

        self.text = text
        self.font = font

        self.clicked = False
        self.pressed = False
        self.current = False
        self.active = active

        if on_hover:
            self.hover_size = 2
            self.hover_pop = 2
        else:
            self.hover_size = 0
            self.hover_pop = 0

    def set_color(self):
        self.color_to_display = (
            self.active_and_current_color
            if (self.active and self.current)
            else self.current_color
            if self.current
            else self.active_color
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

    def set_size(self, popup=False):
        size = (
            (self.width + self.hover_size, self.height + self.hover_size)
            if popup
            else (self.width, self.height)
        )
        self.button = pygame.Rect(0, 0, *size)
        self.shadow = pygame.Rect(0, 0, *size)
        self.button.center = (
            (self.x, self.y - self.hover_pop) if popup else (self.x, self.y)
        )
        self.shadow.center = (self.x, self.y + 5) if popup else (self.x, self.y + 5)

    def draw_up(self, screen):
        pos = pygame.mouse.get_pos()
        self.set_size(self.hitbox.collidepoint(pos) or self.current)
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

    def check_clicked(self):
        pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if self.button.collidepoint(pos) and left_click and not self.clicked:
            self.clicked = True
        if left_click == 0 and self.clicked:
            self.clicked = False
            return True
        return False

    def check_pressed(self, event):
        if not self.current:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if not self.pressed:
                self.pressed = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            if self.pressed:
                self.pressed = False
                return True
        return False

    def check_action(self, event):
        return self.check_pressed(event) or self.check_clicked()

    def check_down(self):
        return self.clicked or self.pressed

    def draw(self, screen):
        self.set_color()
        self.draw_down(screen) if self.check_down() else self.draw_up(screen)
        functions.draw_text(
            text=self.text,
            text_color=self.text_color,
            font=self.font,
            x=self.button.center[0],
            y=self.button.center[1],
            screen=screen,
        )


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class ButtonLayout:
    def __init__(self, buttons) -> None:
        if not isinstance(buttons, list):
            raise Exception("Argument provided must a list")
        self.buttons = buttons

    def display(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def update(self, event):
        for button in self.buttons:
            if button.check_clicked():
                button.run()

    def __len__(self):
        return len(self.buttons)


class Navigation:
    def __init__(self, layouts, navigation=defaultdict(lambda: None)):
        self.layout_id = 0
        self.button_id = 0
        self.layouts = layouts
        self.layouts[self.layout_id].buttons[self.button_id].current = True
        self.navigation = navigation

    def get_next_id(self, event):
        curr_layout = self.layouts[self.layout_id]
        n_buttons = len(curr_layout)
        if event.type != pygame.KEYDOWN:
            return
        if target := self.navigation[(self.layout_id, self.button_id, event.key)]:
            self.layout_id, self.button_id = target[0], target[1]
            return
        if event.key in (pygame.K_DOWN, pygame.K_RIGHT):
            if self.button_id + 1 < n_buttons:
                self.button_id += 1
        elif event.key in (pygame.K_UP, pygame.K_LEFT):
            if self.button_id - 1 >= 0:
                self.button_id -= 1

    def update(self, event):
        self.layouts[self.layout_id].buttons[self.button_id].current = False
        self.get_next_id(event)
        self.layouts[self.layout_id].buttons[self.button_id].current = True


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
        orientation=Orientation.VERTICAL,
        inactive_color=settings.colors.GRAY,
    ) -> None:
        self.num_buttons = len(texts)
        self.buttons = []
        self.active_id = active
        self.start_x = x
        self.start_y = y

        if center:
            half_length = ((self.num_buttons - 1) * distance) / 2
            if orientation == Orientation.HORIZONTAL:
                self.start_x = x - half_length
            elif orientation == Orientation.VERTICAL:
                self.start_y = y - half_length
            else:
                raise Exception("Invalid orientation")

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
            if orientation == Orientation.HORIZONTAL:
                self.start_x += distance
            elif orientation == Orientation.VERTICAL:
                self.start_y += distance

    def display(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def update(self, event):
        for i, button in enumerate(self.buttons):
            if button.check_action(event):
                self.active_id = i
                for other_button in self.buttons:
                    other_button.active = button == other_button
                break

    def __len__(self):
        return len(self.buttons)


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
