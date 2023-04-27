import pygame

from scripts.projectiles import Projectiles, TrailProjectiles, DelanneProjectiles, BlackWidowProjectiles
from scripts.utils import load_animation_frames
from scripts.vfx import VFX

flame_anim_frames = load_animation_frames("sprites/flame", scale=0.1)


class Plane:
    def __init__(self, guns, dmg, health, hitbox, fire_cooldown, projectiles_speed, projectile_image, base_dir, vfx):
        self.guns = guns
        self.dmg = dmg
        self.health = health
        self.max_health = self.health
        self.hitbox = hitbox
        self.alive = True
        self.fire_cooldown = fire_cooldown
        self.projectiles_speed = projectiles_speed
        self.projectile_image = projectile_image
        self.base_dir = base_dir
        self.vfx = vfx
        self.abs_pos = [0, 0]
        self.frame_dict = {

        }
        self.image = None
        self.projectiles = Projectiles(self.guns, self.projectile_image, self.projectiles_speed, self.fire_cooldown,
                                       self.dmg, vfx, (self.get_x, self.get_y))

    def get_x(self):
        return self.abs_pos[0]

    def get_y(self):
        return self.abs_pos[1]

    def update(self, motion, screen, enemies, abs_pos):
        self.abs_pos = abs_pos
        tmp_motion = abs(motion)
        if tmp_motion >= 3.2:
            key = "t1"
        elif tmp_motion >= 2.4:
            key = "t2"
        elif tmp_motion >= 1.6:
            key = "t3"
        elif tmp_motion >= 1.2:
            key = "t4"
        else:
            key = "t5"
        self.image = self.frame_dict[key]
        if motion >= 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.shoot_projectiles(abs_pos)
        self.projectiles.draw(screen, enemies)

    def shoot_projectiles(self, abs_pos):
        self.projectiles.shoot(abs_pos[0], abs_pos[1])


class GrummanF3F(Plane):
    def __init__(self, vfx):
        image_scale = 0.5
        projectile_scale = 0.5
        guns = [[35 * image_scale, 16 * image_scale, 90], [78 * image_scale, 1 * image_scale, 90],
                [120 * image_scale, 16 * image_scale, 90]]
        hitbox = [
            pygame.Rect(67 * image_scale, 5 * image_scale, 23 * image_scale, 105 * image_scale),
            pygame.Rect(0 * image_scale, 22 * image_scale, 157 * image_scale, 38 * image_scale)
        ]
        health = 100
        fire_cooldown = 250
        projectiles_speed = 7
        projectiles_dmg = 8
        base_dir = "sprites/planes/grumman_f3f/"
        projectile_image = pygame.transform.scale_by(pygame.image.load(base_dir + "projectile.png"), projectile_scale)
        super().__init__(guns, projectiles_dmg, health, hitbox, fire_cooldown, projectiles_speed, projectile_image,
                         base_dir, vfx)
        self.frame_dict = {
            "t1": pygame.transform.scale_by(pygame.image.load(base_dir + "t1.png"), image_scale),
            "t2": pygame.transform.scale_by(pygame.image.load(base_dir + "t2.png"), image_scale),
            "t3": pygame.transform.scale_by(pygame.image.load(base_dir + "t3.png"), image_scale),
            "t4": pygame.transform.scale_by(pygame.image.load(base_dir + "t4.png"), image_scale),
            "t5": pygame.transform.scale_by(pygame.image.load(base_dir + "t5.png"), image_scale)
        }
        self.image = self.frame_dict["t5"]


class Boeing_P26_Peashooter(Plane):
    def __init__(self, vfx):
        image_scale = 0.5
        projectile_scale = 0.5
        angle_offset = 1.5
        guns = [[62 * image_scale, 24 * image_scale, 80 - angle_offset],
                [62 * image_scale, 24 * image_scale, 80 + angle_offset],
                [78 * image_scale, 3 * image_scale, 90 - angle_offset],
                [78 * image_scale, 3 * image_scale, 90 + angle_offset],
                [95 * image_scale, 24 * image_scale, 100 + angle_offset],
                [95 * image_scale, 24 * image_scale, 100 - angle_offset]]
        hitbox = [
            pygame.Rect(0 * image_scale, 34 * image_scale, 158 * image_scale, 32 * image_scale),
            pygame.Rect(66 * image_scale, 7 * image_scale, 26 * image_scale, 121 * image_scale)
        ]
        health = 100
        fire_cooldown = 300
        projectiles_speed = 5
        projectiles_dmg = 5
        base_dir = "sprites/planes/boeing_p-26_peashooter/"
        projectile_image = pygame.transform.scale_by(pygame.image.load(base_dir + "projectile.png"), projectile_scale)
        super().__init__(guns, projectiles_dmg, health, hitbox, fire_cooldown, projectiles_speed, projectile_image,
                         base_dir, vfx)
        self.frame_dict = {
            "t1": pygame.transform.scale_by(pygame.image.load(base_dir + "t1.png"), image_scale),
            "t2": pygame.transform.scale_by(pygame.image.load(base_dir + "t2.png"), image_scale),
            "t3": pygame.transform.scale_by(pygame.image.load(base_dir + "t3.png"), image_scale),
            "t4": pygame.transform.scale_by(pygame.image.load(base_dir + "t4.png"), image_scale),
            "t5": pygame.transform.scale_by(pygame.image.load(base_dir + "t5.png"), image_scale)
        }
        self.image = self.frame_dict["t5"]


class SEPECAT_Jaguar(Plane):
    def __init__(self, vfx):
        image_scale = 0.5
        projectile_scale = 1
        guns = [[26 * image_scale, 87 * image_scale, 90], [62 * image_scale, 10 * image_scale, 90],
                [98 * image_scale, 87 * image_scale, 90]]
        hitbox = [
            pygame.Rect(15 * image_scale, 109 * image_scale, 95 * image_scale, 25 * image_scale),
            pygame.Rect(61 * image_scale, 10 * image_scale, 3 * image_scale, 148 * image_scale),
            pygame.Rect(50 * image_scale, 58 * image_scale, 25 * image_scale, 101 * image_scale),
            pygame.Rect(41 * image_scale, 90 * image_scale, 43 * image_scale, 18 * image_scale),
        ]
        health = 100
        fire_cooldown = 400
        projectiles_speed = 10
        projectiles_dmg = 3
        base_dir = "sprites/planes/sepecat_jaguar/"
        projectile_image = pygame.transform.scale_by(pygame.image.load(base_dir + "projectile.png"), projectile_scale)
        projectile_trail = pygame.transform.scale_by(pygame.image.load(base_dir + "projectile_trail.png"),
                                                     projectile_scale)
        super().__init__(guns, projectiles_dmg, health, hitbox, fire_cooldown, projectiles_speed, projectile_image,
                         base_dir, vfx)
        self.projectiles = TrailProjectiles(guns, projectile_image, projectile_trail, projectiles_speed,
                                            fire_cooldown, projectiles_dmg, vfx, (self.get_x, self.get_y))
        self.frame_dict = {
            "t1": pygame.transform.scale_by(pygame.image.load(base_dir + "t1.png"), image_scale),
            "t2": pygame.transform.scale_by(pygame.image.load(base_dir + "t2.png"), image_scale),
            "t3": pygame.transform.scale_by(pygame.image.load(base_dir + "t3.png"), image_scale),
            "t4": pygame.transform.scale_by(pygame.image.load(base_dir + "t4.png"), image_scale),
            "t5": pygame.transform.scale_by(pygame.image.load(base_dir + "t5.png"), image_scale)
        }
        self.image = self.frame_dict["t5"]


class ARSENAL_Delanne_10(Plane):
    def __init__(self, vfx):
        image_scale = 0.5
        projectile_scale = 0.75
        guns = [[45 * image_scale, 31 * image_scale, 90],
                [86 * image_scale, 2 * image_scale, 90],
                [128 * image_scale, 31 * image_scale, 90]]
        hitbox = [
            pygame.Rect(0 * image_scale, 39 * image_scale, 174 * image_scale, 32 * image_scale),
            pygame.Rect(77 * image_scale, 7 * image_scale, 20 * image_scale, 127 * image_scale),
            pygame.Rect(32 * image_scale, 105 * image_scale, 110 * image_scale, 26 * image_scale)
        ]
        health = 100
        fire_cooldown = 300
        projectiles_speed = 10
        projectiles_dmg = 11
        base_dir = "sprites/planes/arsenal-delanne_10/"
        projectile_center_image = pygame.transform.scale_by(pygame.image.load(base_dir + "center_projectile.png"),
                                                            projectile_scale)
        projectile_left_image = pygame.transform.scale_by(pygame.image.load(base_dir + "side_projectile.png"),
                                                          projectile_scale)
        super().__init__(guns, projectiles_dmg, health, hitbox, fire_cooldown, projectiles_speed,
                         projectile_center_image,
                         base_dir, vfx)
        self.projectiles = DelanneProjectiles(guns, projectile_center_image, projectile_left_image, projectiles_speed,
                                              fire_cooldown, projectiles_dmg, vfx, (self.get_x, self.get_y))
        self.frame_dict = {
            "t1": pygame.transform.scale_by(pygame.image.load(base_dir + "t1.png"), image_scale),
            "t2": pygame.transform.scale_by(pygame.image.load(base_dir + "t2.png"), image_scale),
            "t3": pygame.transform.scale_by(pygame.image.load(base_dir + "t3.png"), image_scale),
            "t4": pygame.transform.scale_by(pygame.image.load(base_dir + "t4.png"), image_scale),
            "t5": pygame.transform.scale_by(pygame.image.load(base_dir + "t5.png"), image_scale)
        }
        self.image = self.frame_dict["t5"]


class P_61_Black_Widow(Plane):
    def __init__(self, vfx):
        image_scale = 0.5
        projectile_scale = 0.75
        guns = [
            [61 * image_scale, 22 * image_scale, 85],
            [99 * image_scale, -4 * image_scale, 90],
            [137 * image_scale, 22 * image_scale, 95]]
        hitbox = [
            pygame.Rect(0 * image_scale, 43 * image_scale, 199 * image_scale, 38 * image_scale),
            pygame.Rect(92 * image_scale, 0 * image_scale, 15 * image_scale, 98 * image_scale),
            pygame.Rect(56 * image_scale, 114 * image_scale, 86 * image_scale, 16 * image_scale)
        ]
        health = 100
        fire_cooldown = 250
        projectiles_speed = 8
        projectiles_dmg = 6
        base_dir = "sprites/planes/p-61_black_widow/"
        normal_projectiles = pygame.transform.smoothscale_by(pygame.image.load(base_dir + "projectile_1.png"),
                                                        projectile_scale)

        special_projectiles = pygame.transform.smoothscale_by(pygame.image.load(base_dir + "projectile_2.png"),
                                                        projectile_scale)
        super().__init__(guns, projectiles_dmg, health, hitbox, fire_cooldown, projectiles_speed,
                         normal_projectiles,
                         base_dir, vfx)
        self.projectiles = Projectiles(guns, normal_projectiles, projectiles_speed,
                                       fire_cooldown, projectiles_dmg, vfx, (self.get_x, self.get_y))

        special_speed = 4
        special_cooldown = 2000
        special_dmg = 12
        special_guns = [
            [85 * image_scale, 43 * image_scale, 90],
            [113 * image_scale, 43 * image_scale, 90]
        ]
        self.special_projectiles = BlackWidowProjectiles(special_guns, special_projectiles, special_speed,
                                                         special_cooldown, special_dmg, vfx, image_scale,
                                                         (self.get_x, self.get_y))
        self.frame_dict = {
            "t1": pygame.transform.scale_by(pygame.image.load(base_dir + "t1.png"), image_scale),
            "t2": pygame.transform.scale_by(pygame.image.load(base_dir + "t2.png"), image_scale),
            "t3": pygame.transform.scale_by(pygame.image.load(base_dir + "t3.png"), image_scale),
            "t4": pygame.transform.scale_by(pygame.image.load(base_dir + "t4.png"), image_scale),
            "t5": pygame.transform.scale_by(pygame.image.load(base_dir + "t5.png"), image_scale)
        }
        self.image = self.frame_dict["t5"]

    def update(self, motion, screen, enemies, abs_pos):
        super().update(motion, screen, enemies, abs_pos)
        self.special_projectiles.draw(screen, enemies, abs_pos)

    def shoot_projectiles(self, abs_pos):
        self.special_projectiles.shoot(abs_pos[0], abs_pos[1])
        super().shoot_projectiles(abs_pos)


class F_86_Sabre(Plane):
    def __init__(self, vfx):
        image_scale = 0.5
        projectile_scale = 0.75
        guns = [
            [21 * image_scale, 53 * image_scale, 82],
            [6 * image_scale, 74 * image_scale, 82],
            [47 * image_scale, 36 * image_scale, 82],

            [56 * image_scale, 30 * image_scale, 90],
            [74 * image_scale, -2 * image_scale, 90],
            [92 * image_scale, 30 * image_scale, 90],

            [128 * image_scale, 53 * image_scale, 98],
            [143 * image_scale, 74 * image_scale, 98],
            [101 * image_scale, 36 * image_scale, 98],
        ]
        hitbox = [
            pygame.Rect(0 * image_scale, 34 * image_scale, 150 * image_scale, 59 * image_scale),
            pygame.Rect(0 * image_scale, 63 * image_scale, 24 * image_scale, 125 * image_scale)
        ]
        health = 100
        fire_cooldown = 385
        projectiles_speed = 6
        projectiles_dmg = 3
        base_dir = "sprites/planes/f-86_sabre/"
        normal_projectiles = pygame.transform.scale_by(pygame.image.load(base_dir + "projectile.png"),
                                                       projectile_scale)
        super().__init__(guns, projectiles_dmg, health, hitbox, fire_cooldown, projectiles_speed,
                         normal_projectiles,
                         base_dir, vfx)
        self.frame_dict = {
            "t1": pygame.transform.scale_by(pygame.image.load(base_dir + "t1.png"), image_scale),
            "t2": pygame.transform.scale_by(pygame.image.load(base_dir + "t2.png"), image_scale),
            "t3": pygame.transform.scale_by(pygame.image.load(base_dir + "t3.png"), image_scale),
            "t4": pygame.transform.scale_by(pygame.image.load(base_dir + "t4.png"), image_scale),
            "t5": pygame.transform.scale_by(pygame.image.load(base_dir + "t5.png"), image_scale)
        }
        self.image = self.frame_dict["t5"]
        self.flame_delay = 40
        self.wait_time = 0
        self.max_wait_time = 30
        self.engines = [
            [21*image_scale, 96*image_scale],
            [128*image_scale, 96*image_scale]
        ]

    def update(self, motion, screen, enemies, abs_pos):
        super().update(motion, screen, enemies, abs_pos)
        self.wait_time += 1
        if self.wait_time >= self.max_wait_time:
            for engine in self.engines:
                self.vfx.append(VFX(flame_anim_frames, engine[0], engine[1], delay=self.flame_delay,
                                    anchor=(self.get_x, self.get_y), offset=(engine[0], engine[1])))
            self.wait_time = 0
