def draw_text(text, font, text_color, x, y, screen, center=True): 
    text_obj = font.render(text, font, text_color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    if center:
        text_rect.center = x, y
    screen.blit(text_obj, text_rect)
