import pygame
from .config import *
from .engine import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .master import Master

class Entity(pygame.sprite.Sprite):
    
    def __init__(self, master: "Master", grps, images):

        super().__init__(grps)
        self.master = master
        self.screen:pygame.Surface = self.master.app.screen

        self.pos = pygame.Vector2()
        self.last_pos = self.pos.copy()
        self.vel = pygame.Vector2()
        self.dir = pygame.Vector2(1, 0)

        self.images:list[pygame.Surface] = images

        self.draw_outline = False

        self.rect = self.images[0].get_rect()
        self.hitbox = pygame.FRect(0, 0, 9, 9)

    def set_pos(self, pos):
        self.pos = pygame.Vector2(pos)
        self.rect.midbottom = self.pos
        self.hitbox.midbottom = self.pos

    def trail_collision_detect(self, trail, trail_step):

        colliding = False
        # sorted_sprites:list[TrailSegment] =  sorted(self.trail_grp.sprites(), key=lambda s: s.order)
        for i in range(len(trail)-2):
            x1, y1 = trail[i].rect.midbottom
            x2, y2 = trail[i+1].rect.midbottom
            x3, y3 = self.last_pos.xy
            x4, y4 = self.pos.xy

            if (abs(x1-x3) < trail_step*2 or \
                abs(x2-x3) < trail_step*2 or \
                abs(x1-x4) < trail_step*2 or \
                abs(x2-x4) < trail_step*2):

                colliding = line_line_collide(x1, x2, x3, x4, y1, y2, y3, y4)

            if colliding:
                return (x1+x2)/2, (y1+y2)/2

        return None
    
    def draw(self):

        # sprite
        size = round(max(self.images[0].size)*1.4142)
        canvas = pygame.Surface((size+2, len(self.images)+size+2), pygame.SRCALPHA)

        spread = 1
        for i, sprite in enumerate(self.images):
            sprite = pygame.transform.rotate(sprite, self.dir.angle_to((1, 0)))

            canvas.blit(sprite, (canvas.get_width()/2 - sprite.get_width()/2, canvas.get_height() - sprite.get_height()/2 - spread*i - size/2))

            # self.screen.blit(sprite, (self.pos.x - sprite.get_width()/2, self.pos.y - sprite.get_height()/2 - spread * i))

        # outline
        if self.draw_outline:
            black_sillo = canvas.copy()
            black_sillo.fill(0x0, special_flags=pygame.BLEND_RGB_MIN)
            for dg in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                canvas.blit(black_sillo, dg, special_flags=pygame.BLEND_RGBA_MAX)
        self.screen.blit(canvas, (self.pos.x - canvas.get_width()/2, self.pos.y - canvas.get_height() + size/2))

        pygame.draw.rect(self.master.debug.surface, "green", (self.pos.x - canvas.get_width()/2, self.pos.y - canvas.get_height() + size/2, *canvas.size), 1)
    
    def update(self):

        pass
        
