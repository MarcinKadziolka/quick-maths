import settings


def draw_text(text, x, y, screen, center=True, text_color=settings.colors.BLACK, font=settings.main_font_small):
    text_obj = font.render(str(text), font, text_color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    if center:
        text_rect.center = x, y
    screen.blit(text_obj, text_rect)


def select_category_id(cursor, operation, digit, amount):
    category_name = f"{operation}_digits_{digit}_amount_{amount}"
    cursor.execute(
        "SELECT category_id FROM category WHERE name=?",
        (category_name,),
    )
    return cursor.fetchone()[0]
