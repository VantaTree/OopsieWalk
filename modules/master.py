import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game import Game
    from .level import Level
    from .player import Player
    from .debug import Debug
    from .menu import MainMenu, PauseMenu
    from ..main import App, State

class Master:

    def __init__(self):

        self.app:App
        self.debug:Debug
        self.game:Game
        self.level:Level
        self.player:Player
        self.main_menu: MainMenu
        self.pause_menu:PauseMenu
        self.State:State

        self.dt:float = 0

        self.font_big = pygame.Font(size=25)
        self.font_med = pygame.Font(size=20)
        self.font_small = pygame.Font(size=15)

