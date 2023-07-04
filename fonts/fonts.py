import pygame
import settings
import functions

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 920
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fonts")

all_fonts = pygame.font.get_fonts()
total_fonts = len(all_fonts)
print(all_fonts)

def main_menu():
    run = True
    font_index = 0
    while run:
        screen.fill(settings.colors.WHITE)
        functions.draw_text("Lorem ipsum dolor sit amet", pygame.font.SysFont(all_fonts[font_index], 60), settings.colors.BLACK, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-100, screen) 
        functions.draw_text(f"{font_index}/{total_fonts-1} {all_fonts[font_index]}", pygame.font.SysFont(all_fonts[font_index], 60), settings.colors.BLACK, SCREEN_WIDTH/2, SCREEN_HEIGHT/2+100, screen) 

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_LEFT:
                    font_index -= 1
                    if font_index < 0:
                        font_index = total_fonts-1
                if event.key == pygame.K_RIGHT:
                    font_index += 1
                    if font_index >= total_fonts:
                        font_index = 0

            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
