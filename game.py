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
    HOME = -1
    QUIT = 0
    NEWGAME = 1
    WIN = 2
    INSTRUCTIONS = 3

# window dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# color library
WHITE = (255, 255, 255)
CRIMSON = (99, 0, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# tourists per second
TPS = 10
# starting score
SCORE = 300
# objectives
OBJECTIVES = 5

# sound setup
pygame.mixer.init()
# Sound Source: Mixkit
# https://mixkit.co/free-sound-effects/hurt/
collision_sound = pygame.mixer.Sound('sounds/mixkit_ow.wav')
# https://mixkit.co/free-sound-effects/win/
checkpoint_sound = pygame.mixer.Sound('sounds/mixkit_retro_game_notification.wav')
# https://mixkit.co/free-sound-effects/click/
button_sound = pygame.mixer.Sound('sounds/mixkit_typewriter_soft_click.wav')
# https://mixkit.co/free-sound-effects/win/
win_sound = pygame.mixer.Sound('sounds/mixkit_video_game_win.wav')
# https://mixkit.co/free-sound-effects/game-over/
lose_sound = pygame.mixer.Sound('sounds/mixkit_retro_arcade_game_over.wav')

# clock setup (framerate)
clock = pygame.time.Clock()
time = 0

# score
score = SCORE

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
    ['Harvard Yard Operations (Yard Ops)', 'Weld'],
    ['The Phillips Brooks House Association', 'Phillips Brooks House'],
    ['The Harvard Foundation for Intercultural and Race Relations', 'Grays'],
    ['The Office of BGLTQ Student Life (QuOffice)', 'Thayer'],
    ['Holden Chapel', 'Holden Chapel']
]

# target order
targets = []

# checkpoint info list
infoqueue = []

# checkpoint update list
checkedpoints = []

# deduction visual
subtraction = []


def create_border_surface(text_rect, padding):
    """ Creates border around text """
    return Rect((text_rect.left - padding), (text_rect.top - padding), (text_rect.width + (padding * 2)), (text_rect.height + (padding * 2)))


# Following UI text code from tutorial: 
# Barthaud, Danny. (2019, September 12). "Handling a title screen, game flow and buttons in pygame." Programming Pixels.
# https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont('Courier', font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert()

# Following UI text code from tutorial: 
# Barthaud, Danny. (2019, September 12). "Handling a title screen, game flow and buttons in pygame." Programming Pixels.
# https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
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

        self.borders = [
            create_border_surface(self.rects[0], self.padding),
            create_border_surface(self.rects[1], self.padding)
        ]

        # calls the init method of the parent sprite class
        super().__init__()

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
    
    @property
    def border(self):
        return self.borders[1] if self.mouse_over else self.borders[0]
    
    def update(self, mouse_pos, mouse_up):
        """ Updates text appearance if mouse hover and returns action with click """
        if self.border.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        pygame.draw.rect(surface, self.bg_rgb, self.border, border_radius=self.border_radius)
        surface.blit(self.image, self.rect)


# define player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = player_frames[pframe].convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center=(600, 400))

    def show_point_deduction(self, points, state):
        """ Visuals for point deduction """
        self.bye_points = create_surface_with_text(points, 13, RED, WHITE)
        self.bye_points.set_colorkey(WHITE, RLEACCEL)
        self.bye_rect = self.bye_points.get_rect(center=(self.rect.centerx, self.rect.centery - 50))

        if state == 1:
            subtraction.append([self.bye_points, self.bye_rect])
        elif state == 0:
            subtraction.clear()

        
    # moves sprite with keypresses
    def update(self, pressed_keys, buildings, tourists):
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
        self.name = name
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
            infoqueue.append([self.info, self.info_rect, self.border, self.name])


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
            ) # these set random locations for the tourists along edges
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
            collision_sound.play()
        
        if self.tracker == 1:
            score = score - 20
            player.show_point_deduction('-20', self.tracker)
            collision_sound.play()

        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Game loop adapted from: 
# Barthaud, Danny. (2019, September 12). "Handling a title screen, game flow and buttons in pygame." Programming Pixels.
# https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
def main():
    # initialize
    pygame.init()

    # set screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_state = GameState.HOME

    while True:
        if game_state == GameState.HOME:
            game_state = home_screen(screen)

        if game_state == GameState.CREDITS:
            game_state = credits_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen)
        
        if game_state == GameState.WIN:
            game_state = win_screen(screen)

        if game_state == GameState.GAMEOVER:
            game_state = end_screen(screen)
        
        if game_state == GameState.INSTRUCTIONS:
            game_state = instructions_screen(screen)
        
        if game_state == GameState.QUIT:
            pygame.quit()
            return


def home_screen(screen):
    play_btn = UIElement(
        center_position=(600, 300),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Play',
        padding = 16,
        border_radius = 8,
        action=GameState.NEWGAME,
    )
    instructions_btn = UIElement(
        center_position=(600, 400),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Instructions',
        padding = 20,
        border_radius = 8,
        action=GameState.INSTRUCTIONS
    )
    credits_btn = UIElement(
        center_position=(600, 500),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Credits',
        padding = 20,
        border_radius = 8,
        action=GameState.CREDITS
    )
    quit_btn = UIElement(
        center_position=(600, 600),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Quit',
        padding = 16,
        border_radius = 8,
        action=GameState.QUIT
    )

    buttons = [play_btn, instructions_btn, credits_btn, quit_btn]
    
    bg = pygame.image.load('backgrounds/homebg.png').convert()
    screen.fill(BLACK)

    # Music Source: Square Foot Ocean by Martijn de Boer (NiGiD) (c) copyright 2022 
    # Music License: Licensed under a Creative Commons Attribution Noncommercial  (3.0) license.
    # http://dig.ccmixter.org/files/NiGiD/65334 
    pygame.mixer.music.load('sounds/NiGiD_Square_Foot_Ocean.mp3')
    pygame.mixer.music.play(loops=-1)

    # main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

            # KEYDOWN event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return GameState.QUIT
            # window close
            elif event.type == QUIT:
                return GameState.QUIT
        
        screen.blit(bg, (0,0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                button_sound.play()
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def credits_screen(screen):
    credits_height = SCREEN_HEIGHT + 400
    counter = 0
    scrolly_top = SCREEN_HEIGHT
    

    home_btn = pygame.image.load('buttons/home_btn.png').convert()
    home_btn.set_colorkey(BLACK, RLEACCEL)
    highlight_btn = pygame.image.load('buttons/home_btn_hover.png').convert()
    highlight_btn.set_colorkey(BLACK, RLEACCEL)
    home_rect = home_btn.get_rect(center=(30,30))
    highlight_rect = highlight_btn.get_rect(center=(30,30))
    
    bg = pygame.image.load('backgrounds/creditsbg.png').convert()
    screen.fill(BLACK)
    
    credits = [
        [create_surface_with_text('CAMPUS CROSSER', 40, WHITE, BLACK), 60],
        [create_surface_with_text('A game by Elisabeth Ngo and Adam Wang', 25, WHITE, BLACK), 120],
        [create_surface_with_text('MUSIC', 25, WHITE, BLACK), 260],
        [create_surface_with_text('Square Foot Ocean', 20, WHITE, BLACK), 315],
        [create_surface_with_text('Martijn de Boer (NiGiD) (c) copyright 2022', 15, WHITE, BLACK), 340],
        [create_surface_with_text('Creative Commons Attribution', 15, WHITE, BLACK), 360],
        [create_surface_with_text('Noncommercial (3.0) license', 15, WHITE, BLACK), 380],
        [create_surface_with_text('Floating Through Time (SAW mix)', 20, WHITE, BLACK), 435],
        [create_surface_with_text('stellarartwars (c) copyright 2016', 15, WHITE, BLACK), 460],
        [create_surface_with_text('Created December, 2022 for Harvard CS50', 15, WHITE, BLACK), 480],
        [create_surface_with_text('Creative Commons Attribution', 15, WHITE, BLACK), 500],
        [create_surface_with_text('Noncommercial (3.0) license', 15, WHITE, BLACK), 520],
        [create_surface_with_text('Sound effects from Mixkit', 20, WHITE, BLACK), 600],
        [create_surface_with_text('Some code adapted from tutorials (see source code)', 20, WHITE, BLACK), 680],
        [create_surface_with_text('ABOUT US', 25, WHITE, BLACK), 780],
        [create_surface_with_text('Elisabeth Ngo', 20, WHITE, BLACK), 835],
        [create_surface_with_text('Harvard Class of 2026, I live in Stoughton Hall', 15, WHITE, BLACK), 860],
        [create_surface_with_text('Unsure of what I will concentrate in', 15, WHITE, BLACK), 880],
        [create_surface_with_text('Adam Wang', 20, WHITE, BLACK), 935],
        [create_surface_with_text('Harvard Class of 2026, I live in Grays Hall', 15, WHITE, BLACK), 960],
        [create_surface_with_text('Potential engineering concentrator', 15, WHITE, BLACK), 980],
        [create_surface_with_text('Created December, 2022 for Harvard CS50', 20, WHITE, BLACK), 1150]
    ]
    
    # main loop
    while True:
        mouse_up = False
        counter += 1

        if scrolly_top < -200 - credits_height:
            return GameState.HOME

        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

            # KEYDOWN event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return GameState.QUIT
            # window close
            elif event.type == QUIT:
                return GameState.QUIT
        
        screen.blit(bg, (0,0))

        credits_rect = (250, scrolly_top, 700, credits_height)
        pygame.draw.rect(screen, CRIMSON, credits_rect)
        
        if counter % 8 == 0:
            scrolly_top -= 1
        
        for credit in credits:
            credit[0].set_colorkey((BLACK), RLEACCEL)
            placement = scrolly_top + credit[1]
            if placement > 0 and placement < SCREEN_HEIGHT:
                screen.blit(credit[0], credit[0].get_rect(center=(SCREEN_WIDTH/2, placement)))
        
        screen.blit(home_btn, home_rect)
        if home_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(highlight_btn, highlight_rect)
            if mouse_up:
                button_sound.play()
                return GameState.HOME

        pygame.display.flip()
        
        
def end_screen(screen):
    play_btn = UIElement(
        center_position=(600, 500),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Play again',
        padding = 16,
        border_radius = 8,
        action=GameState.NEWGAME,
    )
    home_btn = UIElement(
        center_position=(600, 600),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Home',
        padding = 20,
        border_radius = 8,
        action=GameState.HOME,
    )
    quit_btn = UIElement(
        center_position=(600, 700),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Quit',
        padding = 16,
        border_radius = 8,
        action=GameState.QUIT
    )

    buttons = [play_btn, home_btn, quit_btn]
    bg = pygame.image.load('backgrounds/gameoverbg.png').convert()
    screen.fill(BLACK)

    # Music Source: Square Foot Ocean by Martijn de Boer (NiGiD) (c) copyright 2022 
    # Music License: Licensed under a Creative Commons Attribution Noncommercial  (3.0) license.
    # http://dig.ccmixter.org/files/NiGiD/65334 
    pygame.mixer.music.load('sounds/NiGiD_Square_Foot_Ocean.mp3')
    pygame.mixer.music.play(loops=-1)

    # main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

            # KEYDOWN event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return GameState.QUIT
            # window close
            elif event.type == QUIT:
                return GameState.QUIT
            
        screen.blit(bg, (0,0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                button_sound.play()
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def win_screen(screen):
    play_btn = UIElement(
        center_position=(600, 500),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Play again',
        padding = 16,
        border_radius = 8,
        action=GameState.NEWGAME,
    )
    home_btn = UIElement(
        center_position=(600, 600),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Home',
        padding = 20,
        border_radius = 8,
        action=GameState.HOME,
    )
    quit_btn = UIElement(
        center_position=(600, 700),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Quit',
        padding = 16,
        border_radius = 8,
        action=GameState.QUIT
    )

    buttons = [play_btn, home_btn, quit_btn]
    bg = pygame.image.load('backgrounds/winbg.png').convert()
    screen.fill(BLACK)

    # display score
    finalscoretext = 'Score: ' + str(score)
    finalscore = [create_surface_with_text(finalscoretext, 40, WHITE, BLACK), (600, 350)]

    # Music Source: Square Foot Ocean by Martijn de Boer (NiGiD) (c) copyright 2022 
    # Music License: Licensed under a Creative Commons Attribution Noncommercial  (3.0) license.
    # http://dig.ccmixter.org/files/NiGiD/65334 
    pygame.mixer.music.load('sounds/NiGiD_Square_Foot_Ocean.mp3')
    pygame.mixer.music.play(loops=-1)

    # main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

            # KEYDOWN event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return GameState.QUIT
            # window close
            elif event.type == QUIT:
                return GameState.QUIT
            
        screen.blit(bg, (0,0))

        finalscore[0].set_colorkey((255, 255, 0), RLEACCEL)
        score_rect = finalscore[0].get_rect(center=finalscore[1])
        finalscoreborder = create_border_surface(score_rect, 16)
        pygame.draw.rect(screen, BLACK, finalscoreborder, border_radius = 12)
        screen.blit(finalscore[0], score_rect)


        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                button_sound.play()
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def instructions_screen(screen):
    home_btn = UIElement(
        center_position=(600, 700),
        font_size=30,
        bg_rgb=CRIMSON,
        text_rgb=WHITE,
        text='Home',
        padding = 16,
        border_radius = 8,
        action=GameState.HOME,
    )

    buttons = [home_btn]
    
    bg = pygame.image.load('backgrounds/instructionsbg.png').convert()
    screen.fill(BLACK)
    
    instructions = [
        [create_surface_with_text('Welcome to Campus Crosser!', 30, WHITE, CRIMSON), (600, 160)],
        [create_surface_with_text('Find important places in the Yard before your score reaches zero.', 22, WHITE, CRIMSON), (600, 220)],
        [create_surface_with_text('Move the player using arrow keys.', 22, WHITE, CRIMSON), (600, 260)],
        [create_surface_with_text('Find targets by touching the points in front of buildings.', 22, WHITE, CRIMSON), (600, 300)],
        [create_surface_with_text('Don\'t run into others in the Yard; you will lose 20 points.', 22, WHITE, CRIMSON), (600, 340)],
        [create_surface_with_text('Hurry! Your score also decreases as time goes on.', 22, WHITE, CRIMSON), (600, 380)],
        [create_surface_with_text('Good luck! Have fun Campus Crossing!', 22, WHITE, CRIMSON), (600, 460)]
    ]

    # main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

            # KEYDOWN event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return GameState.QUIT
            # window close
            elif event.type == QUIT:
                return GameState.QUIT
        
        screen.blit(bg, (0,0))
        
        for instruction in instructions:
            instruction[0].set_colorkey((255, 214, 64), RLEACCEL)
            screen.blit(instruction[0], instruction[0].get_rect(center=instruction[1]))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                button_sound.play()
                return ui_action
            button.draw(screen)

        pygame.display.flip()


# Basics of game design adapted from: 
# Fincher, Jon. (2019, September 16). "PyGame: A Primer on Game Programming in Python." RealPython.
# https://realpython.com/pygame-a-primer/
def play_level(screen):
    global score
    global time

    score = SCORE
    time = 0
    infoqueue.clear()
    subtraction.clear()
    checkedpoints.clear()

    paused = False

    # Music Source: Floating Through Time (SAW mix) by stellarartwars (c) copyright 2016 
    # Music License: Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. 
    # http://dig.ccmixter.org/files/stellarartwars/55017 Ft: Jeris
    pygame.mixer.music.load('sounds/stellarartwars_Floating_Through_Time.mp3')
    pygame.mixer.music.play(loops=-1)

    # set background
    bg = pygame.image.load('backgrounds/grasstile.png').convert()
    pathmap = [
        pygame.image.load('backgrounds/yardmaps/pixil-frame-0.png').convert(),
        pygame.image.load('backgrounds/yardmaps/pixil-frame-1.png').convert(),
        pygame.image.load('backgrounds/yardmaps/pixil-frame-2.png').convert(),
        pygame.image.load('backgrounds/yardmaps/pixil-frame-3.png').convert(),
        pygame.image.load('backgrounds/yardmaps/pixil-frame-4.png').convert(),
        pygame.image.load('backgrounds/yardmaps/pixil-frame-5.png').convert()
    ]

    # background
    screen.fill(BLACK)

    # feature buttons

    buttons = [
        ['home', pygame.image.load('buttons/home_btn.png').convert(), (30,30), pygame.image.load('buttons/home_btn_hover.png').convert()],
        ['pause', pygame.image.load('buttons/pause_btn.png').convert(), (80,30), pygame.image.load('buttons/pause_btn_hover.png').convert()]
    ]
    play_btn = [pygame.image.load('buttons/play_btn.png').convert(), (80,30), pygame.image.load('buttons/play_btn_hover.png').convert()]
    play_btn[0].set_colorkey(BLACK, RLEACCEL)
    play_btn[2].set_colorkey(BLACK, RLEACCEL)
    play_rect = play_btn[0].get_rect(center=play_btn[1])
    play_highlight_rect = play_btn[2].get_rect(center=play_btn[1])
    
    # set player
    player = Player()

    # creates event to add tourist
    ADDTOURIST = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDTOURIST, round(1000/TPS)) # adds tourists every second

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

    # add locations to targets in random order
    if OBJECTIVES > len(locations):
        sites = len(locations)
    else:
        sites = OBJECTIVES
    while len(targets) != sites:
        num = random.randint(0, len(locations) - 1)
        if locations[num] not in targets:
            targets.append(locations[num])

    
    # game loop
    while True:

        mouse_up = False

        for event in pygame.event.get():
            # register right clicks
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            # KEYDOWN event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return GameState.QUIT
            # window close
            elif event.type == QUIT:
                return GameState.QUIT
            # add tourist
            elif event.type == ADDTOURIST and not paused:
                new_tourist = Tourist()
                tourists.add(new_tourist)
                all_sprites.add(new_tourist)
        
        # record keys pressed
        pressed_keys = pygame.key.get_pressed()

        # paused
        if paused:
            screen.blit(play_btn[0], play_btn[0].get_rect(center=play_btn[1]))
            if play_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(play_btn[2], play_highlight_rect)
                if mouse_up:
                    button_sound.play()
                    pygame.mixer.music.play(loops=-1)
                    paused = False
                    mouse_up = False

        if not paused:
            # update player sprite
            player.update(pressed_keys, buildings, tourists)

            # update checkpoints to display info
            checkpoints.update(player, infoqueue)

            # update tourist
            tourists.update(buildings, player)
            
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
                
            # buildings, tourists on screen
            for sprite in all_sprites:
                screen.blit(sprite.surf, sprite.rect)

            # draw updated checkpoints
            for building in building_list:
                if building[0] in checkedpoints:
                    checkedpoint = pygame.image.load('buildings/checkedpoint.png').convert()
                    checkedpoint.set_colorkey(WHITE, RLEACCEL)
                    checked_rect = checkedpoint.get_rect(center=building[3])
                    screen.blit(checkedpoint, checked_rect)

            # draw player
            screen.blit(player.surf, player.rect)

            # draw info labels
            for info in infoqueue:
                pygame.draw.rect(screen, CRIMSON, info[2], border_radius = 4)
                screen.blit(info[0], info[1])
            
            for points in subtraction:
                screen.blit(points[0], points[1])

            # display score
            scoretext = 'Score: ' + str(score)
            scoredisplay = create_surface_with_text(scoretext, 18, WHITE, CRIMSON)
            score_rect = scoredisplay.get_rect(center=(1100,20))
            border = create_border_surface(score_rect, 6)
            pygame.draw.rect(screen, CRIMSON, border, border_radius = 6)
            screen.blit(scoredisplay, score_rect)
                
            # draw home and pause buttons, add functionality
            for button in buttons:
                button[1].set_colorkey(BLACK, RLEACCEL)
                button[3].set_colorkey(BLACK, RLEACCEL)
                button_rect = button[1].get_rect(center=button[2])
                highlight_rect = button[3].get_rect(center=button[2])
                screen.blit(button[1], button_rect)
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(button[3], highlight_rect)
                    if mouse_up:
                        if button[0] == 'home':
                            button_sound.play()
                            return GameState.HOME
                        else:
                            button_sound.play()
                            pygame.mixer.music.stop()
                            screen.blit(button[1], button_rect)
                            paused = True       

            # call the first find
            if time == 0:
                instructions = []
                instructions.append('Please find ' + targets[0][0] + '.')
                goaltext = instructions[0]
                goaldisplay = create_surface_with_text(goaltext, 18, WHITE, CRIMSON)
                goal_rect = goaldisplay.get_rect(center=(600, 400))
                goal_border = create_border_surface(goal_rect, 6)
                pygame.draw.rect(screen, CRIMSON, goal_border, border_radius = 6)
                screen.blit(goaldisplay, goal_rect)
                pygame.display.flip()
                # wait
                pygame.time.wait(2000)
                # clear list
                instructions.clear()
                
            # check for matches 
            for info in infoqueue:
                if info[3] == targets[0][1]:
                    checkedpoints.append(info[3])
                    checkpoint_sound.play()
                    del targets[0]

                    # check for empty list
                    if len(targets) == 0:
                        # win
                        win_sound.play()
                        return GameState.WIN

                    # display on screen
                    instructions.append('Please find ' + targets[0][0] + '.')
                    goaltext = instructions[0]
                    goaldisplay = create_surface_with_text(goaltext, 18, WHITE, CRIMSON)
                    goal_rect = goaldisplay.get_rect(center=(600, 400))
                    goal_border = create_border_surface(goal_rect, 6)
                    pygame.draw.rect(screen, CRIMSON, goal_border, border_radius = 6)
                    screen.blit(goaldisplay, goal_rect)

                    pygame.display.flip()

                    # wait
                    pygame.time.wait(2000)

                    # clear
                    instructions.clear()       
            
            # set framerate
            clock.tick(30)
            time += 1
            if time % 6 == 0:
                score -= 1

            if score <= 0:
                lose_sound.play()
                return GameState.GAMEOVER
        
        # update display
        pygame.display.flip()


main()