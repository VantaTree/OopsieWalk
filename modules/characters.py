import pygame
from .config import *
from .engine import *
from .entity import Entity
import math


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .master import Master

class Biby(Entity):
    
    def __init__(self, master: "Master", grps):

        images:list[pygame.Surface] = import_spritesheet("graphics/player", "biby-16x16.png")
        images = [pygame.transform.rotate(img, 90) for img in images]

        super().__init__(master, grps, images)
        self.master.biby = self
        
        self.draw_outline = True
        self.dir = pygame.Vector2(-1, 0)

        self.moving = False
        self.active = False
        self.speed = 0.5
        self.acc = 0.05
        self.dcc = 0.03
        
    def change_level_state(self, state):
        if state == self.master.level.State.BUILD:
            self.moving = False
            self.active = False
        elif state == self.master.level.State.RUN:
            self.moving = True
            self.active = True

    def move(self):
        
        if not self.active: return

        my_dir = self.dir.copy()
        avoid_vec = pygame.Vector2()
        guide_vec = pygame.Vector2()
        wall_count = 0
        path_dir = 0

        for trail in self.master.level.trails[0]:
            if trail is None: continue
            px, py = trail.rect.midbottom
            if (dis_sq := dist_sq(self.pos.xy, (px, py))) <= 64:
                wall_count += 1

                target_vec = self.pos - (px, py)
                target_vec = ((8-math.sqrt(dis_sq))/8)*target_vec
                avoid_vec += target_vec
                
                dot = my_dir.dot(trail.dir)
                path_dir += sigmoid(dot)

                trail_dir = trail.dir if dot >= 0 else -trail.dir
                guide_vec += trail_dir * 0.1

        self.dir += avoid_vec + guide_vec
        consider_guide = wall_count/5 < path_dir
        if consider_guide:
            self.dir += guide_vec
        self.master.debug("guide:", consider_guide)

        # attractors
        for node in self.master.level.attractors:
            if not node.active: continue
            if (dis_sq := dist_sq(self.pos.xy, node.pos.xy)) <= (node.radius)**2:
                target_vec = self.pos - node.pos
                target_vec *= -1
                target_vec.normalize_ip()
                target_vec = ((node.radius-math.sqrt(dis_sq))/node.radius)*target_vec
                self.dir = self.dir.slerp(target_vec, node.strength)
                node.engage()
                pygame.draw.line(self.master.debug.surface, "blue", self.pos, self.pos+(target_vec.normalize())*16)

        # repellers
        for node in self.master.level.repellers:
            if not node.active: continue
            if (dis_sq := dist_sq(self.pos.xy, node.pos.xy)) <= (node.radius)**2:
                target_vec = self.pos - node.pos
                target_vec.normalize_ip()
                target_vec = ((node.radius-math.sqrt(dis_sq))/node.radius)*target_vec
                self.dir = self.dir.slerp(target_vec, node.strength)
                node.engage()
                pygame.draw.line(self.master.debug.surface, "red", self.pos, self.pos+(target_vec.normalize())*16)

        self.dir.normalize_ip()
        if self.moving:
            self.vel.move_towards_ip(self.dir*self.speed, self.acc*self.master.dt)
        else:
            self.vel.move_towards_ip((0, 0), self.dcc*self.master.dt)

        try:
            self.dir = self.vel.normalize()
        except ValueError:
            pass

        self.pos += self.vel * self.master.dt

        self.hitbox.midbottom = self.pos
        self.rect.midbottom = self.pos

    def update(self):
        
        self.move()
        # for trail in self.master.level.trails:
        #     self.trail_coll_resolution(trail)

