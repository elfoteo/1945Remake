import math
import random
import time

import pygame

from scripts.utils import *
from scripts.vfx import VFX
from scripts.shader import Shader

vfx_shoot_scale = 0.2
vfx_hit_scale = 0.1
shoot_frames = None
hit_frames = None
normal_enemy_projectile = None
bullet_bomb_projectile = None
shader: Shader = None


def init(shader_):
    global shoot_frames, hit_frames, normal_enemy_projectile, bullet_bomb_projectile, shader
    shader = shader_
    shoot_frames = load_animation_frames("sprites/vfx/shoot", vfx_shoot_scale)
    hit_frames = load_animation_frames("sprites/vfx/hit", vfx_hit_scale)
    normal_enemy_projectile = load_image("sprites/enemies/enemy_projectile.png")
    bullet_bomb_projectile = load_image("sprites/bombs/bullet_bomb/projectile.png")


class Projectiles:
    def __init__(self, guns, image, speed=4, cooldown=350, dmg=15, vfx=None, anchor=None):
        if vfx is None:
            vfx = []
            self.use_vfx = False
        else:
            self.use_vfx = True
        self.projectiles = []
        self.cooldown = cooldown
        self.last_shoot = shader.get_time()
        self.guns = guns
        self.projectile_speed = speed
        self.dmg = dmg
        self.image = image
        self.vfx = vfx
        self.vfx_shoot_scale = 0.2
        self.vfx_hit_scale = 0.1
        self.shoot_frames = shoot_frames
        self.hit_frames = hit_frames
        self.anchor = anchor

    def shoot(self, x, y):
        if shader.get_time() > self.last_shoot + self.cooldown:
            for gun in self.guns:
                self.projectiles.append([x + gun[0], y + gun[1], angle_to_motion(gun[2], self.projectile_speed),
                                         pygame.transform.rotate(self.image, -gun[2] - 270)])
                self.vfx.append(VFX(self.shoot_frames,
                                    gun[0] + x,
                                    gun[1] + y,
                                    anchor=self.anchor,
                                    offset=gun,
                                    no_rotation=True))
            self.last_shoot = shader.get_time()

    def draw(self, screen, enemies):
        new_proj = self.projectiles.copy()
        for projectile in self.projectiles:
            removed = False
            projectile[1] -= projectile[2][1]
            projectile[0] -= projectile[2][0]
            screen.blit(projectile[3], (projectile[0] - projectile[3].get_width() / 2,
                                        projectile[1] - projectile[3].get_height() / 2))
            if projectile[1] <= -50 and not removed:
                new_proj.remove(projectile)
                removed = True
            for enemy in enemies:
                if enemy.collide((
                        projectile[0] - projectile[3].get_width() / 2,
                        projectile[1] - projectile[3].get_height() / 2,
                        projectile[3].get_width(),
                        projectile[3].get_height())) and enemy.alive:
                    enemy.health -= self.dmg
                    self.vfx.append(VFX(self.hit_frames,
                                        projectile[0] - projectile[3].get_width() / 2,
                                        projectile[1] - projectile[3].get_height() / 2, delay=10))
                    if not removed:
                        try:
                            new_proj.remove(projectile)
                        except:
                            pass
        self.projectiles = new_proj.copy()
        del new_proj


class DelanneProjectiles(Projectiles):
    def __init__(self, guns, center_image, side_image, speed=4, cooldown=350, dmg=15, vfx=None, anchor=None):
        super().__init__(guns, center_image, speed, cooldown, dmg, vfx, anchor)
        if vfx is None:
            vfx = []
            self.use_vfx = False
        else:
            self.use_vfx = True
        self.projectiles = []
        self.cooldown = cooldown
        self.last_shoot = shader.get_time()
        self.guns = guns
        self.projectile_speed = speed
        self.dmg = dmg
        self.center_image = center_image
        self.left_image = pygame.transform.flip(side_image, True, False)
        self.right_image = side_image
        self.vfx = vfx
        self.vfx_shoot_scale = 0.2
        self.vfx_hit_scale = 0.1
        self.shoot_frames = shoot_frames
        self.hit_frames = hit_frames

    def shoot(self, x, y):

        if shader.get_time() > self.last_shoot + self.cooldown:
            gun_index = 0
            for gun in self.guns:
                if gun_index == 1:
                    self.projectiles.append([x + gun[0], y + gun[1], angle_to_motion(gun[2], self.projectile_speed),
                                             pygame.transform.rotate(self.center_image, -gun[2] - 270)])
                    self.vfx.append(VFX(self.shoot_frames,
                                        gun[0] + x,
                                        gun[1] + y,
                                        anchor=self.anchor,
                                        offset=gun, no_rotation=True))
                elif gun_index == 0:
                    self.projectiles.append([x + gun[0], y + gun[1], angle_to_motion(gun[2], self.projectile_speed),
                                             pygame.transform.rotate(self.left_image, -gun[2] - 270)])

                    self.vfx.append(VFX(self.shoot_frames,
                                        gun[0] + x,
                                        gun[1] + y,
                                        anchor=self.anchor,
                                        offset=gun, no_rotation=True))
                elif gun_index == 2:
                    self.projectiles.append([x + gun[0], y + gun[1], angle_to_motion(gun[2], self.projectile_speed),
                                             pygame.transform.rotate(self.right_image, -gun[2] - 270)])
                    self.vfx.append(VFX(self.shoot_frames,
                                        gun[0] + x,
                                        gun[1] + y,
                                        anchor=self.anchor,
                                        offset=gun, no_rotation=True))
                gun_index += 1
            self.last_shoot = shader.get_time()

    def draw(self, screen, enemies):
        new_proj = self.projectiles.copy()
        for projectile in self.projectiles:
            removed = False
            projectile[1] -= projectile[2][1]
            projectile[0] -= projectile[2][0]
            screen.blit(projectile[3], (projectile[0] - projectile[3].get_width() / 2,
                                        projectile[1] - projectile[3].get_height() / 2))
            if projectile[1] <= -50 and not removed:
                new_proj.remove(projectile)
                removed = True
            for enemy in enemies:
                if enemy.collide((
                        projectile[0] - projectile[3].get_width() / 2,
                        projectile[1] - projectile[3].get_height() / 2,
                        projectile[3].get_width(),
                        projectile[3].get_height())) and enemy.alive:
                    enemy.health -= self.dmg
                    self.vfx.append(VFX(self.hit_frames,
                                        projectile[0] - projectile[3].get_width() / 2,
                                        projectile[1] - projectile[3].get_height() / 2, delay=10))
                    if not removed:
                        new_proj.remove(projectile)
        self.projectiles = new_proj.copy()
        del new_proj


class TrailProjectiles(Projectiles):
    def __init__(self, guns, image, trail_img, speed=4, cooldown=350, dmg=15, vfx=None, anchor=None):
        super().__init__(guns, image, speed, cooldown, dmg, vfx, anchor)
        if vfx is None:
            vfx = []
        self.trail_img: pygame.Surface = pygame.transform.scale_by(trail_img, 0.5).convert_alpha()
        self.trail_length = 5
        self.vfx = vfx
        self.delay = 20

    def shoot(self, x, y):
        if shader.get_time() > self.last_shoot + self.cooldown:
            gun_index = 0
            for gun in self.guns:
                trail_data = []
                for i in range(self.trail_length):
                    trail_data.append([shader.get_time() + i * self.delay, i + 1, False])
                self.projectiles.append([x + gun[0], y + gun[1], angle_to_motion(gun[2], self.projectile_speed),
                                         pygame.transform.rotate(self.image, -gun[2] - 270),
                                         trail_data, False, gun_index, (x, y)])
                self.vfx.append(VFX(self.shoot_frames,
                                    gun[0] + x,
                                    gun[1] + y,
                                    anchor=self.anchor,
                                    offset=gun, no_rotation=True))
                gun_index += 1
            self.last_shoot = shader.get_time()

    def draw(self, screen, enemies):
        new_proj = self.projectiles.copy()
        for projectile in self.projectiles:
            removed = False
            projectile[1] -= projectile[2][1]
            projectile[0] -= projectile[2][0]
            if not projectile[5]:
                screen.blit(projectile[3], (projectile[0] - projectile[3].get_width() / 2,
                                            projectile[1] - projectile[3].get_height() / 2))
            # offset_y = 0
            # alpha = 255
            # for i in range(self.trail_length):
            #     offset_y += self.trail_img.get_height() + 2
            #     tmp_img = self.trail_img.copy()
            #     tmp_img.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            #     screen.blit(tmp_img, (projectile[0] - tmp_img.get_width() / 2,
            #                           projectile[1] - tmp_img.get_height() / 2 + offset_y))
            #     alpha -= 51
            alpha = 255
            for trail in projectile[4]:
                offset_y = (self.trail_img.get_height() + 2) * trail[1]
                if trail[0] < shader.get_time():
                    tmp_img = self.trail_img.copy()
                    tmp_img.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                    screen.blit(tmp_img, (projectile[0] - tmp_img.get_width() / 2,
                                          projectile[1] - tmp_img.get_height() / 2 + offset_y))
                    if not trail[2]:
                        trail[2] = True
                        if self.use_vfx:
                            self.vfx.append(VFX(self.shoot_frames,
                                                self.guns[projectile[6]][0],
                                                self.guns[projectile[6]][1],
                                                anchor=self.anchor,
                                                offset=self.guns[projectile[6]], no_rotation=True))

                    if trail[2]:
                        for enemy in enemies:
                            if enemy.collide((
                                    projectile[0] - tmp_img.get_width() / 2,
                                    projectile[1] - tmp_img.get_height() / 2 + offset_y,
                                    tmp_img.get_width(),
                                    tmp_img.get_height())) and enemy.alive:
                                enemy.health -= self.dmg / (trail[1] + 1)
                                if self.use_vfx:
                                    self.vfx.append(VFX(self.hit_frames,
                                                        projectile[0],
                                                        projectile[1] + offset_y, delay=10))
                                try:
                                    projectile[4].remove(trail)
                                except:
                                    pass

                alpha -= 51

            if projectile[1] <= -50 and not removed and not projectile[5]:
                new_proj.remove(projectile)
            if projectile[1] <= -75:
                projectile[5] = True
            if not projectile[5] and not removed:
                for enemy in enemies:
                    if enemy.collide((
                            projectile[0] - projectile[3].get_width() / 2,
                            projectile[1] - projectile[3].get_height() / 2,
                            projectile[3].get_width(),
                            projectile[3].get_height())) and enemy.alive:
                        enemy.health -= self.dmg
                        self.vfx.append(VFX(self.hit_frames,
                                            projectile[0],
                                            projectile[1], delay=10))
                        projectile[5] = True
            if not projectile[4] and projectile[5]:
                new_proj.remove(projectile)
        self.projectiles = new_proj.copy()
        del new_proj


class BlackWidowProjectiles(Projectiles):
    def __init__(self, guns, image, speed, cooldown, dmg, vfx, image_scale, anchor=None):
        self.image_scale = image_scale
        super().__init__(guns, image, speed, cooldown, dmg, vfx, anchor)

    def shoot(self, x, y):
        if shader.get_time() > self.last_shoot + self.cooldown:
            for gun in self.guns:
                c = 0
                for i in range(3):
                    self.projectiles.append([x + gun[0],
                                             y + gun[1],
                                             angle_to_motion(gun[2], self.projectile_speed),
                                             pygame.transform.rotate(self.image, -gun[2] - 270),
                                             c,
                                             shader.get_time(),
                                             False,
                                             [gun[0], gun[1], x, y],
                                             False if gun[0] > 99 * self.image_scale else True,
                                             0])
                    c += 250
            self.last_shoot = shader.get_time()

    def draw(self, screen, enemies, abs_pos=any):
        new_proj = self.projectiles.copy()
        for projectile in self.projectiles:
            if shader.get_time() > projectile[5] + projectile[4]:
                removed = False
                if not projectile[6]:
                    self.vfx.append(VFX(self.shoot_frames,
                                        abs_pos[0] + projectile[7][0],
                                        abs_pos[1] + projectile[7][1],
                                        anchor=self.anchor,
                                        offset=projectile[7], no_rotation=True))
                    projectile[0] = abs_pos[0] + projectile[7][0]
                    projectile[1] = abs_pos[1] + projectile[7][1]
                    projectile[7][2] = abs_pos[0]
                    projectile[7][3] = abs_pos[1]
                    projectile[6] = True

                projectile[1] -= projectile[2][1]
                projectile[0] -= projectile[2][0]
                projectile[3] = pygame.transform.rotate(self.image, -angle_between_points(
                    (projectile[7][0] + projectile[7][2], projectile[7][1] + projectile[7][3]),
                    (projectile[0], projectile[1])) - 270)
                projectile[9] += 0.05
                if projectile[8]:
                    projectile[0] -= math.sin(projectile[9]) * 2 - 1
                else:
                    projectile[0] += math.sin(projectile[9]) * 2 - 1
                screen.blit(projectile[3], (projectile[0] - projectile[3].get_width() / 2,
                                            projectile[1] - projectile[3].get_height() / 2))
                if projectile[1] <= -50 and not removed:
                    new_proj.remove(projectile)
                    removed = True
                for enemy in enemies:
                    if enemy.collide((
                            projectile[0] - projectile[3].get_width() / 2,
                            projectile[1] - projectile[3].get_height() / 2,
                            projectile[3].get_width(),
                            projectile[3].get_height())) and enemy.alive:
                        enemy.health -= self.dmg
                        self.vfx.append(VFX(self.hit_frames,
                                            projectile[0] - projectile[3].get_width() / 2,
                                            projectile[1] - projectile[3].get_height() / 2, delay=10))
                        if not removed:
                            try:
                                new_proj.remove(projectile)
                            except:
                                pass
        self.projectiles = new_proj.copy()
        del new_proj


class EnemyProjectiles:
    def __init__(self, guns, image, screen: pygame.Surface, speed=4, cooldown=350, dmg=4):
        self.projectiles = []
        self.projectile_hitbox = [2, 4, 4, 8]
        self.cooldown = cooldown
        self.last_shoot = shader.get_time()
        self.guns = guns
        self.projectile_speed = speed
        self.dmg = dmg
        self.image = image
        self.screen_rect = pygame.Rect(
            -10,
            -100,
            screen.get_width() + 20,
            screen.get_height() + 200
        )

    def shoot(self, x, y):
        if shader.get_time() > self.last_shoot + self.cooldown:
            for gun in self.guns:
                self.projectiles.append([x + gun[0], y + gun[1], angle_to_motion(gun[2], self.projectile_speed)])
            self.last_shoot = shader.get_time()

    def draw(self, screen: pygame.Surface, player):
        new_proj = self.projectiles.copy()
        for projectile in self.projectiles:
            removed = False
            projectile[1] -= projectile[2][1]
            projectile[0] -= projectile[2][0]
            if not self.screen_rect.collidepoint((projectile[0], projectile[1])):
                removed = True
                try:
                    new_proj.remove(projectile)
                except:
                    pass
            screen.blit(self.image, (
                projectile[0] - self.projectile_hitbox[0], projectile[1] - self.projectile_hitbox[1],
                self.projectile_hitbox[2], self.projectile_hitbox[3]))
            if projectile[1] >= screen.get_height() + 30 and not removed:
                new_proj.remove(projectile)
                removed = True
            if not removed:
                for p_box in player.plane.hitbox:
                    if pygame.Rect(
                            (projectile[0] - self.projectile_hitbox[0], projectile[1] - self.projectile_hitbox[1],
                             self.projectile_hitbox[2], self.projectile_hitbox[3])) \
                            .colliderect((player.abs_pos[0] + p_box.x, player.abs_pos[1] + p_box.y, p_box.w, p_box.h)):
                        player.deal_damage(self.dmg)
                        try:
                            new_proj.remove(projectile)
                        except:
                            pass
        self.projectiles = new_proj.copy()
        del new_proj


class Enemy6DirProjectiles(EnemyProjectiles):
    def __init__(self, screen):
        super().__init__([], normal_enemy_projectile, screen)
        self.cooldown = 1750

    def shoot(self, x, y):
        if shader.get_time() > self.last_shoot + self.cooldown:
            for i in range(0, 360, 60):
                self.projectiles.append([x, y, angle_to_motion(i, self.projectile_speed),
                                         pygame.transform.rotate(self.image, i)])
            self.last_shoot = shader.get_time()


class RotatingEnemyProjectiles(EnemyProjectiles):
    def __init__(self, display):
        guns = [
            [42, 35, -45],
            [33, 35, -135]
        ]
        self.shoot_height = display.get_height() / 2 - 100
        super().__init__(guns, normal_enemy_projectile, display)
        self.max_shoot_count = 5
        self.cooldown = 30
        self.shoot_count = 0

    def shoot(self, x, y):
        if shader.get_time() > self.last_shoot + self.cooldown and \
                y > self.shoot_height and self.shoot_count < self.max_shoot_count:
            for gun in self.guns:
                self.projectiles.append(
                    [x + gun[0], y + gun[1], angle_to_motion(gun[2] + random.uniform(-10, 10), self.projectile_speed)])
            self.shoot_count += 1
            self.last_shoot = shader.get_time()


class BombProjectiles(EnemyProjectiles):
    def __init__(self, screen):
        super().__init__([], bullet_bomb_projectile, screen)

    def shoot(self, x, y):
        for i in range(0, 360, 24):
            self.projectiles.append([x, y, angle_to_motion(i, self.projectile_speed),
                                     pygame.transform.rotate(self.image, i)])
