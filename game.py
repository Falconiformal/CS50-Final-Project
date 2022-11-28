# import and initialize
import pygame
pygame.init()

# game window
screen = pygame.display.set_mode([500, 500])

# run until user quits
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # background
    screen.fill((255, 255, 255))

    # update display
    pygame.display.flip()

pygame.quit()