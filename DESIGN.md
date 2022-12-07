OVERVIEW

The primary structure of our game runs through several functions that each correspond to a different screen and its associated features. The main game loop tracks different game states (GAMEOVER, CREDITS, HOME, QUIT, NEWGAME, WIN, INSTRUCTIONS) and runs the specific function for each. The “screen” functions (creating the homescreen, credit screen, introduction screen, and end screens) create a chain of user interfaces and are all structured similarly: buttons are initialized with certain parameters and purposes, and a main loop constantly checks for inputs to transfer to other game states. The “play” function runs the game itself. After initializing variables and resources, the “play” loop runs, continually updating objects on screen while checking for completion of certain actions. If the score reaches zero, the “play” loop exits to a loss screen and enters the interface chain. If the player reaches all the requested destinations, the game exits to a win screen before entering the interface chain again.
	Pygame works through surface layering: continuously looped updates to the screen create movement and events. Surfaces coordinates are defined with (0,0) at the top left corner and positive “x” directed right, positive “y” directed downward. The pygame blit() (“block transfer”) function appends images or shapes to a specified surface or location. Then the flip() function updates the display with all new surfaces. Most of our surfaces are rectangles, an easy shape for geometry manipulation and positioning. A majority of the code deals with what to add to a screen layer, when to add it, and where to add it. Other aspects of the code address event detection, sprite interactions, and many static lists store information to be referenced by different functions.
The structure of the game allows for easy expansion and manipulation of game features through use of global variables and drawing from centralized “libraries” of information in the form of global lists. Specifically, the frequency of tourist generation, the starting player score, and the number of target buildings are easily modified at the start of the code. Further, target locations can be added or removed in the [locations] list (provided they are linked to an existing building), and entirely new maps can be added by creating new building directories and terrain maps. Additionally, player sprite customization can occur by modifying its animation frames, also located near the top of the document. The main obstacle to scalability—beyond the constraints of the python and the pygame library—is the number of assets which will eventually slow down the game.
Lastly, though our code is largely dynamic, we hard-coded a few items. The primary example of this occurs in the screen size (1200 x 800 pixels), which is not adjustable; all the pixel art is sized for these dimensions. Additionally, many of our global variables such as “time” and “pframe” are not actually necessary and could have been included in the initialization section of local functions before the main gameplay loops, or associated with the attribute initialization of a sprite class.

INITIALIZATION (lines 1-128)

1: Imported libraries: The main library, [pygame], provides most of the game functionality through custom features suited to game programming. [pygame.freetype] adds text and font capability. Specific functions within pygame that will be referenced often are also individually imported to avoid having to type “pygame._” every instance (namely with the “rectangle” class and keystrokes). The python [random] library allows for pseudorandom number generation, important for diversifying the gameplay. The python [enum] library adds “enumerations,” a constant data type that ties together an identifier and a value.

20: Defining [GameState]: The gamestates are global enums that are constant, unique, and easily identifiable. Each corresponds to a function that should be performed to carry out a stage of the game.

30: Window dimensions: represented by these global constants so they are easily identifiable in the code below, but not adjustable.

34: Color library: constant color RGB triples defined for use below

39: Tourists per second: the number of tourists that spawn during each second of gameplay. Can be adjusted for varying game difficulty.

42: Score: starting score for the player upon entering a level, adjustable.

44: Objectives: number of target buildings the player must find, adjustable. If objectives is set higher than the number of listed target buildings, the game defaults to using all listed buildings (see line 900).

47: Initialization of pygame sound compatibility

50: Sounds: each sound is set to a global variable that can be used in the code below for easier readability.

61: Initialization an object to track time within pygame

62: Global time variable set (used in [play_level] function for score decrement and initial instructions). This variable doesn’t actually need to be global in our code, but this aspect can give flexibility if needed for sub-functions.

65: Score initialized for use in the play_level function and within the tourist class.

68: Global “pframe” variable accessed to always know the state of the player and return proper animation frame (used within the [Player] class).

69: The following global lists define the animation frames for the player, the buildings for the yard (with associated names, image files, locations on the map, and locations for their waypoints), and the target locations (name/service, connected building).

119: The following empty lists are initialized to search and print impermanent items on screen

DEF CREATE_BORDER_SURFACE (lines 131-133)
This custom function returns a rectangular surface for the pygame.draw function to draw onto in order to create borders (of “padding” pixel width) around a given text surface. As this occurs fairly frequently, the function was created to aid readability.

DEF CREATE_SURFACE_WITH_TEXT (lines 139-143)

This function accesses built-in pygame text capability to return a surface with specified text in bold. The function’s arguments adjust font size, the background highlight color of the text, and the text color. The font is set to ‘Courier’ within this function.

CLASS UIELEMENT (lines 148-217)

The UI element class creates and defines a pygame sprite to be used as a button, with arguments for text, position (xy), font size, background color (RGB triple), text color (RGB triple), border width (pixels), border radius, and button action (a [GameState] to return).
	
def __init__
The initialized properties of a UI element. The button has two states, a highlighted state that occurs when in contact with the mouse and a default state. The create_surface_with_text function is called to create surfaces for both of these conditions, with the highlighted surface 1.2 times the size of the default. These image surfaces and their corresponding rectangles (used to position the surfaces) are added to lists. This list is called by the @property sub-functions below to conditionally return the correct index. Several “self._” variables are defined (these will be linked to the specific sprite) based on input arguments for use below in drawing a rectangular border around the text (line 216). The surfaces for these rectangular borders are created by calling the create_border_surface function based on the default text and highlighted text. Lastly, calling the python super() function allows this init method to access all the properties of the parent sprite class defined within pygame.
	
@property
The property tags decorate the following sub-functions which return the default or the highlighted state for the text, text rectangle, and border surface based on the “self.mouse_over” variable which checks whether the mouse is hovering over the button in the update function below.

def update
Using the pygame collidepoint function, this function checks whether the position of the mouse pointer (passed into here within each of the main screen functions where this function is called) is within the surface of the button. If the mouse pointer is over the button, the mouse_over conditional is updated (triggering highlighted states) and the function further checks if the button has been right-clicked (through the mouse_up variable, also passed in from the screen function), and returns the button’s action, a [GameState].

def draw
This function draws the border rectangle, implementing as arguments certain properties of the UI element class defined above, and blits the text as well to a specified surface (always the screen when called below).


CLASS PLAYER (lines 221 - 308)

The player class defines the playable sprite controlled by the player, responsible for updating the player location based on keystrokes, checking for collisions, and showing a point deduction visual above the player’s head.

def __init__
Attribute initialization: the surface (the player’s appearance) is set based on the global “pframe” variable, and all white pixels in this skin are keyed out. Additionally, the player rectangle defining its location is set initially at the center of the screen.

def show_point_deduction
A text surface is created to display a number in red (input as an argument to the function) and the white background of this number is keyed out. The position of this visual is set with a rectangle positioned relative to the player’s rectangle position (same x-value, smaller y-value to appear above the player’s head). Based on an input state, the function will also either add this deduction visual and its rectangle location to the global subtraction list, a “queue” that presents information to be printed to the screen in the play_level function (line 990).

def update
The update function continually checks the input arguments and adjusts the player's rectangular position accordingly. If action keys (left, right, up, down) occur in the pressed_keys list of all user-input keystrokes, the player rectangle is moved accordingly, and animation frames are incremented sequentially, or reset to the beginning of the cycle based if incrementing would enter an animation for a different orientation. The screen boundaries constantly check the player rectangle for side positioning, if any of these sides go past the coordinates that define the screen, the rectangle is set against the edge of the screen, not allowing the player to move any further. The player hitbox is created to be slightly smaller and much shorter than the player’s bounding rectangle, so that the player can navigate between buildings and visually walk up to a building without triggering collisions. This hitbox is used for building collisions: while iterating through each of the buildings, if the player’s hitbox is contacting the building rectangle (detected using the pygame colliderect() function), a mathematical operation (adding a small increment in the opposite direction of a possible collision should push the player’s side coordinate outside the building in that direction if the player is against that side of the building) first determines which side of the player is colliding, then that side of the player player is set against the corresponding side of the building and is unable to cross further. Lastly, tourist collisions detect whether the player’s bounding rectangle contacts the tourist’s rectangle and applies the same method as the building collision to ensure that these two rectangles do not pass through each other.

CLASS BUILDING (lines 312 - 317)

The building sprite class is created so that sprite collisions can be used to detect player interactions and the buildings can be printed on screen along with the other sprites. The buildings have only a few initialized attributes used when calling a surface and location to blit: the surface image with white pixels keyed out is created by loading a specific building file taken from the building_list (assigned within the [play_level] function, line 888) and a rectangle for positioning is rendered in a set location (also from the building_list).

CLASS BUILDING_CHECKPOINT (lines 321 - 343)

The Building_checkpoint class creates and defines a pygame sprite which appears as a circle by a building sprite and is used to track collisions with the player for the game objective.

def __init__
The custom checkpoint image is loaded to be used as the surface and a corresponding rectangle is created with the location passed in to __init__ as its center. A sprite for the name label and a border are also created, via create_surface_with_text and create_border_surface, respectively. A tracker is also initialized to zero.

def update
We wished for the info labels with the building names to appear when the player was in contact with the checkpoint and disappear when the player moved away; thus, we incremented the tracker once when the collision was first detected and in that case appended the proper surface, text, border, and name to be displayed to infoqueue. Once the player is no longer colliding with the checkpoint, self.tracker is reset to zero and infoqueue is cleared, so that further displays to the screen will no longer display the label.

CLASS TOURIST (lines 347 - 411)

The Tourist class creates and defines a pygame sprite which will enter the screen to interfere with the Player’s movement and score. 

def __init__
Tourist loads three frames for the appearance, which are held in the tourist_frames list. A pseudorandom integer from 0 to 2 inclusive is generated in order to select the index of tourist_frames that will be used; this allows different instances of the Tourist class to have different appearances on screen. As we wished for the tourist sprites to appear to enter the screen from the edges, but wanted the tourist sprites to be killed when they exited the screen we created a sides list to define edges one pixel away from the true edges of the screen. Sides also initializes x and y direction speeds for each edge, such that the tourist sprite will initially move into the screen (rather than immediately off). A tracker is also initialized to zero for later use with collisions.  

def update
Update controls the tourist’s movement and monitors collisions with the buildings and the player. New speeds are generated periodically for the tourist sprites; in order to prevent the tourists from changing speeds very rapidly with the frame rate for the rest of the program, we controlled for a 1/11 chance of changing speeds via the use of random integer generation and comparison within the range from 0 to 10 inclusive. The speeds generated for the x and y directions are also randomly generated within a restricted range, enabling tourist sprites to move at different speeds from others and in different directions. A check is included such that a tourist could not have both an x direction and y direction speed of 0 (which would result in no motion). Move_ip is then used to move the tourist based on the x and y speeds. In order to prevent tourist sprites from passing over building sprites, update checks for collisions between each tourist and all the sprites in the buildings group; if there is a collision, the x and y speeds are reversed so that the tourist is stopped and travels in the opposite direction. If the tourist and player sprites collide, the direction will be reversed as for the building collisions, and the tracker will be incremented. If the tracker is equal to 1 (or otherwise not equal to 0 at some point), a collision will be registered, resulting in a visual -20 effect and a sound effect. If the tourist passes beyond the edges of the screen, the sprite will be killed.

DEF MAIN (lines 417 - 447)

Def main initializes pygame, creates an initial screen with the specified dimensions, and sets up the structure for the game loop. It initializes the game_state to the home screen for the start of the game, and then continually checks for changes to the game_state, at which point it runs the corresponding function for the specified screen. If the change sets game_state to quit, it quits pygame and stops the program.

DEF HOME_SCREEN (lines 450 - 528)

Def home_screen creates the home screen display. It creates buttons for play, instructions, credits, and quit using UIElement, specifying the necessary information, and adds the buttons to a list. It sets a default background to black and loads the custom background image png, which is displayed on the screen later via blit. It also loads music and plays it with an indefinite loop. Within the main loop, it continually initializes mouse_up to False and then checks for a mouse right-click event (right-click is specified by event.button == 1). It also checks for a keydown event when the user presses escape or when the user quits the game by closing the window and responds by returning the quit game state. If a button has been right-clicked, mouse_up is set to True, which triggers the button sound effect and returns the specified button action based on the position. The visuals are displayed to the screen via pygame.display.flip.

DEF CREDITS_SCREEN (lines 531 - 614)

The initial variables define the height of the rectangle that the credits are displayed on, a counter to track each frame and update the animation accordingly, and a variable to define where the top of the credits rectangle is drawn. The credits screen incorporates a smaller house image as the home button, since a normal home button would interfere visually with the scrolling screen animation. This image is loaded and its highlighted counterpart are loaded, keyed, and positioned using bounding rectangles. The background is loaded using the appropriate background image. The credits list contains all lines of credits as text surfaces created by calling create_surface_with_text repeatedly (this design is bulky, but worked with existing structures), and a positioning index that indicates how far below the top of the credits rectangle to position the text surface based on y-coordinates. The main loop begins similarly to the other screen functions with a check for mouse right-click, esc key, and window close, but adding a counter increment for each run-through and checking whether the top border of the credits rectangle is a set increment past the top of the screen (the height of the credits plus an increment for a little delay) at which point the loop is exited, returning the [GameState] for the home screen. The credits rectangle is redrawn with a new y-value parameter each time the variable “scrolly_top” is adjusted, starting at the height of the screen (i.e. being entirely off-screen) and decrementing by one each time a certain number of frames pass. Here, every eight frames (i.e. eight updates of the counter) the top of the rectangle is drawn slightly further up the screen. Each of the credits in the initial list is incremented through, and if it’s y-position is within the screen window, it’s drawn on-screen in the correct position each frame, always the same increment from the top of the credits rectangle (allowing the credits to ascend with the border rectangle). Lasty, the home button is appended on the screen, appended in its highlighted form if the mouse hovers over it (detected with the mouse position and the collidepoint() function from pygame), and if the mouse is both over the button and clicks, the [GameState] for the home screen is returned.

DEF END_SCREEN (lines 617 - 684)

Def end_screen creates the end screen display when the user loses. It functions in the same way as def home_screen, but with variations to buttons (play again, home, and quit).

DEF WIN_SCREEN (lines 687 - 765)

Def win_screen creates the end screen display when the user wins. It functions in the same way as def home_screen, but with variations to buttons (play again, home, and quit). It also displays the user’s final score to the screen via create_surface_with_text.

DEF INSTRUCTIONS_SCREEN (lines 768 - 824)

Def instructions_screen creates the instructions screen display. It functions in the same way as def home_screen, but with variations to buttons (it creates only a home button). It also displays instructions on the screen by creating and iterating through a list of calls to create_surface_with_text.

DEF PLAY_LEVEL (830-1077)

Def play_level initializes score to the starting score of 300, as stored in the score constant, resets the time, and clears infoqueue, subtraction, and checkedpoints in order to prevent any residual displays when the user replays the game. It sets paused to False, such that the game begins in the play state. It then loads in music, background and map images, and sets a default black screen. It creates a list of buttons for the home and pause buttons and adjusts button appearance when the user hovers over the button. It then sets an instance of the Player class equal to player. It creates a custom event to add tourists and runs the event at certain time intervals, as determined by the value of TPS set. We chose to use a custom event for the tourist generation in order to allow for continuous renewal of the tourist sprites, given that some sprites would inevitably leave the game screen and thus be killed. Four sprite groups are then created for buildings, checkpoints, tourists, and all_sprites. These make collision checking more efficient, as it is possible to check for collisions with an entire group; they also help in the initial blit, as all_sprites can be iterated through. Buildings and checkpoints are then created based on information from building_list and are added to their respective groups. We wished for each round of gameplay to create a random route for the user to navigate when finding the targets. We thus create a new list, in random order. First, the number of sites is capped at the length of possible locations to choose from. Then, until the new target list has been completely filled, we select a random integer, the element at which index in locations we then append to targets.

The game loop continually checks for escape presses and window closing, which prompt the game to return the quit gamestate. It also checks for right clicks.

The paused function displays the default and highlighted states of the play button, and gives this functionality to change the paused state back to false, using the same click detection method as other buttons. Mouse up is immediately changed back to false as well, so that the subsequent pause button in the same position isn’t activated during the same frame.

If the game is not paused, the rest of the gameplay continues, updating the player, checkpoints, and tourists. The grass and path background tiles are displayed to the screen based on the size of the window. It then iterates through each sprite in the all_sprites group and displays it via blit. 

The updated checkpoints iterate through each building in the building list to get the any names that appear in the global “checkedpoints” list of reached target waypoints. If the name matches, the red “checkedpoint” image is displayed at the building’s waypoint location.

The player is then displayed to the screen via blit.

The name labels for each building and the visual point loss cues are displayed to the screen if they are present in infoqueue and subtraction, respectively. If infoqueue and subtraction are empty, the blit will effectively appear invisible on the screen.

The score is displayed to the upper right corner of the screen by creating a new surface, rect, and border via create_surface_with_text and create_border_surface, respectively. The border is drawn to the screen and the score surface and rect are displayed on top of it, via blit.

The home and pause buttons are both drawn with default and highlighted states, then functionality is instituted using the same method as the other buttons, iterating through each of them and checking for mouse collisions, then if the mouse is colliding, checking for clicks. If the home button is clicked, the gamestate for the home screen is returned. Otherwise, the pause button must be the one being clicked, thus the music is paused, the default version of the button is passed so that the default play button doesn’t have the highlighted pause button border during the frame, then the paused conditional is changed to “True.”

For the first set of instructions, only called when the loop is run for the first time (the time variable is zero), a surface is created (through the same text surface and border method) displaying the first item in the target list which should be found. This surface immediately is added to the screen and updated, then after waiting two seconds, the game loop resumes, clearing the surface as it is no longer called on the next passes.

The match function checks whether any entries have been appended to the global infoqueue list (i.e. the player has contacted a building waypoint), and if the building name of this entry matches the first entry’s building name in the ordered target list, the name is added to the “checkedpoints” list (so that the updated red checkpoint icon is now printed on top of the former checkpoint) and this first entry is now deleted from the targets list. Then if the length of the targets list is now zero (all targets found), the WIN gamestate is returned. Otherwise, the next set of instructions is displayed, by appending a string with new first entry on the target list to the instructions list, and then using this string value to make a bordered surface with the text instructions in the correct position and updating the screen immediately. After waiting for two seconds (the wait function freezes the entire game while it completes), the instructions list is cleared so that the next instructions can display when called.

The clock.tick() function from pygame sets the framerate to a determined value, here 30 fps to make the gameplay smooth but not too fast. Each frame the time variable is incremented by one. Every 6 frames (one fifth of a second) the player’s score is decreased to add some urgency to gameplay.

Lastly, if score is ever less than or equal to zero (since the -20 points from tourist collisions can send the score to negative values), the game plays a losing sound effect and returns the GAMEOVER gamestate.

MAIN (line 1080)

Calls the main() function and runs the game.