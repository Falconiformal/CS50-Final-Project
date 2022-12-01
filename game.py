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
        self.surf = player_frames[pframe].convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(600, 400))
    
    # moves sprite with keypresses
    def update(self, pressed_keys):
        global pframe
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            if pframe in [4, 5, 6]:
                pframe += 1
            else:
                pframe = 4
            player.surf = player_frames[pframe].convert()
            player.surf.set_colorkey((255, 255, 255), RLEACCEL)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            if pframe in [0, 1, 2]:
                pframe += 1
            else:
                pframe = 0
            player.surf = player_frames[pframe].convert()
            player.surf.set_colorkey((255, 255, 255), RLEACCEL)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            if pframe in [12, 13, 14]:
                pframe += 1
            else:
                pframe = 12
            player.surf = player_frames[pframe].convert()
            player.surf.set_colorkey((255, 255, 255), RLEACCEL)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            if pframe in [8, 9, 10]:
                pframe += 1
            else:
                pframe = 8
            player.surf = player_frames[pframe].convert()
            player.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # set screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
# clock setup (framerate)
clock = pygame.time.Clock()

# initialize
pygame.init()

# player animation frames
pframe = 4
player_frames = [
    pygame.image.load('pixilart-frames/pixil-frame-0.png'),
    pygame.image.load('pixilart-frames/pixil-frame-1.png'),
    pygame.image.load('pixilart-frames/pixil-frame-2.png'),
    pygame.image.load('pixilart-frames/pixil-frame-3.png'),
    pygame.image.load('pixilart-frames/pixil-frame-4.png'),
    pygame.image.load('pixilart-frames/pixil-frame-5.png'),
    pygame.image.load('pixilart-frames/pixil-frame-6.png'),
    pygame.image.load('pixilart-frames/pixil-frame-7.png'),
    pygame.image.load('pixilart-frames/pixil-frame-8.png'),
    pygame.image.load('pixilart-frames/pixil-frame-9.png'),
    pygame.image.load('pixilart-frames/pixil-frame-10.png'),
    pygame.image.load('pixilart-frames/pixil-frame-11.png'),
    pygame.image.load('pixilart-frames/pixil-frame-12.png'),
    pygame.image.load('pixilart-frames/pixil-frame-13.png'),
    pygame.image.load('pixilart-frames/pixil-frame-14.png'),
    pygame.image.load('pixilart-frames/pixil-frame-15.png')
]

# set screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set background
bg = pygame.image.load('grasstile.png').convert()
pathmap = [
    pygame.image.load('yardmaps/pixil-frame-0.png').convert(),
    pygame.image.load('yardmaps/pixil-frame-1.png').convert(),
    pygame.image.load('yardmaps/pixil-frame-2.png').convert(),
    pygame.image.load('yardmaps/pixil-frame-3.png').convert(),
    pygame.image.load('yardmaps/pixil-frame-4.png').convert(),
    pygame.image.load('yardmaps/pixil-frame-5.png').convert()
]

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
    
    # iterates through screen width and screen height to set down green grass tiles
    i = 0
    j = 0
    while i < SCREEN_WIDTH:
        while j < SCREEN_HEIGHT:
            screen.blit(bg, (i, j))
            j += bg.get_height()
        j = 0
        i += bg.get_width()

    # lays down six path tiles
    for k in range(3):
        pathmap[k].set_colorkey((255, 255, 255), RLEACCEL)
        pathmap[k + 3].set_colorkey((255, 255, 255), RLEACCEL)
        screen.blit(pathmap[k], (k * pathmap[k].get_width(), 0))
        screen.blit(pathmap[k + 3], (k * pathmap[k].get_width(), pathmap[k].get_height()))


    # draw player on screen
    x = 600
    y = 400
    screen.blit(player.surf, player.rect)

    # update display
    pygame.display.flip()

    # set framerate
    clock.tick(30)

pygame.quit()