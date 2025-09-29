import pygame
from .config import *
from .engine import CustomGroup
from .player import Player

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .master import Master

class Game:
    
    def __init__(self, master: "Master"):
        
        self.master = master
        self.master.game = self

        self.ysort_grp = CustomGroup()
        
        self.player = Player(master, [self.ysort_grp], main_player=True)

    def get_input(self):
        
        for event in pygame.event.get((pygame.KEYDOWN)):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
                

    def draw(self):

        # self.player.draw()
        self.ysort_grp.draw_y_sort(lambda obj: obj.rect.bottom)

    def update(self):

        self.get_input()

        self.player.update()

    def run(self):

        self.update()

        self.draw()
