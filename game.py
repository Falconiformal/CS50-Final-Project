from enum import Enum
import pygame
import pygame.freetype
from pygame.rect import Rect
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

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1

# window dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# clock setup (framerate)
clock = pygame.time.Clock()

# following UI text code from tutorial (https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html)
def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(pygame.sprite.Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
        """
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        # calls the init method of the parent sprite class
        super().__init__()

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates text appearance if mouse hover and returns action with click """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)


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
    'Hollis': ['buildings/stoughton.png', 386, 518],
    'Thayer': ['buildings/thayer.png', 274, 70],
    'University Hall': ['buildings/universityhall.png', 624, 128],
    'Mower': ['buildings/mower.png', 168, 732],
    'Lionel': ['buildings/mower.png', 388, 732],
    'Holworthy': ['buildings/holworthy.png', 54, 328],
    'Weld': ['buildings/weld.png', 922, 78],
    'Phillips Brooks House': ['buildings/phillipsbrooks.png', 46, 626],
    'Holden Chapel': ['buildings/holdenchapel.png', 278, 658],
    'Harvard Hall': ['buildings/harvardhall.png', 520, 632],
    'Massachusetts Hall': ['buildings/masshall.png', 748, 616],
    'Johnston Gate House': ['buildings/gatehouse.png', 614, 702],
    'Matthews': ['buildings/matthews.png', 942, 512],
    'Straus': ['buildings/straus.png', 948, 702]
}


# define player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = player_frames[pframe].convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(600, 400))

        
    # moves sprite with keypresses
    def update(self, pressed_keys, buildings):
        global pframe
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            if pframe in [4, 5, 6]:
                pframe += 1
            else:
                pframe = 4
            self.surf = player_frames[pframe].convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            if pframe in [0, 1, 2]:
                pframe += 1
            else:
                pframe = 0
            self.surf = player_frames[pframe].convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            if pframe in [12, 13, 14]:
                pframe += 1
            else:
                pframe = 12
            self.surf = player_frames[pframe].convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            if pframe in [8, 9, 10]:
                pframe += 1
            else:
                pframe = 8
            self.surf = player_frames[pframe].convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # set screen boundaries; player sprite image has extra border space, numbers here adjust for that buffer
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        # player hitbox
        self.hitbox = Rect(self.rect.left + 10, self.rect.top + 40, 16, 40)
        # building collisions
        for building in buildings:
            if Rect.colliderect(self.hitbox, building.rect):
                if self.hitbox.left + 5 >= building.rect.right:
                    self.rect.left = building.rect.right - 10
                elif self.hitbox.right - 5 <= building.rect.left:
                    self.rect.right = building.rect.left + 10
                elif self.hitbox.top + 5 >= building.rect.bottom:
                    self.rect.top = building.rect.bottom - 40
                elif self.hitbox.bottom - 5 <= building.rect.top:
                    self.rect.bottom = building.rect.top
        
                    
# define building class
class Building(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super(Building, self).__init__()
        self.surf = pygame.image.load(name).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y)) # the locations of the buildings
        

# define tourist class
class Tourist(pygame.sprite.Sprite):
    def __init__(self):
        super(Tourist, self).__init__()
        # tourist frames
        tourist_frames = [
        pygame.image.load('tourists/tourist0.png'),
        pygame.image.load('tourists/tourist1.png'),
        pygame.image.load('tourists/tourist2.png')
        ]
        
        pickframe = random.randint(0, 2)
        self.surf = tourist_frames[pickframe]
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.speedx = random.randint(-5, 5)
        self.speedy = random.randint(-5, 5)
        
        sides = [
            [(random.randint(1, SCREEN_WIDTH - 1), 1), random.randint(-5, 5), random.randint(1, 5)],
            [(random.randint(1, SCREEN_WIDTH - 1), SCREEN_HEIGHT - 1), random.randint(-5, 5), random.randint(-5, -1)],
            [(1, random.randint(1, SCREEN_HEIGHT - 1)), random.randint(1, 5), random.randint(-5, 5)],
            [(SCREEN_WIDTH - 1, random.randint(1, SCREEN_HEIGHT - 1)), random.randint(-5, -1), random.randint(-5, 5)]
        ]

        pickSide = random.randint(0, 3)
        self.rect = self.surf.get_rect(
            center=(
                sides[pickSide][0]
            ) # these would set random locations for the tourists along edges
        )

        self.speedx = sides[pickSide][1]
        self.speedy = sides[pickSide][2]


    def update(self, buildings):
        if random.randint(0, 10) == 5:
            while True:
                self.speedx = random.randint(-5, 5)
                self.speedy = random.randint(-5, 5)

                if self.speedx != 0 or self.speedy != 0:
                    break

        self.rect.move_ip(self.speedx, self.speedy) # random motion

        if pygame.sprite.spritecollideany(self, buildings):
            self.rect.move_ip(-self.speedx, -self.speedy) # reverse direction

        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


# game loop adapted from (https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html)
def main():
    # initialize
    pygame.init()

    # set screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

        
def title_screen(screen):
    start_btn = UIElement(
        center_position=(600, 400),
        font_size=30,
        bg_rgb=(0, 0, 0),
        text_rgb=(255, 255, 255),
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(600, 500),
        font_size=30,
        bg_rgb=(0, 0, 0),
        text_rgb=(255, 255, 255),
        text="Quit",
        action=GameState.QUIT
    )

    buttons = [start_btn, quit_btn]

    # main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            
            screen.fill((0, 0, 0))

            # KEYDOWN event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return GameState.QUIT
            # window close
            elif event.type == QUIT:
                return GameState.QUIT

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

     
def play_level(screen):
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
    pygame.time.set_timer(ADDTOURIST, 200) # adds 5 tourists every second

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
    while True:

        for event in pygame.event.get():
            # KEYDOWN event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return GameState.QUIT
            # window close
            elif event.type == QUIT:
                return GameState.QUIT
            # add tourist
            elif event.type == ADDTOURIST:
                new_tourist = Tourist()
                tourists.add(new_tourist)
                all_sprites.add(new_tourist)

        # record keys pressed
        pressed_keys = pygame.key.get_pressed()

        # update player sprite
        player.update(pressed_keys, buildings)

        # update tourist
        tourists.update(buildings)

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

main()