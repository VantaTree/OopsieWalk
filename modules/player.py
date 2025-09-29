import pygame
from .config import *
from .engine import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .master import Master

class Player(pygame.sprite.Sprite):
    
    def __init__(self, master: "Master", grps, /, main_player=False):

        super().__init__(grps)

        self.master = master
        self.master.player = self
        self.screen:pygame.Surface = self.master.app.screen

        self.main_player = main_player

        self.pos = pygame.Vector2(100, 100)
        self.vel = pygame.Vector2()
        self.dir = pygame.Vector2(1, 0)
        self.input_dir = pygame.Vector2()
        self.speed = 1
        self.input = False
        self.acc = 0.1
        self.dcc = 0.06
        self.moving = False

        self.turning_speed = 4

        # self.images:list[pygame.Surface] = import_spritesheet("graphics/player", "player-32x32.png")
        self.images:list[pygame.Surface] = import_spritesheet("graphics/player", "RedMotorcycle-16x16.png")
        # self.images:list[pygame.Surface] = import_spritesheet("graphics/player", "biby-16x16.png")
        # self.images = [pygame.transform.rotate(img, 90) for img in self.images]

        self.draw_outline = False

        self.rect = self.images[0].get_rect(midbottom=self.pos)
        self.hitbox = pygame.FRect(0, 0, 9, 9)
        self.hitbox.midbottom = self.pos
        self.color = pygame.Color(0x00FFFFFF)

        self.trail_step = 4
        self.trail_height = 8
        self.trail:list[TrailSegment] = []
        # self.trail_grp = CustomGroup()
        self.trail_index = 0

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
        self.last_pos = self.pos.copy()

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

        if self.pos.distance_squared_to(self.last_pos) >= self.trail_step**2:

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                x1, y1 = self.last_pos.xy
                x2, y2 = self.pos.xy
                x = min(x1, x2)
                y = min(y1, y2)-(self.trail_height)
                w = abs(x1-x2)+1
                # h = max(abs(y1-y2)+1, self.trail_height)
                h = self.trail_height
                w = round(w)
                h = round(h)

                # self.trail.append((x, y, w, h))
                trail = TrailSegment(self.screen, self.trail_sprite, self.wall_sprite,
                                     x, y, w, h, self.trail_index, [self.master.game.ysort_grp])
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

    def trail_collision_detect(self):

        colliding = False
        # sorted_sprites:list[TrailSegment] =  sorted(self.trail_grp.sprites(), key=lambda s: s.order)
        for i in range(len(self.trail)-2):
            x1, y1 = self.trail[i].rect.midbottom
            x2, y2 = self.trail[i+1].rect.midbottom
            x3, y3 = self.last_pos.xy
            x4, y4 = self.pos.xy

            if (abs(x1-x3) < self.trail_step*2 or \
                abs(x2-x3) < self.trail_step*2 or \
                abs(x1-x4) < self.trail_step*2 or \
                abs(x2-x4) < self.trail_step*2):

                colliding = line_line_collide(x1, x2, x3, x4, y1, y2, y3, y4)

            if colliding:
                # aaaaaah
                self.trail[i].deactivate()
                self.trail[i+1].deactivate()
                break

        self.master.debug("Collision:", colliding)


    def update(self):
        
        self.get_input()

        self.record_trail()

        self.move()

        self.trail_collision_detect()
        
        # pygame.draw.rect(self.master.debug.surface, "green", self.hitbox, 1)
        self.master.debug("pos:", self.rect.center)
        self.master.debug("trail:", len(self.trail))


class TrailSegment(pygame.sprite.Sprite):

    def __init__(self, screen, image, wall_img, x, y, w, h, order, grps):
        
        super().__init__(grps)
        self.screen:pygame.Surface = screen
        self.original_img:pygame.Surface = image
        self.image:pygame.Surface = image
        self.wall_img:pygame.Surface = wall_img
        self.rect = pygame.Rect(x, y, w, h)
        self.order = order

        self.deactivated = False

    def deactivate(self):
        self.deactivated = True
        self.image = self.wall_img

    def reactivate(self):
        self.deactivated = False
        self.image = self.original_img_img

    def draw(self):

        self.screen.blit(self.image, (self.rect.x, self.rect.y), (0, 0, self.rect.w, self.rect.h))

