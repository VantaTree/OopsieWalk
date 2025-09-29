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

        super().__init__(master, grps, images, (220, 120))
        self.draw_outline = True
        self.dir = pygame.Vector2(-1, 0)

        self.moving = True
        self.speed = 0.5
        self.acc = 0.05
        self.dcc = 0.03

    def move(self):

        # vel_dist = self.vel.length()

        self.vel = self.dir * self.speed
        my_dir = self.dir.copy()

        for trail in self.master.player.trail:
            px, py = trail.rect.midbottom
            if (dis_sq := dist_sq(self.pos.xy, (px, py))) <= 64:
                target_vec = self.pos - (px, py)
                target_vec.normalize_ip()
                trail_dir = trail.dir if my_dir.dot(trail.dir) >= 0 else -trail.dir
                target_vec += trail_dir
                # target_vec.scale_to_length(0.02)
                # target_vec = ((8-math.sqrt(dis))/8)*target_vec
                # self.vel += target_vec
                self.dir += target_vec
        self.dir.normalize_ip()
        # self.vel.clamp_magnitude(vel_dist)

        if self.moving:
            self.vel.move_towards_ip(self.dir*self.speed, self.acc*self.master.dt)
        else:
            self.vel.move_towards_ip((0, 0), self.dcc*self.master.dt)

        # self.vel = self.dir * self.speed
        try:
            self.dir = self.vel.normalize()
        except ValueError:
            pass

        self.pos += self.vel * self.master.dt

        self.hitbox.midbottom = self.pos
        self.rect.midbottom = self.pos

    def update(self):
        
        self.move()