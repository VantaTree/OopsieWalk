# Oopsie Walk

#### Video Demo:  https://youtu.be/AHPfh8V_DP4

#### Description:

You are a sentient motorcycle, your task is to guide a robot called BiBy towards the target for each level.
You can guide the robot by placing walls and placing gravity nodes that attract or repels it.
Make sure to not let the Biby robot close to any of the hazards.
If you find yourself in a difficult position you can pause the game and restart the level.

#### Controls:

* WASD | Arrow Keys -> Move player Character
* Space -> Place walls when holding it
* 1 -> Place attractor
* 2 -> Place repeller
* Enter -> Start Biby Robot (you cannot move after this)
* Escape -> Pause / Unpause

#### Working:

The game is made in pygame, it is built on a custom engine I made, it includes spritesheet loading, timers, menus, etc.

The `Level` class loads the specified level from json files.

App states like MAIN_MENU, LEVEL_MENU, IN_GAME, WIN, PAUSED etc, define which part of the game is supposed to run, having seperate logic for each.

The `App` class handles all the states seamelessly.

The `Game` and `Level` classes manage all the aspect of the game, including the player, robot, hazards, gravity nodes, wall tiles, win/loose condition etc.

The `Debug` class is a handy tool to display debug text and debug surfaces like collision boxes, vectors etc.


#### How to run:

1. Make sure python 3.10+ is installed
2. Close this repoitory `git clone https://github.com/VantaTree/OopsieWalk.git`
3. Navigate to the `OopsieWalk` folder
4. Install libraries `pip install -r requirements.txt` (`pip install pygame-ce`)
5. Run the game `python main.py`
