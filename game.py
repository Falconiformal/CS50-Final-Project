import pygame

# pygame.locals gives key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# define player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
    # moves sprite with keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        
# initialize
pygame.init()  

# set screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set player
player = Player()

# game loop
running = True

while running:

    for event in pygame.event.get():
        # KEYDOWN event
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # window close
        elif event.type == QUIT:
            running = False

    # record keys pressed
    pressed_keys = pygame.key.get_pressed()

    # update player sprite
    player.update(pressed_keys)

    # background
    screen.fill((0, 0, 0))

    # draw player on screed
    screen.blit(player.surf, player.rect)

    # update display
    pygame.display.flip()

pygame.quit()