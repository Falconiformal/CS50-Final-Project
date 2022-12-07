# CS50-Final-Project
WELCOME

Welcome to Campus Crosser! As the game is implemented in Python using PyGame, please ensure that Python and PyGame are installed, such as by running python3 -m pip install -U pygame --user or by following the instructions at https://www.pygame.org/wiki/GettingStarted. 

No additional configuration is necessary, although the game should be run on a device large enough to view the entirety of a window with dimensions 1200 x 800 pixels.


OBJECTIVE OF THE GAME

The objective of Campus Crosser is to find a given set of significant locations in part of Harvard’s Old Yard in the order instructed by prompts displayed one by one to the screen. The user should attempt to do so in the fastest time possible with the fewest number of collisions between the player and tourists/people in the Yard. The user can win the game by finding all of the objectives before their score reaches zero. The number of objectives and the rate of tourists per second in the game can be adjusted within the code in order to change the difficulty level; currently, the user can play with one to five objectives.


NAVIGATING THE GAME SCREEN

Campus Crosser begins on a Home Screen with four button options: “Play,” “Instructions,” “Credits,” and “Quit.” Select “Play” to begin the gameplay, select “Instructions” to view tips for how to play, select “Credits” to view a scrolling display of the music and sound effect sources, attribution of reference tutorials (more citation information is provided within the code), and game author information, and select “Quit” to close the game. On the Instructions and Credits screens, there are Home buttons — below the instructions (“Home”) and in the upper left corner (a house symbol), respectively — which return the user to the Home screen. Once the entire Credits scroll runs, it will automatically return to the Home screen; otherwise, the Home button can be used to return earlier. In some cases, the Credit screen scroll rate may lag or appear inconsistent, potentially due to differences in devices. In the upper left corner within the Play screen, there is another Home button (a house symbol), as well as a Pause/Play button, which pauses and resumes the game (including the game clock, music, tourists/people, and player). Once the game has been won or lost, there are button options for “Play again,” “Home,” and “Quit”; the “Play again” button starts gameplay again, “Home” returns to the Home screen, and “Quit” closes the game. At any point of gameplay, pressing the Esc key will also close the game.


HOW TO PLAY

The user controls the player sprite using left, right, up, and down arrow keys. The player cannot pass over buildings or tourists/people in the Yard; however, perhaps due to a dual interaction with the buildings, the player can pass over Lionel Hall when moving through the corner intersection of Lionel Hall and Harvard Hall from the Johnston Gate side (the bottom of the screen). 

Gameplay begins by displaying the instructions prompt (“Please find . . .”) for the first target location from the possible choices of Harvard Yard Operations (Yard Ops), The Phillips Brooks House Association, The Harvard Foundation for Intercultural and Race Relations, The Office for BGLTQ Student Life (QuOffice), and Holden Chapel. The order in which the targets are displayed and must be found is determined randomly at the start of each game. To find targets, the user must navigate the player to the checkpoint (the circle sprite) in front of the correct building. When a target’s matching checkpoint is found, a confirmation sound effect will play, the checkpoint will turn from gold to red, and the instruction for the next target location will be displayed. While exploring the Yard, if the player crosses over checkpoints (whether correct or incorrect), the name of the dorm/building will be displayed as long as the player is contacting it, and will disappear once the player moves away.

The user’s score will be recorded during the game and displayed in the upper right corner of the screen. The score starts at 300, but the user loses a point every fifth of a second. The user also loses 20 points each time the player collides with a tourist/person in the Yard; each collision will also trigger an “ow” sound effect. If the score reaches zero before all targets have been found, the user loses, the end sound is played, and the end screen is displayed. Otherwise, if the user finds all the targets before the score reaches zero, the player wins, the win sound is played, and the win screen with the player’s score is displayed.
