import pygame

pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# game loop
run = True
while run:

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

# exit pygame
pygame.quit()
