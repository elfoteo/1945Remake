import math

import pygame.font
from scripts import planes
from scripts.projectiles import *
from scripts.stats import Stats
from scripts.utils import *
from scripts.utils import _quit
from scripts.vfx import VFX
from array import array
import moderngl

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((440, 854), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface(screen.get_size())

clock = pygame.time.Clock()
DEBUG = False
if DEBUG:
    print("!!! THIS GAME IS RUNNING IN DEBUG MODE !!!")
enemy_shooter_6dir_img = pygame.image.load("sprites/enemies/enemy_shooter_6dir.png")
enemy_laser_img = pygame.image.load("sprites/enemies/enemy_laser.png")
# TODO: better healthbar
healthbar_img = pygame.transform.scale(pygame.image.load("sprites/ui/healthbar.png"), (290 / 2 * 1.2, 56 / 2 * 1.2))
enemy_normal_img = pygame.transform.scale(pygame.image.load("sprites/enemies/enemy_normal.png"),
                                          (110 / 4 * 2.5, 90 / 4 * 2.5))
enemy_projectile_img = pygame.image.load("sprites/bombs/bullet_bomb/projectile.png")
enemy_normal2_frames = load_animation_frames("sprites/enemies/enemy_normal2")
rotating_enemy_frames = load_animation_frames("sprites/enemies/rotating_enemy")
following_enemy_img = pygame.image.load("sprites/enemies/following_enemy.png")
bullet_bomb_frames = load_animation_frames("sprites/bombs/bullet_bomb")
nuclear_bomb_frames = load_animation_frames("sprites/bombs/nuclear_bomb")
death_frames = load_animation_frames("sprites/vfx/explosion")
coin1_frames = load_animation_frames("sprites/coins/1")
coin5_frames = load_animation_frames("sprites/coins/5")
ingame_coins_img = pygame.transform.scale_by(pygame.image.load("sprites/ui/ingame_coin.png"), 0.8)
win_tail_r = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/tail.png"), 1)
win_front_r = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/front.png"), 1)
win_shadow_r = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/shadow.png"), 1)
win_tail_l = pygame.transform.flip(win_tail_r, True, False)
win_shadow_l = pygame.transform.flip(win_shadow_r, True, False)
win_front_l = pygame.transform.flip(win_front_r, True, False)
win_label = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/victory_label.png"), 1.2)

eagle_head = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/eagle_head.png"), 1.2)
eagle_wing_r = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/eagle_wing.png"), 1.2)
eagle_wing_bottom_r = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/eagle_wing_bottom.png"), 1.2)
eagle_wing_l = pygame.transform.flip(eagle_wing_r, True, False)
eagle_wing_bottom_l = pygame.transform.flip(eagle_wing_bottom_r, True, False)
win_star_circle = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/star_circle.png"), 1.2)
win_star = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/star.png"), 1.2)
level_banner = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/level_banner.png"), 1.2)
pass_lvl_button = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/pass_lvl_button.png"), 1)
level_rewards_bg = pygame.transform.scale_by(pygame.image.load("sprites/ui/level/rewards_bg.png"), 1)

ui_background = pygame.transform.scale(pygame.image.load("sprites/ui/ui_background.png"), display.get_size())
pygame.display.set_caption("1945 Remake")
visual_effects = []
user_stats = Stats()
scroll_speed = 1
coins = []
font = pygame.font.Font("font/font.ttf", 30)

shader_time = 0


# TODO: Fix image imports
# TODO: screen sake effect


def quit_game():
    user_stats.save()
    _quit()


class Shader:
    def __init__(self):
        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,  # topright
            -1.0, -1.0, 0.0, 1.0,  # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))
        print("Loading shaders...")
        with open("shaders/vertex.vert") as shader_file:
            self.vert_shader = shader_file.read()
        with open("shaders/frag.frag") as shader_file:
            self.frag_shader = shader_file.read()
        print("Shaders loaded")
        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def get_ctx(self):
        return self.ctx

    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

    def draw(self, program_args: dict):
        frame_tex = self.surf_to_texture(display)
        frame_tex.use(0)
        for arg in program_args:
            self.program[arg] = program_args[arg]

        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        pygame.display.flip()
        frame_tex.release()


class Mouse:
    def __init__(self):
        self.rel = [0, 0]
        self.mouse_grabbed = True
        self.mouse_visible = False

    def set_grab(self, toggle):
        pygame.event.set_grab(toggle)
        self.mouse_grabbed = toggle

    def set_visible(self, toggle):
        pygame.mouse.set_visible(toggle)
        self.mouse_visible = toggle

    def unlock(self):
        self.set_grab(False)
        self.set_visible(True)

    def lock(self):
        self.set_grab(True)
        self.set_visible(False)

    def draw(self):
        self.rel = pygame.mouse.get_rel()


class Player:
    def __init__(self):
        self.coins_pickup_distance = 100
        self.pos = [150, 250]
        self.abs_pos = self.pos
        self.window = pygame.Rect((0, 0,
                                   display.get_width(),
                                   display.get_height()))
        self.plane = planes.P_61_Black_Widow(visual_effects)
        self.average_motion_x = 0
        self.motion_history = []

    def draw_healthbar(self):
        display.blit(healthbar_img, (10, 10))
        rect = pygame.Rect(10 + 266 / 2 * 1.2, 11 + 22 / 2 * 1.2,
                           -(215 / 2 * 1.2) * (max(self.plane.health / self.plane.max_health, 0) * -1 + 1),
                           21 / 2 * 1.2 - 1)
        rect.normalize()
        pygame.draw.rect(display, (120, 120, 120), rect)
        if self.plane.health <= 0:
            self.plane.alive = False

    @staticmethod
    def draw_coins():
        display.blit(ingame_coins_img, (display.get_width() - 50, 150))
        text = outlined_text(str(user_stats.data["ingame_coins"]), font)
        display.blit(text, (display.get_width() - 50 - text.get_width(), 150))

    def draw(self):
        mx, my = mouse.rel

        if pygame.mouse.get_pressed()[0]:
            self.motion_history.append([mx, time.time()])
        else:
            self.motion_history.append([0, time.time()])
        for i in self.motion_history:
            if i[1] + 0.7 <= time.time():
                self.motion_history.remove(i)

        first_values = [x[0] for x in self.motion_history]
        self.average_motion_x = sum(first_values) / len(first_values)

        if pygame.mouse.get_pressed()[0] and self.window.collidepoint((self.pos[0] + mx, self.pos[1])):
            self.pos[0] += mx
        if pygame.mouse.get_pressed()[0] and self.window.collidepoint((self.pos[0], self.pos[1] + my)):
            self.pos[1] += my
        self.abs_pos = (self.pos[0] - self.plane.image.get_width() / 2, self.pos[1] - self.plane.image.get_height() / 2)
        self.plane.update(self.average_motion_x, display, enemies, self.abs_pos)

        display.blit(self.plane.image,
                     (self.pos[0] - self.plane.image.get_width() / 2, self.pos[1] - self.plane.image.get_height() / 2))
        if DEBUG:
            for box in self.plane.hitbox:
                pygame.draw.rect(display, (255, 0, 0), (self.abs_pos[0] + box.x, self.abs_pos[1] + box.y, box.w, box.h))
        self.draw_healthbar()
        self.draw_coins()


class Coin:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos
        if self.value == 1:
            self.frames = coin1_frames
        elif self.value == 5:
            self.frames = coin5_frames
        else:
            raise ValueError("Invalid coins value")
        self.index = 0
        self.last_frame = time.time() * 1000
        self.delay = 120
        self.abs_pos = (self.pos[0] - self.frames[self.index].get_width() / 2,
                        self.pos[1] - self.frames[self.index].get_height() / 2)
        self.alive = True
        self.picking_up = False

    def draw(self):
        self.abs_pos = (self.pos[0] + self.frames[self.index].get_width() / 2,
                        self.pos[1] + self.frames[self.index].get_height() / 2)
        if self.alive:
            self.pos[1] += scroll_speed
            if self.last_frame + self.delay < time.time() * 1000:
                if self.index + 1 >= len(self.frames):
                    self.index = 0
                else:
                    self.index += 1
                self.last_frame = time.time() * 1000
            display.blit(self.frames[self.index], self.pos)
            if self.pos[1] > display.get_height() + 30:
                self.alive = False

            if distance_between_points(player.pos, self.abs_pos) < player.coins_pickup_distance:
                self.picking_up = True
            if self.picking_up:
                self.pos[0] += (player.pos[0] - self.abs_pos[0]) / 14
                self.pos[1] += (player.pos[1] - self.abs_pos[1]) / 14
            if distance_between_points(player.pos, self.abs_pos) < 25 and self.alive:
                user_stats.add_ingame_coins(self.value)
                self.alive = False


class Enemy:
    def __init__(self, speed, health, enemy_projectiles, image, pos, hitbox, auto_shoot=True,
                 particles_on_death=True):
        self.speed = speed
        self.health = health
        self.max_health = health
        self.projectiles: EnemyProjectiles = enemy_projectiles
        self.image = image
        self.pos = pos
        self.hitbox = hitbox
        self.alive = True
        self.particles_on_death = particles_on_death
        self.auto_shoot = auto_shoot

    def collide(self, rect) -> bool:
        for hitbox in self.hitbox:
            if pygame.Rect(self.pos[0] + hitbox.x, self.pos[1] + hitbox.y,
                           hitbox.w, hitbox.h).colliderect(rect):
                return True
        return False

    def draw_health_bar(self):
        if self.health < self.max_health:
            pygame.draw.rect(display, (80, 80, 80),
                             (self.pos[0] + self.image.get_width() / 4, self.pos[1] + self.image.get_height() + 5,
                              self.image.get_width() / 4 * 2, 5))
            pygame.draw.rect(display, (216, 13, 0),
                             (self.pos[0] + self.image.get_width() / 4, self.pos[1] + self.image.get_height() + 5,
                              (self.image.get_width() / 4 * 2) * (self.health / self.max_health), 5))

    def on_death(self):
        coins.append(Coin(1, [self.pos[0], self.pos[1]]))
        if self.particles_on_death:
            visual_effects.append(
                VFX(death_frames, self.pos[0] + self.image.get_width() / 4, self.pos[1] + self.image.get_height() + 5,
                    delay=10))

    def draw(self):
        self.pos[1] += self.speed
        if self.health <= 0 and self.alive:
            self.alive = False
            self.on_death()
        if self.alive:
            display.blit(self.image, self.pos)
        if self.alive and self.pos[1] >= 0 and self.auto_shoot:
            self.projectiles.shoot(self.pos[0], self.pos[1])
        self.projectiles.draw(display, player)
        if self.alive:
            self.draw_health_bar()
            if self.pos[1] >= display.get_height() + self.image.get_height() + 100:
                self.alive = False
            for p_box in player.plane.hitbox:
                if self.collide((player.abs_pos[0] + p_box.x, player.abs_pos[1] + p_box.y, p_box.w, p_box.h)):
                    # TODO: Explosion
                    player.plane.health -= self.health
                    self.health = 0
            if DEBUG:
                for box in self.hitbox:
                    pygame.draw.rect(display, (255, 0, 0), (self.pos[0] + box.x, self.pos[1] + box.y, box.w, box.h))


class NormalEnemy(Enemy):
    def __init__(self, speed, pos):
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        image = enemy_normal_img
        health = 75
        hitbox = [pygame.Rect((round(47 / 4 * 2.5), round(3 / 4 * 2.5), round(16 / 4 * 2.5), round(87 / 4 * 2.5))),
                  pygame.Rect((round(0 / 4 * 2.5), round(44 / 4 * 2.5), round(110 / 4 * 2.5), round(22 / 4 * 2.5)))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox)


class NormalEnemy2(Enemy):
    def __init__(self, pos):
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        image = enemy_normal2_frames[0]
        health = 35
        speed = 1
        self.frame_delay = 120
        self.next_frame = time.time() * 1000
        self.frame_index = 0
        hitbox = [pygame.Rect((round(31 / 4 * 3), round(0 / 4 * 3), round(11 / 4 * 3), round(56 / 4 * 3))),
                  pygame.Rect((round(0 / 4 * 3), round(25 / 4 * 3), round(73 / 4 * 3), round(18 / 4 * 3)))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox)

    def draw(self):
        if self.next_frame + self.frame_delay <= time.time() * 1000:
            self.next_frame = time.time() * 1000
            self.frame_index += 1
            if self.frame_index >= 2:
                self.frame_index = 0
            self.image = enemy_normal2_frames[self.frame_index]
        super().draw()


class FollowingEnemy(Enemy):
    def __init__(self, pos):
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        image = following_enemy_img
        health = 35
        speed = 2
        self.base_speed = speed * 2
        self.frame_delay = 120
        self.next_frame = time.time() * 1000
        self.frame_index = 0
        self.base_image = image
        self.current_angle = 0
        hitbox = [pygame.Rect((0, 25, 55, 27)),
                  pygame.Rect((15, 0, 25, 69))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox)

    def draw(self):
        if display.get_rect().colliderect(
                pygame.Rect(self.hitbox[0].x+self.pos[0], self.hitbox[0].y+self.pos[1],
                            self.hitbox[0].w, self.hitbox[0].h)):
            self.speed = 0
        if self.speed == 0:
            if self.pos[1] > player.pos[1]:
                angle = 90
            else:
                angle = angle_between_points(self.pos, player.pos)
            self.current_angle += (angle-self.current_angle)/15
            motion = angle_to_motion(self.current_angle, self.base_speed)
            if self.pos[1] < player.pos[1]:
                self.pos[0] += motion[0]
            self.pos[1] += self.base_speed
            self.image = pivot_rotate(self.base_image, self.current_angle-90, (self.base_image.get_width()/2,
                                                                                  self.base_image.get_height()/2),
                                      pygame.Vector2(0, 0))[0]
        super().draw()


class RotatingEnemy(Enemy):
    def __init__(self, pos):
        enemy_projectiles = RotatingEnemyProjectiles(display)
        image = rotating_enemy_frames[0]
        health = 35
        speed = 1.5
        self.frame_delay = 140
        self.next_frame = time.time() * 1000
        self.frame_index = 0
        self.current_image = image
        hitbox = [pygame.Rect((0, 0, 76, 31)),
                  pygame.Rect((32, 3, 12, 65))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox)

    def draw(self):
        if self.next_frame + self.frame_delay <= time.time() * 1000:
            self.next_frame = time.time() * 1000
            self.frame_index += 1
            if self.frame_index >= len(rotating_enemy_frames):
                self.frame_index = 0
            self.current_image = rotating_enemy_frames[self.frame_index]
        # Draw
        self.pos[1] += self.speed
        if self.health <= 0 and self.alive:
            self.alive = False
            self.on_death()
        if self.alive:
            display.blit(self.current_image,
                         (self.pos[0] - self.current_image.get_width() / 2 + self.image.get_width() / 2,
                          self.pos[1]))
        if self.alive and self.pos[1] >= 0 and self.auto_shoot:
            self.projectiles.shoot(self.pos[0], self.pos[1])
        self.projectiles.draw(display, player)
        if self.alive:
            self.draw_health_bar()
            if self.pos[1] >= display.get_height() + self.image.get_height() + 100:
                self.alive = False
            for p_box in player.plane.hitbox:
                if self.collide((player.abs_pos[0] + p_box.x, player.abs_pos[1] + p_box.y, p_box.w, p_box.h)):
                    # TODO: Explosion
                    player.plane.health -= self.health
                    self.health = 0
            if DEBUG:
                for box in self.hitbox:
                    pygame.draw.rect(display, (255, 0, 0), (self.pos[0] + box.x, self.pos[1] + box.y, box.w, box.h))


class LaserEnemy(Enemy):  # TODO
    def __init__(self, pos):
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        self.image_scale = 0.75
        image = pygame.transform.scale_by(enemy_laser_img, self.image_scale)
        health = 35
        speed = 1
        hitbox = [pygame.Rect((round(14 * self.image_scale), round(13 * self.image_scale),
                               round(86 * self.image_scale), round(85 * self.image_scale)))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox, auto_shoot=False)
        self.laser_cooldown = 6000
        self.laser_duration = 2000
        self.laser_active = True
        self.last_shoot = time.time() * 1000

    def draw(self):
        super().draw()
        if self.laser_active:
            rect_l = pygame.Rect(-display.get_width(), self.pos[1] + (52 * self.image_scale),
                                 -display.get_width() - self.pos[0], 9 * self.image_scale)
            rect_r = pygame.Rect(self.pos[0] + (113 * self.image_scale), self.pos[1] + (52 * self.image_scale),
                                 display.get_width() - self.pos[0], 9 * self.image_scale)
            pygame.draw.rect(display, (255, 0, 0), rect_l)
            pygame.draw.rect(display, (255, 0, 0), rect_r)


class EnemyShooter6Dir(Enemy):
    def __init__(self, pos):
        img_scale = 0.75
        enemy_projectiles = Enemy6DirProjectiles(display)
        image = pygame.transform.scale_by(enemy_shooter_6dir_img, img_scale)
        health = 55
        speed = 1
        hitbox = [
            pygame.Rect((round(0 * img_scale), round(36 * img_scale), round(96 * img_scale), round(14 * img_scale))),
            pygame.Rect((round(25 * img_scale), round(1 * img_scale), round(45 * img_scale), round(63 * img_scale)))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox)

    def draw(self):
        self.pos[1] += self.speed
        if self.health <= 0 and self.alive:
            self.alive = False
            self.on_death()
        if self.alive:
            display.blit(self.image, self.pos)
        if self.alive and self.pos[1] >= 0 and self.auto_shoot:
            self.projectiles.shoot(self.pos[0] + self.image.get_width() / 2, self.pos[1] + self.image.get_height() / 2)
        self.projectiles.draw(display, player)
        if self.alive:
            self.draw_health_bar()
            if self.pos[1] >= display.get_height() + self.image.get_height() + 100:
                self.alive = False
            for p_box in player.plane.hitbox:
                if self.collide((player.abs_pos[0] + p_box.x, player.abs_pos[1] + p_box.y, p_box.w, p_box.h)):
                    # TODO: Explosion
                    player.plane.health -= self.health
                    self.health = 0
            if DEBUG:
                for box in self.hitbox:
                    pygame.draw.rect(display, (255, 0, 0), (self.pos[0] + box.x, self.pos[1] + box.y, box.w, box.h))


class BulletBomb(Enemy):
    def __init__(self, pos):
        speed = 1
        health = 30
        enemy_projectiles = BombProjectiles(display)
        image = bullet_bomb_frames[0]
        self.image_scale = 1
        self.next_frame = time.time() * 1000
        self.frame_index = 0
        self.frame_delay = 150
        hitbox = [
            pygame.Rect(0 * self.image_scale, 11 * self.image_scale, 70 * self.image_scale, 72 * self.image_scale)
        ]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox, auto_shoot=False)

    def on_death(self):
        self.projectiles.shoot(self.pos[0], self.pos[1])
        super().on_death()

    def draw(self):
        if self.next_frame + self.frame_delay <= time.time() * 1000:
            self.next_frame = time.time() * 1000
            self.frame_index += 1
            if self.frame_index >= 5:
                self.frame_index = 0
            self.image = bullet_bomb_frames[self.frame_index]
        super().draw()


class NuclearBomb(Enemy):
    def __init__(self, pos):
        speed = 1
        health = 30
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        image = nuclear_bomb_frames[0]
        self.image_scale = 1
        self.next_frame = time.time() * 1000
        self.frame_index = 0
        self.frame_delay = 250
        hitbox = [
            pygame.Rect(0 * self.image_scale, 0 * self.image_scale, 33 * self.image_scale, 83 * self.image_scale)
        ]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox, auto_shoot=False,
                         particles_on_death=False)

    def on_death(self):

        for enemy in enemies:
            if distance_between_points(enemy.pos, self.pos) <= 350:
                enemy.health -= distance_between_points(enemy.pos, self.pos) * -1 + 400

        if distance_between_points(player.pos, self.pos) <= 350:
            player.plane.health -= distance_between_points(player.pos, self.pos) * -1 + 385

        anim = []
        for i in death_frames:
            anim.append(pygame.transform.scale_by(i, 2.5))
        visual_effects.append(
            VFX(anim, self.pos[0] + self.image.get_width() / 4, self.pos[1] + self.image.get_height() + 5,
                delay=10))
        del anim
        super().on_death()

    def draw(self):
        if self.next_frame + self.frame_delay <= time.time() * 1000:
            self.next_frame = time.time() * 1000
            self.frame_index += 1
            if self.frame_index >= 5:
                self.frame_index = 0
            self.image = nuclear_bomb_frames[self.frame_index]
        super().draw()


shader = Shader()
mouse = Mouse()
player = Player()
enemies = []
