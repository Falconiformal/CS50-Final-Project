import pygame

# pygame.locals gives key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# window dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# define player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(player_frames[4]).convert()
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(600, 400))
    
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
        # set screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# player animation frames
player_frames = [
    'pixilart-frames/pixil-frame-0.png',
    'pixilart-frames/pixil-frame-1.png',
    'pixilart-frames/pixil-frame-2.png',
    'pixilart-frames/pixil-frame-3.png',
    'pixilart-frames/pixil-frame-4.png',
    'pixilart-frames/pixil-frame-5.png',
    'pixilart-frames/pixil-frame-6.png',
    'pixilart-frames/pixil-frame-7.png',
    'pixilart-frames/pixil-frame-8.png',
    'pixilart-frames/pixil-frame-9.png',
    'pixilart-frames/pixil-frame-10.png',
    'pixilart-frames/pixil-frame-11.png',
    'pixilart-frames/pixil-frame-12.png',
    'pixilart-frames/pixil-frame-13.png',
    'pixilart-frames/pixil-frame-14.png',
    'pixilart-frames/pixil-frame-15.png'
    ]
            
# clock setup (framerate)
clock = pygame.time.Clock()

# initialize
pygame.init()  

# set screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set background
bg = pygame.image.load('grasstile.png').convert()

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
   
    i = 0
    j = 0
    while i < SCREEN_WIDTH:
        while j < SCREEN_HEIGHT:
            screen.blit(bg, (i, j))
            j += bg.get_height()
        j = 0
        i += bg.get_width()

    # draw player on screen
    x = 600
    y = 400
    screen.blit(player.surf, player.rect)

    # update display
    pygame.display.flip()

    # set framerate
    clock.tick(30)

pygame.quit()