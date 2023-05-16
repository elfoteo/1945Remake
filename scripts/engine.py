import pygame.font
from scripts import planes
from scripts.projectiles import *
from scripts.stats import Stats
from scripts.utils import *
from scripts.utils import _quit
from scripts.vfx import VFX
from scripts.shader import Shader, ShaderDisplay
from scripts.button import *
import scripts.patterns as patterns

# init pygame and custom modules
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((440, 854), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("1945 Remake")
display = ShaderDisplay(screen.get_size())
shader = Shader()

loading_logo_img = load_image("sprites/ui/loading.png", 0.6)
display.blit(loading_logo_img, (display.get_width() / 2 - loading_logo_img.get_width() / 2,
                                display.get_height() / 2 - loading_logo_img.get_height() / 2))
shader.draw(display)
clock = pygame.time.Clock()
DEBUG = False
if DEBUG:
    print("!!! THIS GAME IS RUNNING IN DEBUG MODE !!!")
# TODO: better healthbar
planes.init()  # initialize the plane module adding all planes to the "all_planes" list
# load all images
healthbar_img = load_image("sprites/ui/ingame/healthbar.png", 0.6)
enemy_projectile_img = load_image("sprites/bombs/bullet_bomb/projectile.png")
enemy_normal2_frames = load_animation_frames("sprites/enemies/enemy_normal2")
enemy_normal_frames = load_animation_frames("sprites/enemies/enemy_normal")
rotating_enemy_frames = load_animation_frames("sprites/enemies/rotating_enemy")
enemy_shooter_6dir_img = load_image("sprites/enemies/enemy_shooter_6dir.png")
enemy_laser_img = load_image("sprites/enemies/enemy_laser.png")
following_enemy_img = load_image("sprites/enemies/following_enemy.png")
bullet_bomb_frames = load_animation_frames("sprites/bombs/bullet_bomb")
nuclear_bomb_frames = load_animation_frames("sprites/bombs/nuclear_bomb")
death_frames = [load_animation_frames("sprites/vfx/explosion_1"), load_animation_frames("sprites/vfx/explosion_2"),
                load_animation_frames("sprites/vfx/explosion_3"), load_animation_frames("sprites/vfx/explosion_4")]
coin1_frames = load_animation_frames("sprites/coins/1")
coin5_frames = load_animation_frames("sprites/coins/5")
ingame_coins_img = load_image("sprites/ui/ingame/ingame_coin.png", 0.8)
win_tail_r = load_image("sprites/ui/level/tail.png", 1)
win_front_r = load_image("sprites/ui/level/front.png", 1)
win_shadow_r = load_image("sprites/ui/level/shadow.png", 1)
win_tail_l = pygame.transform.flip(win_tail_r, True, False)
win_shadow_l = pygame.transform.flip(win_shadow_r, True, False)
win_front_l = pygame.transform.flip(win_front_r, True, False)
win_label = load_image("sprites/ui/level/victory_label.png", 1.2)

eagle_head = load_image("sprites/ui/level/eagle_head.png", 1.2)
eagle_wing_r = load_image("sprites/ui/level/eagle_wing.png", 1.2)
eagle_wing_bottom_r = load_image("sprites/ui/level/eagle_wing_bottom.png", 1.2)
eagle_wing_l = pygame.transform.flip(eagle_wing_r, True, False)
eagle_wing_bottom_l = pygame.transform.flip(eagle_wing_bottom_r, True, False)
win_star_circle = load_image("sprites/ui/level/star_circle.png", 1.2)
win_star = load_image("sprites/ui/level/star.png", 1.2)
level_banner = load_image("sprites/ui/level/level_banner.png", 1.2)
pass_lvl_button = load_image("sprites/ui/level/pass_lvl_button.png", 1)
level_rewards_bg = load_image("sprites/ui/level/rewards_bg.png", 1)

level_defeated = load_image("sprites/ui/level/defeated.png", 1.2)

ui_background = load_image("sprites/ui/ui_background.png", display.get_size(), no_scale_by=True, alpha=False)

coin_icon = load_image("sprites/ui/coin.png", 1)
gem_icon = load_image("sprites/ui/gem.png", 1)
dogtag_icon = load_image("sprites/ui/dogtag.png", 1)
buy_dogtags = load_image("sprites/ui/buy_dogtags.png", 0.9)
popup_bg = load_image("sprites/ui/buy_dogtags.png", 0.9)
dogtags_pile = load_image("sprites/ui/dogtags_pile.png", 1)
single_dogtag = load_image("sprites/ui/single_dogtag.png", 1)
text_label = load_image("sprites/ui/text_label.png", 1.25)
popup_title_label = load_image("sprites/ui/text_label.png", 1)
gem_purchase = load_image("sprites/ui/gem_purchase.png", 1.35)
gui_close = load_image("sprites/ui/gui_close.png", 1.1)
gui_close_hover = load_image("sprites/ui/gui_close_hover.png", 1.1)

gui_parking_area = load_image("sprites/ui/parking_area.png", 1.1)
arrow_back = load_image("sprites/ui/arrow_back.png", 1.25)
planes_gui_plane_station = load_image("sprites/ui/planes/plane_station.png", 1.2)
planes_gui_container = load_image("sprites/ui/planes/plane_container.png", 1.135)
planes_gui_progressbar_container = load_image("sprites/ui/planes/progressbar_container.png", 1.22)
planes_gui_plane_name_label = load_image("sprites/ui/planes/plane_name_label.png", 1.1)
planes_gui_not_selected_plane = load_image("sprites/ui/planes/not_selected_plane.png", 0.435)
planes_gui_not_unlocked_plane = load_image("sprites/ui/planes/not_unlocked_plane.png", 0.435)
planes_gui_selected_plane = load_image("sprites/ui/planes/selected_plane.png", 0.435)
planes_gui_arrow_back_frame = load_image("sprites/ui/planes/arrow_back_frame.png", 1.2)
green_button = load_image('sprites/ui/green_button.png', 1.5)
pile_of_coins = load_image('sprites/ui/level/pile_of_coins.png', 1)
pile_of_gems = load_image('sprites/ui/level/pile_of_gems.png', 1)
visual_effects = []
user_stats = Stats()
scroll_speed = 0.35
coins = []

font_small = pygame.font.Font("font/font.ttf", 16)
font_medium_small = pygame.font.Font("font/font.ttf", 20)
font_medium = pygame.font.Font("font/font.ttf", 24)
gui_title_font = pygame.font.Font("font/font.ttf", 28)
font = pygame.font.Font("font/font.ttf", 30)
big_font = pygame.font.Font("font/font.ttf", 58)


def quit_game():
    user_stats.save()
    _quit()


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

    @staticmethod
    def get_button(num):
        return pygame.mouse.get_pressed()[num]

    def collideswith(self, rect):
        if type(rect) == pygame.Rect:
            if rect.collidepoint(self.get_pos()):
                return True
        else:
            if pygame.Rect(rect).collidepoint(self.get_pos()):
                return True
        return False

    def lock(self):
        self.set_grab(True)
        self.set_visible(False)

    @staticmethod
    def get_pos():
        return pygame.mouse.get_pos()

    def draw(self):
        self.rel = pygame.mouse.get_rel()


class Player:
    def __init__(self):
        self.coins_pickup_distance = 100
        self.window = pygame.Rect((0, 0,
                                   display.get_width(),
                                   display.get_height()))
        self.plane = user_stats.get_plane()(visual_effects)
        self.default_spawn_pos = [display.get_width() / 2, display.get_height() - self.plane.image.get_height() * 4]
        self.pos = self.default_spawn_pos
        self.abs_pos = self.pos
        self.average_motion_x = 0
        self.motion_history = []
        self.auto_controlled = False
        self.auto_rel = [0, 0]
        self.is_dummy = False

    def refresh_plane(self):
        self.plane = user_stats.get_plane()(visual_effects)

    def draw_healthbar(self):
        display.blit(healthbar_img, (10, 10))
        rect = pygame.Rect(10 + 266 / 2 * 1.2, 11 + 22 / 2 * 1.2,
                           -(215 / 2 * 1.2) * (max(self.plane.health / self.plane.max_health, 0) * -1 + 1),
                           21 / 2 * 1.2 - 1)
        rect.normalize()
        pygame.draw.rect(display, (120, 120, 120), rect)
        if self.plane.health <= 0 and self.plane.alive:
            self.plane.alive = False
            visual_effects.append(VFX(death_frames[0], self.abs_pos[0], self.abs_pos[1], delay=10))

    def collides(self, hitboxes):
        for hitbox in hitboxes:
            for plane_hitbox in self.plane.hitbox:
                real_hitbox = pygame.Rect(self.abs_pos[0] + plane_hitbox.x,
                                          self.abs_pos[1] + plane_hitbox.y,
                                          plane_hitbox.w,
                                          plane_hitbox.h)
                if hitbox.colliderect(real_hitbox):
                    return True
        return False

    @staticmethod
    def draw_coins():
        display.blit(ingame_coins_img, (display.get_width() - 50, 150))
        text = outlined_text(str(user_stats.data["ingame_coins"]), font)
        display.blit(text, (display.get_width() - 50 - text.get_width(), 150))

    def deal_damage(self, ammount):
        self.plane.health -= ammount
        shader.red_overlay = 1
        shader.shake_ammount += 1.5

    def draw(self):
        if not self.auto_controlled:
            mx, my = mouse.rel
        else:
            mx, my = self.auto_rel

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
        if (pygame.mouse.get_pressed()[0] and self.window.collidepoint(
                (self.pos[0], self.pos[1] + my))) or self.auto_controlled:
            self.pos[1] += my
        self.abs_pos = (self.pos[0] - self.plane.image.get_width() / 2, self.pos[1] - self.plane.image.get_height() / 2)
        if self.plane.alive:
            self.plane.update(self.average_motion_x, display, enemies, self.abs_pos, is_dummy=self.is_dummy)
            display.blit(self.plane.image,
                        (self.pos[0] - self.plane.image.get_width() / 2, self.pos[1] - self.plane.image.get_height() / 2))
        if DEBUG:
            for box in self.plane.hitbox:
                pygame.draw.rect(display, (255, 0, 0), (self.abs_pos[0] + box.x, self.abs_pos[1] + box.y, box.w, box.h))

    def draw_gui(self):
        self.draw_healthbar()
        self.draw_coins()


class Coin:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos
        if self.value <= 4:
            self.frames = coin1_frames
        elif self.value >= 5:
            self.frames = coin5_frames
        self.index = 0
        self.last_frame = time.time() * 1000
        self.delay = 120
        self.abs_pos = (self.pos[0] - self.frames[self.index].get_width() / 2,
                        self.pos[1] - self.frames[self.index].get_height() / 2)
        self.alive = True
        self.picking_up = False
        self.pos = [self.pos[0] - self.frames[self.index].get_width() / 2,
                    self.pos[1] - self.frames[self.index].get_height() / 2]

    def draw(self):
        self.abs_pos = (self.pos[0] + self.frames[self.index].get_width() / 2,
                        self.pos[1] + self.frames[self.index].get_height() / 2)
        if self.alive:
            self.pos[1] += scroll_speed+0.1
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

class Popup:
    def __init__(self, title, option1, option2, description) -> None:
        self.title = title
        self.option_1 = Button(display.get_width() / 2-148/2, display.get_height() / 2+50, 148,
                           40,
                           'sprites/ui/green_button.png',
                           text=option1,
                           font="font/font.ttf", increase_font_size=0.15)
        self.option_2 = Button(display.get_width() / 2 - 148/2, display.get_height() / 2 + 100, 148,
                         40,
                         'sprites/ui/yellow_button.png',
                         text=option2,
                         font="font/font.ttf", increase_font_size=0.15)
        self.description = description

    def get_result(self, display_copy):
        transparent_overlay = transparent_rect(display.get_size(), 0.65)
        popup_title = font_medium.render(self.title, False, (255, 255, 255))

        popup_description = font_medium_small.render(self.description, False, (255, 255, 255))
        while True:
            display.blit(display_copy, (0, 0))
            display.blit(transparent_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            display.blit(popup_bg, (display.get_width()/2-popup_bg.get_width()/2, display.get_height()/2-popup_bg.get_height()/2))
            display.blit(popup_title_label, (display.get_width() / 2 - popup_title_label.get_width() / 2,
                                             display.get_height()/2-popup_bg.get_height()/2))
            display.blit(popup_title, (display.get_width() / 2 - popup_title.get_width() / 2, display.get_height()/2-popup_bg.get_height()/2+5))
            display.blit(popup_description, (display.get_width() / 2 - popup_description.get_width() / 2, display.get_height()/2-75))
            self.option_1.draw(display)
            self.option_2.draw(display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                if self.option_1.handle_event(event):
                    return 1
                elif self.option_2.handle_event(event):
                    return 2

            mouse.draw()
            shader.draw(display)
            clock.tick(120)

class Enemy:
    def __init__(self, speed, health, enemy_projectiles, image, pos, hitbox, auto_shoot=True,
                 particles_on_death=True, auto_move=True):
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
        self.auto_move = auto_move

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
        coins.append(Coin(1, [self.pos[0] + self.image.get_width() / 2, self.pos[1] + self.image.get_height() / 2]))
        if self.particles_on_death:
            for _ in range(2):
                visual_effects.append(
                    VFX(random.choice(death_frames), self.pos[0] + self.image.get_width() / 4, self.pos[1] + self.image.get_height() + 5,
                        delay=10))
            visual_effects.append(
                VFX(death_frames[0], self.pos[0] + self.image.get_width() / 4,
                    self.pos[1] + self.image.get_height() + 5,
                    delay=10))

    def draw(self):
        if self.auto_move:
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
                    player.deal_damage(self.health)
                    self.health = 0
            if DEBUG:
                for box in self.hitbox:
                    pygame.draw.rect(display, (255, 0, 0), (self.pos[0] + box.x, self.pos[1] + box.y, box.w, box.h))


class NormalEnemy(Enemy):
    def __init__(self, pos):
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        image = enemy_normal_frames[0]
        health = 35
        speed = 1
        self.frame_delay = 120
        self.next_frame = time.time() * 1000
        self.frame_index = 0
        hitbox = [pygame.Rect((round(47 * 0.6), round(3 * 0.6), round(16 * 0.6), round(87 * 0.6))),
                  pygame.Rect((round(0 * 0.6), round(44 * 0.6), round(110 * 0.6), round(22 * 0.6)))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox)
    
    def draw(self):
        if self.next_frame + self.frame_delay <= time.time() * 1000:
            self.next_frame = time.time() * 1000
            self.frame_index += 1
            if self.frame_index >= 2:
                self.frame_index = 0
            self.image = enemy_normal_frames[self.frame_index]
        super().draw()

class NormalEnemy2(Enemy):
    def __init__(self, pos):
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        image = enemy_normal2_frames[0]
        health = 35
        speed = 1
        self.frame_delay = 110
        self.next_frame = time.time() * 1000
        self.frame_index = 0
        hitbox = [pygame.Rect((round(47 * 0.6), round(3 * 0.6), round(16 * 0.6), round(87 * 0.6))),
                  pygame.Rect((round(0 * 0.6), round(44 * 0.6), round(110 * 0.6), round(22 * 0.6)))]
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
                pygame.Rect(self.hitbox[0].x + self.pos[0], self.hitbox[0].y + self.pos[1],
                            self.hitbox[0].w, self.hitbox[0].h)):
            self.speed = 0
        if self.speed == 0:
            if self.pos[1] > player.pos[1]:
                angle = 90
            else:
                angle = angle_between_points(self.pos, player.pos)
            self.current_angle += (angle - self.current_angle) / 15
            motion = angle_to_motion(self.current_angle, self.base_speed)
            if self.pos[1] < player.pos[1]:
                self.pos[0] += motion[0]
            self.pos[1] += self.base_speed
            self.image = pivot_rotate(self.base_image, self.current_angle - 90, (self.base_image.get_width() / 2,
                                                                                 self.base_image.get_height() / 2),
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
                    player.deal_damage(self.health)
                    self.health = 0
            if DEBUG:
                for box in self.hitbox:
                    pygame.draw.rect(display, (255, 0, 0), (self.pos[0] + box.x, self.pos[1] + box.y, box.w, box.h))


class LaserEnemy(Enemy):
    def __init__(self, pos):
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        self.image_scale = 0.75
        image = pygame.transform.scale_by(enemy_laser_img, self.image_scale)
        health = 35
        speed = 1
        hitbox = [pygame.Rect((round(14 * self.image_scale), round(13 * self.image_scale),
                               round(86 * self.image_scale), round(85 * self.image_scale)))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox, auto_shoot=False, auto_move=False)
        self.laser_cooldown = 6000
        self.laser_duration = 3000
        self.last_laser_active = time.time() * 1000
        self.laser_active = False
        self.last_shoot = time.time() * 1000

    def draw(self):
        super().draw()
        self.pos[1] += min(self.speed, (display.get_height() / 3 - self.pos[1]) / 20)
        if self.laser_active:
            rect_l = pygame.Rect(0, self.pos[1] + (52 * self.image_scale),
                                 self.pos[0], 9 * self.image_scale)
            rect_r = pygame.Rect(self.pos[0] + (113 * self.image_scale), self.pos[1] + (52 * self.image_scale),
                                 display.get_width() - self.pos[0], 9 * self.image_scale)
            pygame.draw.rect(display, (255, 0, 0), rect_l)
            pygame.draw.rect(display, (255, 0, 0), rect_r)
            if player.collides([rect_l, rect_r]):
                player.deal_damage(player.plane.health + 1)
        if self.last_laser_active + self.laser_cooldown < time.time() * 1000 and not self.laser_active and display.get_rect().colliderect(
                pygame.Rect(self.hitbox[0].x + self.pos[0], self.hitbox[0].y + self.pos[1],
                            self.hitbox[0].w, self.hitbox[0].h)):
            self.last_shoot = time.time() * 1000
            self.laser_active = True
        if self.laser_active and self.last_shoot + self.laser_duration < time.time() * 1000:
            self.last_laser_active = time.time() * 1000
            self.laser_active = False


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
                    player.deal_damage(self.health)
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
        shader.shake_ammount += 1.6
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
        shader.shake_ammount += 2.4
        for enemy in enemies:
            if distance_between_points(enemy.pos, self.pos) <= 350:
                enemy.health -= distance_between_points(enemy.pos, self.pos) * -1 + 400

        if distance_between_points(player.pos, self.pos) <= 350:
            player.deal_damage(distance_between_points(player.pos, self.pos) * -1 + 385)

        anim = []
        for i in death_frames[0]:
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


class Level:
    def __init__(self, enemies, level_number: int, level_difficulty: int, bg: str) -> None:
        difficulty_int = level_difficulty
        if level_difficulty == 1:
            level_difficulty = "EASY"
        elif level_difficulty == 2:
            level_difficulty = "MEDIUM"
        elif level_difficulty == 3:
            level_difficulty = "HARD"
        else:
            level_difficulty = "UNKNOWN"
        self.name = "LEVEL " + str(level_number) + " - " + level_difficulty.upper()
        self.number = level_number
        self.difficulty = level_difficulty
        self.enemies = enemies
        self.finished = False
        self.finished_cooldown = 5000
        self.finished_timestamp = -1
        self.coins = []
        self.rewarded_gems = difficulty_int
        self.rewarded_coins = self.get_coins_from_level(level_number, difficulty_int)
        self.bg = load_image(bg)

    @staticmethod
    def get_coins_from_level(num, multiplier=1):
        output_num = int(num * (30 + multiplier * 15) + 500)
        if output_num > 3500:
            output_num = int(3500 + (output_num - 3500) * 0.2)
        return output_num

    def give_rewards(self):
        user_stats.add_coins(self.rewarded_coins)
        user_stats.add_gems(self.rewarded_gems)

    def get_rewards(self):
        return self.rewarded_coins, self.rewarded_gems


mouse = Mouse()
player = Player()
enemies = []
