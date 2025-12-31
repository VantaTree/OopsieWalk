import pygame
from .config import *
from .engine import CustomGroup, CustomTimer, dist_sq
from .player import TrailSegment
from .hazards import Hazard
import json
import random
from enum import Enum

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from .master import Master
    from .player import Player
    from .characters import Biby

class Level:
    
    class State(Enum):
        BUILD = 0,
        RUN = 1,
    
    def __init__(self, master: "Master", player, biby, map_type):
        
        self.master = master
        self.master.level = self
        self.screen:pygame.Surface = self.master.app.screen

        self.player:"Player" = player
        self.biby:"Biby" = biby

        self.map_type = map_type
        with open(F"data/levels/{map_type}.json") as f:
            self.data = json.load(f)

        self.ysort_grp = CustomGroup()

        self.trails:list[list[TrailSegment]] = []
        self.attractors:list[GravityNode] = []
        self.repellers:list[GravityNode] = []

        self.attract_strength = 0.002
        self.repel_strength = 0.001

        self.attract_radius = 32
        self.repel_radius = 32
        
        self.curr_state = self.State.BUILD

        self.load_map()

    def load_map(self):
        
        self.player.set_pos(self.data["player_pos"])
        
        x, y, size = self.data["biby_goal_pos_size"]
        self.biby_goal_pos = pygame.Vector2(x, y)
        self.biby_goal_size = size

        self.biby.set_pos(self.data["biby_pos"])
        self.biby.dir.update(1, 0)
        self.biby.dir.rotate_ip(self.data["biby_angle"])

        self.player.max_walls = self.data["wall_amount"]
        self.player.wall_remaining = self.player.max_walls
        
        self.attractor_amount = self.data["attractor_amount"]
        self.repeller_amount = self.data["repeller_amount"]
        
        self.hazard_grp = CustomGroup()
        for hazard in self.data["hazards"]:
            Hazard(self.master, [self.hazard_grp, self.ysort_grp],
                   hazard["type"], hazard["pos"], random.randint(1, 360))

        # for x, y in self.data["attractors"]:
        #     node = GravityNode(self.master, x, y, self.attract_strength, self.attract_radius, 2500, 1)
        #     self.attractors.append(node)

        # for x, y in self.data["repellers"]:
        #     node = GravityNode(self.master, x, y, self.repel_strength, self.repel_radius, 2500, -1)
        #     self.repellers.append(node)

    def check_biby_goal(self):
        
        if dist_sq(self.biby.pos, self.biby_goal_pos) <= self.biby_goal_size**2:
            pass
            self.master.debug("Goal", "")
            self.master.win_screen.open()
            # self.master.app.state = self.master.State.WIN
            # weeeeeeeeeeeee
            
    def place_gravity_node(self, type:Literal["attractor", "repeller"]):
        
        if not self.player.in_control: return
        
        x, y = self.player.pos
        if type == "attractor" and self.attractor_amount > 0:
            self.attractor_amount -= 1
            node = GravityNode(self.master, x, y, self.attract_strength, self.attract_radius, 2500, 1)
            self.attractors.append(node)
                
        elif type == "repeller" and self.repeller_amount > 0:
            self.repeller_amount -= 1
            node = node = GravityNode(self.master, x, y, self.repel_strength, self.repel_radius, 2500, -1)
            self.repellers.append(node)
            
    def change_state(self, state):
        self.curr_state = state
        self.master.player.change_level_state(self.curr_state)
        self.master.biby.change_level_state(self.curr_state)

    def draw_bg(self):
        
        self.screen.fill("beige")

        for node in self.attractors:
            node.draw()
        for node in self.repellers:
            node.draw()

    def draw(self):
        
        pygame.draw.circle(self.screen, "gold", self.biby_goal_pos, self.biby_goal_size)
        
        self.ysort_grp.draw_y_sort(lambda obj: obj.rect.bottom)

    def draw_fg(self):
        pass

    def update(self):

        for node in self.attractors:
            node.update()
        for node in self.repellers:
            node.update()
            
        self.hazard_grp.update()
            
        self.check_biby_goal()
        
        # for trail in self.trails:
        #     for i in range(len(trail)-3):
        #         if trail[i] is None or trail[i+1] is None: continue
        #         pygame.draw.line(self.master.debug.surface, (255, 0, 0), trail[i].rect.midbottom, trail[i+1].rect.midbottom)


class GravityNode:

    def __init__(self, master:"Master", x, y, strength, radius, duration, multiplier):

        self.master = master
        self.screen:pygame.Surface = self.master.app.screen
        self.pos = pygame.Vector2(x, y)
        self.strength = strength
        self.radius = radius
        self.duration = duration
        self.active = True
        self.multiplier = multiplier

        self.active_timer = CustomTimer()

    def engage(self):
        if self.master.level.curr_state != self.master.level.State.RUN:
            return
        if self.active and not self.active_timer.running:
            self.active_timer.start(self.duration)

    def draw(self):
        
        if self.multiplier > 0:
            color = pygame.Color.from_hsla((96.4, 80, 50, 100))
        else:
            color = pygame.Color.from_hsla((23.5, 80, 50, 100))
        
        if not self.active:
            color = color.lerp(0x0, 0.2)
        elif self.active_timer.running:
            h, s, l, a = color.hsla
            color = pygame.Color.from_hsla((h, 100, l, a))

        pygame.draw.circle(self.screen, color, self.pos, 4)
        pygame.draw.circle(self.screen, color, self.pos, 4+self.radius, 1)

    def update(self):

        if self.active_timer.check():
            self.active = False
