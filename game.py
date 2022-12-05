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
    GAMEOVER = -3
    CREDITS = -2
    TITLE = -1
    QUIT = 0
    NEWGAME = 1

# window dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# color library
WHITE = (255, 255, 255)
CRIMSON = (99, 0, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# clock setup (framerate)
clock = pygame.time.Clock()
time = 0

# score
score = 300

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
building_list = [
    ['Grays', 'buildings/grays.png', (1132,322), (1075,322)],
    ['Stoughton', 'buildings/stoughton.png', (170,518), (170,465)],
    ['Hollis', 'buildings/stoughton.png', (386,518), (386,465)],
    ['Thayer', 'buildings/thayer.png', (274,70), (272,135)],
    ['University Hall', 'buildings/universityhall.png', (624,128), (681,195)],
    ['Mower', 'buildings/mower.png', (168,732), (168,687)],
    ['Lionel', 'buildings/mower.png', (388,732), (388,687)],
    ['Holworthy', 'buildings/holworthy.png', (54,328), (100,328)],
    ['Weld', 'buildings/weld.png', (922,78), (922,155)],
    ['Phillips Brooks House', 'buildings/phillipsbrooks.png', (46,626), (100,626)],
    ['Holden Chapel', 'buildings/holdenchapel.png', (278,658), (278,605)],
    ['Harvard Hall', 'buildings/harvardhall.png', (520,632), (576,632)],
    ['Massachusetts Hall', 'buildings/masshall.png', (748,616), (698,574)],
    ['Johnston Gate House', 'buildings/gatehouse.png', (614,702), (632,702)],
    ['Matthews', 'buildings/matthews.png', (942,512), (942,456)],
    ['Straus', 'buildings/straus.png', (948,702), (948,662)],
    ['John Harvard Statue', 'buildings/johnharvard.png', (624,175), (624,220)]
]

# target locations
locations = [
    'Harvard Yard Operations (Yard Ops)',
    'Phillips Brooks House',
    'Harvard Foundation for Intercultural and Race Relations',
    'Office of BGLTQ Student Life (QuOffice)'
]

# checkpoint info list
infoqueue = []
subtraction = []


def create_border_surface(text_rect, padding):
    """ Creates border around text """
    return Rect((text_rect.left - padding), (text_rect.top - padding), (text_rect.width + (padding * 2)), (text_rect.height + (padding * 2)))


# following UI text code from tutorial (https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html)
def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert()


class UIElement(pygame.sprite.Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, padding, border_radius, action=None):
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
        self.padding = padding
        self.bg_rgb = bg_rgb
        self.border_radius = border_radius

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
        border = create_border_surface(self.rect, self.padding)
        pygame.draw.rect(surface, self.bg_rgb, border, border_radius=self.border_radius)
        surface.blit(self.image, self.rect)


# define player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = player_frames[pframe].convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center=(600, 400))
        #self.tracker = 0

    def show_point_deduction(self, points, state):
        ''' Visuals for point deduction '''
        self.bye_points = create_surface_with_text(points, 13, RED, WHITE)
        self.bye_points.set_colorkey(WHITE, RLEACCEL)
        self.bye_rect = self.bye_points.get_rect(center=(self.rect.centerx, self.rect.centery - 50))

        if state == 1:
            subtraction.append([self.bye_points, self.bye_rect])
        elif state == 0:
            subtraction.clear()

        
    # moves sprite with keypresses
    def update(self, pressed_keys, buildings, tourists):
        global score
        global pframe
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            if pframe in [4, 5, 6]:
                pframe += 1
            else:
                pframe = 4
            self.surf = player_frames[pframe].convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            if pframe in [0, 1, 2]:
                pframe += 1
            else:
                pframe = 0
            self.surf = player_frames[pframe].convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            if pframe in [12, 13, 14]:
                pframe += 1
            else:
                pframe = 12
            self.surf = player_frames[pframe].convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            if pframe in [8, 9, 10]:
                pframe += 1
            else:
                pframe = 8
            self.surf = player_frames[pframe].convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
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
        self.hitbox = Rect(self.rect.left + 10, self.rect.top + 50, 16, 30)
        # building collisions
        for building in buildings:
            if Rect.colliderect(self.hitbox, building.rect):
                if self.hitbox.left + 5 >= building.rect.right:
                    self.rect.left = building.rect.right - 10
                if self.hitbox.right - 5 <= building.rect.left:
                    self.rect.right = building.rect.left + 10
                if self.hitbox.top + 5 >= building.rect.bottom:
                    self.rect.top = building.rect.bottom - 50
                if self.hitbox.bottom - 5 <= building.rect.top:
                    self.rect.bottom = building.rect.top
        
        # tourist collisions
        for tourist in tourists:
            if Rect.colliderect(self.rect, tourist.rect):
                if self.rect.left + 5 >= tourist.rect.right:
                    self.rect.left = tourist.rect.right
                elif self.rect.right - 5 <= tourist.rect.left:
                    self.rect.right = tourist.rect.left
                elif self.rect.top + 5 >= tourist.rect.bottom:
                    self.rect.top = tourist.rect.bottom
                elif self.rect.bottom - 5 <= tourist.rect.top:
                    self.rect.bottom = tourist.rect.top

                    
# define building class
class Building(pygame.sprite.Sprite):
    def __init__(self, file, xy):
        super(Building, self).__init__()
        self.surf = pygame.image.load(file).convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center=(xy)) # the locations of the buildings

        
# define building checkpoint class
class Building_checkpoint(pygame.sprite.Sprite):
    def __init__(self, name, xy):
        super(Building_checkpoint, self).__init__()
        self.surf = pygame.image.load('buildings/checkpoint.png').convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center=(xy)) # the locations of the checkpoints
        self.info = create_surface_with_text(name, 12, WHITE, CRIMSON)
        self.info_rect = self.info.get_rect(center=xy)
        self.border = create_border_surface(self.info_rect, 4)
        self.tracker = 0

    def update(self, player, infoqueue):
        if Rect.colliderect(self.rect, player.hitbox):
            self.tracker += 1
        elif self.tracker != 0:
            # leaves checkpoint
            self.tracker = 0
            infoqueue.clear()
      
        if self.tracker == 1:
            # checkpoint first contact
            infoqueue.append([self.info, self.info_rect, self.border])


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
        self.surf.set_colorkey(WHITE, RLEACCEL)

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

        self.tracker = 0


    def update(self, buildings, player):
        global score
        if random.randint(0, 10) == 5:
            while True:
                self.speedx = random.randint(-5, 5)
                self.speedy = random.randint(-5, 5)

                if self.speedx != 0 or self.speedy != 0:
                    break

        self.rect.move_ip(self.speedx, self.speedy) # random motion

        if pygame.sprite.spritecollideany(self, buildings):
            self.rect.move_ip(-self.speedx, -self.speedy) # reverse direction

        if pygame.sprite.collide_rect(self, player):
            self.rect.move_ip(-self.speedx, -self.speedy) # reverse direction
            self.tracker += 1
        elif self.tracker != 0:
            self.tracker = 0
            player.show_point_deduction('-20', self.tracker)
        
        if self.tracker == 1:
            score = score - 20
            player.show_point_deduction('-20', self.tracker)

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

        if game_state == GameState.CREDITS:
            game_state = credits_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen)

        if game_state == GameState.GAMEOVER:
            game_state = end_screen(screen)
        
        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):
    play_btn = UIElement(
        center_position=(600, 300),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text="Play",
        padding = 16,
        border_radius = 4,
        action=GameState.NEWGAME,
    )
    credits_btn = UIElement(
        center_position=(600, 400),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text="Credits",
        padding = 20,
        border_radius = 4,
        action=GameState.CREDITS
    )
    quit_btn = UIElement(
        center_position=(600, 500),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text="Quit",
        padding = 16,
        border_radius = 4,
        action=GameState.QUIT
    )

    buttons = [play_btn, credits_btn, quit_btn]
    bg = pygame.image.load('homebg.png').convert()

    # main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            
            screen.fill(CRIMSON)
            screen.blit(bg, (0,0))

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


def credits_screen(screen):
    home_btn = UIElement(
        center_position=(600, 500),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text="Home",
        padding = 16,
        border_radius = 4,
        action=GameState.TITLE,
    )

    buttons = [home_btn]
    #credits_a = create_surface_with_text('A game by Elisabeth Ngo and Adam Wang')
    #credits_b = create_surface_with_text('Created December, 2022 for Harvard CS50')

    # main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            
            screen.fill(CRIMSON)

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
        
        
def end_screen(screen):
    play_btn = UIElement(
        center_position=(600, 300),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text="Play again",
        padding = 16,
        border_radius = 4,
        action=GameState.NEWGAME,
    )
    home_btn = UIElement(
        center_position=(600, 400),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text="Home",
        padding = 16,
        border_radius = 4,
        action=GameState.TITLE,
    )
    quit_btn = UIElement(
        center_position=(600, 500),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text="Quit",
        padding = 8,
        border_radius = 4,
        action=GameState.QUIT
    )

    buttons = [play_btn, home_btn, quit_btn]

    # main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            
            screen.fill(CRIMSON)

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
    checkpoints = pygame.sprite.Group()
    tourists = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # create buildings and checkpoints
    for building in building_list:
        new_building = Building(building[1], building[2])
        new_checkpoint = Building_checkpoint(building[0], building[3])
        buildings.add(new_building)
        all_sprites.add(new_building)
        checkpoints.add(new_checkpoint)
        all_sprites.add(new_checkpoint)

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
        player.update(pressed_keys, buildings, tourists)

        # update checkpoints to display info
        checkpoints.update(player, infoqueue)

        # update tourist
        tourists.update(buildings, player)

        # background
        screen.fill(BLACK)
        
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
            pathmap[k].set_colorkey(WHITE, RLEACCEL)
            pathmap[k + 3].set_colorkey(WHITE, RLEACCEL)
            screen.blit(pathmap[k], (k * pathmap[k].get_width(), 0))
            screen.blit(pathmap[k + 3], (k * pathmap[k].get_width(), pathmap[k].get_height()))

        # draw player, buildings, tourists on screen
        for sprite in all_sprites:
            screen.blit(sprite.surf, sprite.rect)

        # draw info labels
        for info in infoqueue:
            pygame.draw.rect(screen, CRIMSON, info[2], border_radius = 4)
            screen.blit(info[0], info[1])
        
        for points in subtraction:
            screen.blit(points[0], points[1])

        # display score
        global score
        scoretext = 'Score: ' + str(score)
        scoredisplay = create_surface_with_text(scoretext, 18, WHITE, CRIMSON)
        score_rect = scoredisplay.get_rect(center=(1100,20))
        border = create_border_surface(score_rect, 6)
        pygame.draw.rect(screen, CRIMSON, border, border_radius = 6)
        screen.blit(scoredisplay, score_rect)

        # update display
        pygame.display.flip()

        # set framerate
        clock.tick(30)
        global time
        time += 1
        if time % 6 == 0:
            score -= 1

main()