import pygame
from .config import *
from .engine import CustomGroup
from .player import TrailSegment
import json

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .master import Master
    from .player import Player
    from .characters import Biby

class Level:
    
    def __init__(self, master: "Master", player, biby, map_type):
        
        self.master = master
        self.master.level = self
        self.screen:pygame.Surface = self.master.app.screen

        self.player:"Player" = player
        self.biby:"Biby" = biby

        self.map_type = map_type
        with open(F"data/levels/{map_type}.json") as f:
            self.data = json.load(f)
        self.load_map()

        self.ysort_grp = CustomGroup()

        self.trails:list[list[TrailSegment]] = []

    def load_map(self):
        
        self.player.set_pos(self.data["player_pos"])

        self.biby.set_pos(self.data["biby_pos"])
        self.biby.dir.update(1, 0)
        self.biby.dir.rotate_ip(self.data["biby_angle"])

        self.player.max_walls = self.data["wall_amount"]
        self.player.wall_remaining = self.player.max_walls


    def draw_bg(self):
        pass

    def draw(self):
        self.ysort_grp.draw_y_sort(lambda obj: obj.rect.bottom)

    def draw_fg(self):
        pass

    def update(self):
        pass

