import settings


def draw_text(text, x, y, screen, center=True, text_color=settings.colors.BLACK, font=settings.main_font_small):
    text_obj = font.render(str(text), font, text_color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    if center:
        text_rect.center = x, y
    screen.blit(text_obj, text_rect)
