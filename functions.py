def draw_text(text, font, text_color, x, y, screen): 
    text_obj = font.render(text, font, text_color)
    text_rect = text_obj.get_rect(center=(x, y))
    screen.blit(text_obj, text_rect)
