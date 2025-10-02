import pygame
from .config import *
from .engine import *
from .entity import Entity


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .master import Master

class Player(Entity):
    
    def __init__(self, master: "Master", grps):

        # images:list[pygame.Surface] = import_spritesheet("graphics/player", "player-32x32.png")
        images:list[pygame.Surface] = import_spritesheet("graphics/player", "RedMotorcycle-16x16.png")
        # images:list[pygame.Surface] = import_spritesheet("graphics/player", "biby-16x16.png")
        # images = [pygame.transform.rotate(img, 90) for img in images]

        super().__init__(master, grps, images)
        # self.draw_outline = True

        self.master.player = self

        self.input_dir = pygame.Vector2()
        self.speed = 1
        self.input = False
        self.acc = 0.1
        self.dcc = 0.06
        self.moving = False

        self.turning_speed = 4

        self.max_walls = None
        self.wall_remaining = None

        self.trail_step = 4
        self.trail_height = 8
        self.trail:list[TrailSegment] = []
        # self.master.level.trails.append(self.trail)
        self.trail_index = 0
        self.color = pygame.Color(0x00FFFFFF)

        self.trail3d_effect = pygame.Surface((max(self.trail_height, self.trail_step)+1, self.trail_height), pygame.SRCALPHA)
        col = pygame.Color(0x00000000)
        for y in range(self.trail3d_effect.get_height()):
            col.a = int(0.05 * 255 * y)
            for x in range(self.trail3d_effect.get_width()):
                self.trail3d_effect.set_at((x, y), col)

        self.trail_sprite = pygame.Surface(self.trail3d_effect.size)
        self.trail_sprite.fill(self.color)
        self.trail_sprite.blit(self.trail3d_effect)

        self.wall_sprite = pygame.Surface(self.trail3d_effect.size)
        self.wall_sprite.fill(0xAFAFAF)
        self.wall_sprite.blit(self.trail3d_effect)

        # self.trail_sprite_cache:dict[int, pygame.Surface] = {}
        # self.trail_timer = CustomTimer()
        # self.trail_timer.start(100, 0)

    def get_input(self):

        keys = pygame.key.get_pressed()

        self.input_dir.update()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.input_dir.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.input_dir.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.input_dir.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.input_dir.x += 1

        self.input = bool(self.input_dir.x or self.input_dir.y)

    def record_trail(self):

        if not pygame.key.get_pressed()[pygame.K_SPACE]:
            if len(self.trail) != 0 and self.trail[0] != None:
                self.trail.append(None)

        if self.pos.distance_squared_to(self.last_pos) >= self.trail_step**2:

            if self.wall_remaining > 0 and pygame.key.get_pressed()[pygame.K_SPACE]:
                self.wall_remaining -= 1
                x1, y1 = self.last_pos.xy
                x2, y2 = self.pos.xy
                x = min(x1, x2)
                y = min(y1, y2)-(self.trail_height)
                w = abs(x1-x2)+1
                # h = max(abs(y1-y2)+1, self.trail_height)
                h = self.trail_height
                w = round(w)
                h = round(h)

                dir = self.pos - self.last_pos

                # self.trail.append((x, y, w, h))
                trail = TrailSegment(self.screen, self.trail_sprite, x, y, w, h,
                                     dir, self.trail_index, [self.master.level.ysort_grp])
                self.trail.append(trail)
                self.trail_index += 1

            self.last_pos = self.pos.copy()

    def move(self):
        self.dir.rotate_ip(self.input_dir.x * self.turning_speed * self.master.dt)

        # self.vel.move_towards_ip(self.dir*self.speed, self.acc*self.master.dt)
        if self.input_dir.y < 0:
            self.vel.move_towards_ip(self.dir*self.speed, self.acc*self.master.dt)
        else:
            self.vel.move_towards_ip((0, 0), self.dcc*self.master.dt)

        # self.vel = self.dir * self.speed
        # try:
        #     self.dir = self.vel.normalize()
        # except ValueError:
        #     pass

        self.pos += self.vel * self.master.dt

        self.hitbox.midbottom = self.pos
        self.rect.midbottom = self.pos

    def draw(self):

        # # trail
        # for x, y, w, h in self.trail:
        #     self.screen.blit(self.trail_sprite, (x, y), (0, 0, w, h))
        # self.master.debug("Trail: ", len(self.trail))

        # player

        super().draw()

    def trail_collision_detect(self):

        colliding = super().trail_collision_detect(self.trail, self.trail_step)

        self.master.debug("Collision:", colliding)


    def update(self):
        
        self.get_input()

        self.record_trail()

        self.move()

        # for trail in self.master.level.trails:
        #     self.trail_coll_resolution(trail)

        # self.trail_collision_detect()
        
        # pygame.draw.rect(self.master.debug.surface, "green", self.hitbox, 1)
        self.master.debug("pos:", self.rect.center)
        self.master.debug("trail:", len(self.trail))
        self.master.debug("walls:", self.wall_remaining)


class TrailSegment(pygame.sprite.Sprite):

    def __init__(self, screen, image, x, y, w, h, dir, order, grps):
        
        super().__init__(grps)
        self.screen:pygame.Surface = screen
        self.image:pygame.Surface = image
        self.rect = pygame.Rect(x, y, w, h)
        self.dir:pygame.Vector2 = pygame.Vector2(dir)
        self.order = order

        self.deactivated = False

    def draw(self):

        self.screen.blit(self.image, (self.rect.x, self.rect.y), (0, 0, self.rect.w, self.rect.h))

