import pygame
from .config import *
from .engine import *
from .entity import Entity

class Hazard(Entity):
    
    def __init__(self, master, grps, _type, pos, angle):
        
        if _type == "spike":
            hazard = "spike-4x4"
        if _type == "acid":
            hazard = "acid-16x16"
        else: pass
        images:list[pygame.Surface] = import_spritesheet("graphics/hazards", f"{hazard}.png")
        images = [pygame.transform.rotate(img, 90) for img in images]
        super().__init__(master, grps, images)
        self.pos.update(pos)
        self.dir.rotate_ip(angle)
        self.hitbox.x = pos[0] - self.rect.w/2
        self.hitbox.y = pos[1] - self.rect.h/2
        self.hitbox.w = self.rect.w
        self.hitbox.h = self.rect.h
        
    def update(self):
        
        if self.master.biby.hitbox.colliderect(self.hitbox):
            self.master.loose_screen.open()