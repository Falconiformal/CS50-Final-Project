import pygame
import random

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
        # set screen boundaries; player sprite image has extra border space, numbers here adjust for that buffer
        if self.rect.left < -30:
            self.rect.left = -30
        if self.rect.right > SCREEN_WIDTH + 35:
            self.rect.right = SCREEN_WIDTH + 35
        if self.rect.top <= -10:
            self.rect.top = -10
        if self.rect.bottom >= SCREEN_HEIGHT + 10:
            self.rect.bottom = SCREEN_HEIGHT + 10
        # player hitbox
        self.hitbox = pygame.Rect(self.rect.left + 35, self.rect.top + 50, 25, 40)
        # building collisions
        for building in buildings:
            if pygame.Rect.colliderect(self.hitbox, building.rect):
                if self.hitbox.left + 5 >= building.rect.right:
                    self.rect.left = building.rect.right - 35
                elif self.hitbox.right - 5 <= building.rect.left:
                    self.rect.right = building.rect.left + 40
                elif self.hitbox.top + 5 >= building.rect.bottom:
                    self.rect.top = building.rect.bottom - 50
                elif self.hitbox.bottom - 5 <= building.rect.top:
                    self.rect.bottom = building.rect.top + 10
            
# define building class
class Building(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super(Building, self).__init__()
        self.surf = pygame.image.load(name).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y)) # these would need to be the real locations of the buildings
        

# define tourist class
class Tourist(pygame.sprite.Sprite):
    def __init__(self):
        super(Tourist, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        
        sides = [
            (random.randint(1, SCREEN_WIDTH - 1), 1),
            (random.randint(1, SCREEN_WIDTH - 1), SCREEN_HEIGHT - 1),
            (1, random.randint(1, SCREEN_HEIGHT - 1)),
            (SCREEN_WIDTH - 1, random.randint(1, SCREEN_HEIGHT - 1))
        ]

        self.rect = self.surf.get_rect(
            center=(
                sides[random.randint(0, 3)]
            ) # these would set random locations for the tourists along edges
        )

    def update(self):

        while True:
            self.speedx = random.randint(-20, 20)
            self.speedy = random.randint(-20, 20)

            if self.speedx != 0 or self.speedy != 0:
                break
        self.rect.move_ip(self.speedx, self.speedy) # random motion

        if self.rect.right > SCREEN_WIDTH or self.rect.right < 0 or self.rect.top < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

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

# building skins and locations
building_list = {
    'Grays': ['buildings/grays.png', 1132, 322],
    'Stoughton': ['buildings/stoughton.png', 170, 518],
    'Hollis': ['buildings/stoughton.png', 386, 518]
}

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

# creates event to add tourist
ADDTOURIST = pygame.USEREVENT + 1
pygame.time.set_timer(ADDTOURIST, 250) # adds 4 tourists every second


# create sprite groups
buildings = pygame.sprite.Group()
tourists = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# create buildings
for building in building_list:
    new_building = Building(building_list[building][0], building_list[building][1], building_list[building][2])
    buildings.add(new_building)
    all_sprites.add(new_building)

# add player to sprite group after buildings
all_sprites.add(player)
    
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
        # add tourist
        elif event.type == ADDTOURIST:
            new_tourist = Tourist()
            tourists.add(new_tourist)
            all_sprites.add(new_tourist)

    # record keys pressed
    pressed_keys = pygame.key.get_pressed()

    # update player sprite
    player.update(pressed_keys)

    # update tourist
    tourists.update()

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


    # draw player, buildings, tourists on screen
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    # update display
    pygame.display.flip()

    # set framerate
    clock.tick(30)

pygame.quit()