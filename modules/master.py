import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game import Game
    from .player import Player
    from .debug import Debug
    from ..main import App

class Master:

    def __init__(self):

        self.app:App
        self.debug:Debug
        self.game:Game
        self.player:Player

        self.dt:float = 0

        self.font_big = pygame.Font(size=20)
        self.font_med = pygame.Font(size=15)
        self.font_small = pygame.Font(size=10)

