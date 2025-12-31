# Oopsie Walk

#### Video Demo:  https://youtu.be/AHPfh8V_DP4

#### Description:

You are a sentient motorcycle, your task is to guide a robot called BiBy towards the target for each level.
You can guide the robot by placing walls and placing gravity nodes that attract or repels it.
Make sure to not let the Biby robot close to any of the hazards.
If you find yourself in a difficult position you can pause the game and restart the level.

**Controls:**

* WASD | Arrow Keys -> Move player Character
* Space -> Place walls when holding it
* 1 -> Place attractor
* 2 -> Place repeller
* Enter -> Start Biby Robot (you cannot move after this)
* Escape -> Pause / Unpause

**Working:**

The game is made in pygame, it is built on a custom engine I made, it includes spritesheet loading, timers, menus, etc.

The `Level` class loads the specified level from json files in `data/levels`.

The `App` class handles all the states seamelessly.
App states like MAIN_MENU, LEVEL_MENU, IN_GAME, WIN, PAUSED etc, define which part of the game is supposed to run, having seperate logic for each.

The `Game` and `Level` classes manage all the aspect of the game, including the player, robot, hazards, gravity nodes, wall tiles, win/loose condition etc.

The `Player` is handles user input to move the motorcycle and turn it, when pressing space it lays down a trail of walls each 4-8 pixels apart making a smooth yet seamless wall, with shadows to indicate where it touches the ground.
While pressing 1 or 2 places the respective gravity node at the player's position.

The `Biby` or the robot that you are tasked with guiding has a simple physics based movement, it calculates the nearest wall segment and performs distamce and direction calculations to keep itself from colliding into the wall and tries to align itself in the direction of the wall.
It also moves away from repeller graity nodes and towards attractor gravity nodes, sometimes orbiting them till that node's timer runs out it becomes deactivated to prevent the robot from oribiting it endlessly.
When the `Biby` character reaches the gold and white striped target shape, the levels is completed.
But if it touches any of the spikes or other hazards it will end it game over, prompting you to restart the level.

The `Entity` class is a parent class for both the player and the robot, it defines some default logic including that of **Sprite Stacking**, which is the chosen way of rendering objects giving a smooth voxel like 3D look, with pixel perfect rotations.

The `menus.py` file is a collection of buttons and different menus like `MainMenu`, `PauseMenu`, `LevelMenu`, `WinScreen` and `LooseScreen`.

The `Debug` class is a handy tool to display debug text and debug surfaces like collision boxes, vectors etc.


**How to run:**

1. Make sure python 3.10+ is installed
2. Close this repoitory `git clone https://github.com/VantaTree/OopsieWalk.git`
3. Navigate to the `OopsieWalk` folder
4. Install libraries `pip install -r requirements.txt` (`pip install pygame-ce`)
5. Run the game `python main.py`
