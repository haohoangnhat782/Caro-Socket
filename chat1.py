import pygame
import sys
from unidecode import unidecode

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("")

font = pygame.font.Font("font/times-new-roman-14.ttf", 36)
input_text = ''

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                print("Entered:", unidecode(input_text))
                input_text = ''
            else:

                if len(input_text) < 14:
                    input_text += unidecode(event.unicode)
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (50, 50, 300, 100), 1)
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (55, 55))

    pygame.display.flip()
    clock.tick(60)
