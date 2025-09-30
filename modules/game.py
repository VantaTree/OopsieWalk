import pygame
from .config import *
from .level import Level
from .engine import CustomGroup
from .player import Player
from .characters import Biby

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .master import Master

class Game:
    
    def __init__(self, master: "Master"):
        
        self.master = master
        self.master.game = self

        self.player = Player(master, [])
        self.biby = Biby(master, [])

        # self.level = Level(master, self.player, self.biby, "01")
        self.level = Level(master, self.player, self.biby, "test")
        self.level.ysort_grp.add(self.player)
        self.level.ysort_grp.add(self.biby)
        self.level.trails.append(self.player.trail)

    def change_level(self, map_type):

        self.player.trail.clear()
        self.player.vel.update()
        self.player.dir.update(1, 0)
        self.player.input = False
        self.player.moving = False
        self.player.trail_index = 0
        # self.player.
        self.biby.vel.update()

        self.level = Level(self.master, self.player, self.biby, map_type)
        self.level.ysort_grp.add(self.player)
        self.level.ysort_grp.add(self.biby)
        self.level.trails.append(self.player.trail)


    def get_input(self):
        
        for event in pygame.event.get((pygame.KEYDOWN)):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
                if event.key == pygame.K_1:
                    self.change_level("01")
                if event.key == pygame.K_0:
                    self.change_level("test")

    def draw(self):

        self.level.draw_bg()
        self.level.draw()
        self.level.draw_fg()

    def update(self):

        self.get_input()

        self.player.update()

        self.biby.update()

        self.level.update()

    def run(self):

        self.update()

        self.draw()
