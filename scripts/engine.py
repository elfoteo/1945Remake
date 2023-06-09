import pygame.font
from scripts import planes
from scripts.projectiles import *
from scripts.stats import Stats
from scripts.utils import *
from scripts.utils import _quit
from scripts.vfx import VFX
from scripts.vfx import init as vfx_init
from scripts.shader import Shader, ShaderDisplay
from scripts.button import *
from scripts import projectiles
from scripts import patterns

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
vfx_init(shader)  # initialize the vfx module
projectiles.init(shader)  # initialize the projectiles module to load all images
planes.init()  # initialize the plane module adding all planes to the "all_planes" list
patterns.init(display)  # initialize the pattern module to place enemies more easly
# load all images
healthbar_img = load_image("sprites/ui/ingame/healthbar.png", 0.75)
healthbar_frame_img = load_image("sprites/ui/ingame/healthbar_frame.png", 0.75)
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
small_coin_icon = load_image("sprites/ui/coin.png", 0.85)
gem_icon = load_image("sprites/ui/gem.png", 1)
small_gem_icon = load_image("sprites/ui/gem.png", 0.85)
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
plane_star_rank = load_image("sprites/ui/planes/star_rank.png", 0.75)
planes_gui_container = load_image("sprites/ui/planes/plane_container.png", 1.135)
planes_gui_progressbar_container = load_image("sprites/ui/planes/progressbar_container.png", 1.22)
planes_gui_plane_name_label = load_image("sprites/ui/planes/plane_name_label.png", 1.1)
planes_gui_not_selected_plane = load_image("sprites/ui/planes/not_selected_plane.png", 0.435)
planes_gui_not_unlocked_plane = load_image("sprites/ui/planes/not_unlocked_plane.png", 0.435)
planes_gui_selected_plane = load_image("sprites/ui/planes/selected_plane.png", 0.435)
planes_gui_not_unlocked_selected_plane = load_image("sprites/ui/planes/not_unlocked_selected_plane.png", 0.435)
planes_gui_arrow_back_frame = load_image("sprites/ui/planes/arrow_back_frame.png", 1.2)
green_button = load_image('sprites/ui/green_button.png', 1.5)
pile_of_coins = load_image('sprites/ui/level/pile_of_coins.png', 1)
pile_of_gems = load_image('sprites/ui/level/pile_of_gems.png', 1)
italy_map = load_image('sprites/ui/map/italy_map.png', 1.22)
level_icon = load_image('sprites/ui/map/level_icon.png', 0.65)
locked_level_icon = load_image('sprites/ui/map/locked_level_icon.png', 0.65)
rapid_fire_img = load_image('sprites/buffs/rapid_fire.png', 0.5)
rapid_fire_pickup_img = load_image('sprites/buffs/rapid_fire_pickup.png', 0.5)
protection_img = load_image('sprites/buffs/protection.png', 0.5)
protection_pickup_img = load_image('sprites/buffs/protection_pickup.png', 0.5)
magnet_img = load_image('sprites/buffs/magnet.png', 0.5)
magnet_pickup_img = load_image('sprites/buffs/magnet_pickup.png', 0.5)
visual_effects = []
user_stats = Stats()
scroll_speed = 0.35
coins = []
buffs_pickup = []

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
        level = user_stats.data["planes"][user_stats.get_plane()][1]
        self.plane = user_stats.get_plane()(visual_effects, level)
        self.default_spawn_pos = [display.get_width() / 2, display.get_height() - self.plane.image.get_height() * 4]
        self.pos = self.default_spawn_pos
        self.abs_pos = self.pos
        self.average_motion_x = 0
        self.motion_history = []
        self.auto_controlled = False
        self.auto_rel = [0, 0]
        self.is_dummy = False
        self.buffs = []

    def reset(self):
        level = user_stats.data["planes"][user_stats.get_plane()][1]
        self.plane = user_stats.get_plane()(visual_effects, level)
        self.default_spawn_pos = [display.get_width() / 2, display.get_height() - self.plane.image.get_height() * 4]
        self.pos = self.default_spawn_pos
        self.abs_pos = self.pos
        self.average_motion_x = 0
        self.motion_history = []
        self.auto_controlled = False
        self.auto_rel = [0, 0]
        self.is_dummy = False
        self.buffs = []

    def has_buff(self, buff_type) -> bool:
        for buff in self.buffs:
            if type(buff) == buff_type:
                return True
        return False

    def refresh_plane(self):
        self.plane = user_stats.get_plane()(visual_effects, user_stats.data["planes"][user_stats.get_plane()][1])

    def draw_healthbar(self):
        healthbar_pos = 10, 10
        healthbar_scale = 0.75
        display.blit(healthbar_frame_img, (10, 10))
        # Cut the healthbar image blitting it in a smaller surface
        healthbar_surf = pygame.Surface((healthbar_img.get_width() * max(self.plane.health / self.plane.max_health, 0),
                                         healthbar_img.get_height()))
        healthbar_surf.blit(healthbar_img, (0, 0))
        display.blit(healthbar_surf, (healthbar_pos[0] + 53 * healthbar_scale, healthbar_pos[1] + 23 * healthbar_scale))

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
        display.blit(ingame_coins_img, (display.get_width() - 50, 25))
        text = outlined_text(str(user_stats.data["ingame_coins"]), font)
        display.blit(text, (display.get_width() - 55 - text.get_width(), 25))

    def deal_damage(self, amount):
        if amount <= 0:
            return
        if not self.has_buff(ProtectionBuff):
            shader.shake_amount += 1.5
            self.plane.health -= amount
            shader.red_overlay = 1
        else:
            shader.shake_amount += 0.75  # reduce shake amount if the player has the protection buff

    def draw(self):
        if self.plane.health >= self.plane.max_health:
            self.plane.health = self.plane.max_health
        if not self.auto_controlled:
            mx, my = mouse.rel
        else:
            mx, my = self.auto_rel

        if pygame.mouse.get_pressed()[0]:
            self.motion_history.append([mx, shader.get_time() / 1000])
        else:
            self.motion_history.append([0, shader.get_time() / 1000])
        for i in self.motion_history:
            if i[1] + 0.7 <= shader.get_time() / 1000:
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
                         (self.pos[0] - self.plane.image.get_width() / 2,
                          self.pos[1] - self.plane.image.get_height() / 2))
        if DEBUG:
            for box in self.plane.hitbox:
                pygame.draw.rect(display, (255, 0, 0), (self.abs_pos[0] + box.x, self.abs_pos[1] + box.y, box.w, box.h))

    def apply_buff(self, buff_type):
        apply = True
        for buff in self.buffs:
            if type(buff) == buff_type:
                buff.renew()
                return
        if apply:
            self.buffs.append(buff_type())

    def draw_gui(self):
        self.draw_healthbar()
        self.draw_coins()
        y = 80
        x = 30
        for buff in self.buffs:
            buff.draw([x, y])
            if not buff.active:
                self.buffs.remove(buff)
            y += 70


class Buff:
    def __init__(self, duration, image):
        self.duration = duration
        self.image = image
        self.start_time = shader.get_ingame_time()
        self.active = True
        self.buff_applied()

    def renew(self):
        self.start_time = shader.get_ingame_time()

    def draw(self, pos):
        if shader.get_ingame_time() - self.start_time < self.duration:
            self.active = True
        else:
            self.active = False
            self.buff_expired()
        surf = pygame.Surface((69, 69), pygame.SRCALPHA)
        draw_pie_segment(surf, shader.get_ingame_time() - self.start_time, self.duration, (69 / 2, 69 / 2), 69)
        surf.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        display.blit(surf, pos)
        if self.active:
            self.on_buff_active_tick()

    def buff_applied(self):
        pass

    def buff_expired(self):
        pass

    def on_buff_active_tick(self):
        pass


class RapidFireBuff(Buff):
    def __init__(self):
        duration = seconds_to_ticks(10)  # 10 seconds
        image = rapid_fire_img
        super().__init__(duration, image)

    def buff_applied(self):
        super().buff_applied()
        player.plane.projectiles.cooldown /= 2

    def buff_expired(self):
        super().buff_expired()
        player.plane.projectiles.cooldown *= 2


class MagnetBuff(Buff):
    def __init__(self):
        duration = seconds_to_ticks(10)  # 10 seconds
        image = magnet_img
        super().__init__(duration, image)

    def buff_applied(self):
        super().buff_applied()
        player.coins_pickup_distance *= 5

    def buff_expired(self):
        super().buff_expired()
        player.coins_pickup_distance /= 5


class ProtectionBuff(Buff):
    def __init__(self):
        duration = seconds_to_ticks(10)  # 10 seconds
        image = protection_img
        super().__init__(duration, image)


class BuffPickup:
    def __init__(self, pos, image, buff_type):
        self.pos = pos
        self.image = image
        self.buff_type = buff_type
        self.alive = True

    def draw(self):
        if self.alive:
            self.pos[1] += scroll_speed + 0.15
            hitbox = pygame.Rect((self.pos[0] - self.image.get_width() / 2, self.pos[1] - self.image.get_height() / 2,
                                  self.image.get_width(), self.image.get_height()))
            display.blit(self.image, (hitbox.x, hitbox.y))
            if player.collides([hitbox]):
                player.apply_buff(self.buff_type)
                self.alive = False


class RapidFirePickup(BuffPickup):
    def __init__(self, pos):
        image = rapid_fire_pickup_img
        buff_type = RapidFireBuff
        super().__init__(pos, image, buff_type)


class MagnetPickup(BuffPickup):
    def __init__(self, pos):
        image = magnet_pickup_img
        buff_type = MagnetBuff
        super().__init__(pos, image, buff_type)


class ProtectionPickup(BuffPickup):
    def __init__(self, pos):
        image = protection_pickup_img
        buff_type = ProtectionBuff
        super().__init__(pos, image, buff_type)


class Coin:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos
        if self.value <= 4:
            self.frames = coin1_frames
        elif self.value >= 5:
            self.frames = coin5_frames
        self.index = 0
        self.last_frame = shader.get_time()
        self.delay = 120
        self.abs_pos = (self.pos[0] - self.frames[self.index].get_width() / 2,
                        self.pos[1] - self.frames[self.index].get_height() / 2)
        self.alive = True
        self.picking_up = False
        self.pos = [self.pos[0] - self.frames[self.index].get_width() / 2,
                    self.pos[1] - self.frames[self.index].get_height() / 2]

    def draw(self):
        if self.alive:
            self.abs_pos = (self.pos[0] + self.frames[self.index].get_width() / 2,
                            self.pos[1] + self.frames[self.index].get_height() / 2)
            self.pos[1] += scroll_speed + 0.15
            if self.last_frame + self.delay < shader.get_time():
                if self.index + 1 >= len(self.frames):
                    self.index = 0
                else:
                    self.index += 1
                self.last_frame = shader.get_time()
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
        self.option_1 = Button(display.get_width() / 2 - 148 / 2, display.get_height() / 2 + 50, 148,
                               40,
                               'sprites/ui/green_button.png',
                               text=option1,
                               font="font/font.ttf", increase_font_size=0.15)
        self.option_2 = Button(display.get_width() / 2 - 148 / 2, display.get_height() / 2 + 100, 148,
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
            display.blit(popup_bg, (
                display.get_width() / 2 - popup_bg.get_width() / 2,
                display.get_height() / 2 - popup_bg.get_height() / 2))
            display.blit(popup_title_label, (display.get_width() / 2 - popup_title_label.get_width() / 2,
                                             display.get_height() / 2 - popup_bg.get_height() / 2))
            display.blit(popup_title, (display.get_width() / 2 - popup_title.get_width() / 2,
                                       display.get_height() / 2 - popup_bg.get_height() / 2 + 5))
            display.blit(popup_description,
                         (display.get_width() / 2 - popup_description.get_width() / 2, display.get_height() / 2 - 75))
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
        self.dropped_coins = 1

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def collide(self, rect) -> bool:
        for hitbox in self.hitbox:
            if pygame.Rect(self.pos[0] + hitbox.x, self.pos[1] + hitbox.y,
                           hitbox.w, hitbox.h).colliderect(rect):
                return True
        return False

    def draw_health_bar(self):
        if self.health < self.max_health:
            pygame.draw.rect(display, (80, 80, 80),
                             (self.pos[0] + self.get_width() / 4, self.pos[1] + self.get_height() + 5,
                              self.get_width() / 4 * 2, 5))
            pygame.draw.rect(display, (216, 13, 0),
                             (self.pos[0] + self.get_width() / 4, self.pos[1] + self.get_height() + 5,
                              (self.get_width() / 4 * 2) * (self.health / self.max_health), 5))

    def on_death(self):
        if random.randint(0, max(2, int(100-self.health*2))) == 0:
            pos = [self.pos[0]+self.image.get_width()/2, self.pos[1]+self.image.get_height()/2]
            buff_list = [RapidFirePickup, ProtectionPickup, MagnetPickup]
            buffs_pickup.append(random.choice(buff_list)(pos))
        else:
            coins.append(Coin(self.dropped_coins, [self.pos[0] + self.get_width() / 2, self.pos[1] + self.get_height() / 2]))
        if self.particles_on_death:
            for _ in range(2):
                visual_effects.append(
                    VFX(random.choice(death_frames), self.pos[0] + self.get_width() / 4,
                        self.pos[1] + self.get_height() + 5,
                        delay=10))
            visual_effects.append(
                VFX(death_frames[0], self.pos[0] + self.get_width() / 4,
                    self.pos[1] + self.get_height() + 5,
                    delay=10))

    def draw(self):
        if self.auto_move:
            self.pos[1] += self.speed * shader.get_dt()
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
            if self.pos[1] >= display.get_height() + self.get_height() + 100:
                self.alive = False
            for p_box in player.plane.hitbox:
                if self.collide((player.abs_pos[0] + p_box.x, player.abs_pos[1] + p_box.y, p_box.w, p_box.h)):
                    player.deal_damage(self.health)
                    self.health = 0
            if DEBUG:
                for box in self.hitbox:
                    pygame.draw.rect(display, (255, 0, 0), (self.pos[0] + box.x, self.pos[1] + box.y, box.w, box.h))


class NormalEnemy(Enemy):
    def __init__(self, pos):
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        image = enemy_normal_frames[0]
        health = 30
        speed = 1
        self.frame_delay = 120
        self.next_frame = shader.get_time()
        self.frame_index = 0
        hitbox = [pygame.Rect((round(47 * 0.6), round(3 * 0.6), round(16 * 0.6), round(87 * 0.6))),
                  pygame.Rect((round(0 * 0.6), round(44 * 0.6), round(110 * 0.6), round(22 * 0.6)))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox)

    def draw(self):
        if self.next_frame + self.frame_delay <= shader.get_time():
            self.next_frame = shader.get_time()
            self.frame_index += 1
            if self.frame_index >= 2:
                self.frame_index = 0
            self.image = enemy_normal_frames[self.frame_index]
        super().draw()


class NormalEnemy2(Enemy):
    def __init__(self, pos):
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        image = enemy_normal2_frames[0]
        health = 30
        speed = 1
        self.frame_delay = 110
        self.next_frame = shader.get_time()
        self.frame_index = 0
        hitbox = [pygame.Rect((round(47 * 0.6), round(3 * 0.6), round(16 * 0.6), round(87 * 0.6))),
                  pygame.Rect((round(0 * 0.6), round(44 * 0.6), round(110 * 0.6), round(22 * 0.6)))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox)

    def draw(self):
        if self.next_frame + self.frame_delay <= shader.get_time():
            self.next_frame = shader.get_time()
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
        self.next_frame = shader.get_time()
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
                self.pos[0] += motion[0] * shader.get_dt()
            self.pos[1] += self.base_speed * shader.get_dt()
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
        self.next_frame = shader.get_time()
        self.frame_index = 0
        self.current_image = image
        hitbox = [pygame.Rect((0, 0, 76, 31)),
                  pygame.Rect((32, 3, 12, 65))]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox)

    def draw(self):
        if self.pos[1] <= -50:
            self.speed = 1
        else:
            self.speed = 1.5
        if self.next_frame + self.frame_delay <= shader.get_time():
            self.next_frame = shader.get_time()
            self.frame_index += 1
            if self.frame_index >= len(rotating_enemy_frames):
                self.frame_index = 0
            self.current_image = rotating_enemy_frames[self.frame_index]
        # Draw
        self.pos[1] += self.speed * shader.get_dt()
        if self.health <= 0 and self.alive:
            self.alive = False
            self.on_death()
        if self.alive:
            display.blit(self.current_image,
                         (self.pos[0] - self.current_image.get_width() / 2 + self.get_width() / 2,
                          self.pos[1]))
        if self.alive and self.pos[1] >= 0 and self.auto_shoot:
            self.projectiles.shoot(self.pos[0], self.pos[1])
        self.projectiles.draw(display, player)
        if self.alive:
            self.draw_health_bar()
            if self.pos[1] >= display.get_height() + self.get_height() + 100:
                self.alive = False
            for p_box in player.plane.hitbox:
                if self.collide((player.abs_pos[0] + p_box.x, player.abs_pos[1] + p_box.y, p_box.w, p_box.h)):
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
        self.last_laser_active = shader.get_time()
        self.laser_active = False
        self.last_shoot = shader.get_time()

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
        if self.last_laser_active + self.laser_cooldown < shader.get_time() and not self.laser_active and display.get_rect().colliderect(
                pygame.Rect(self.hitbox[0].x + self.pos[0], self.hitbox[0].y + self.pos[1],
                            self.hitbox[0].w, self.hitbox[0].h)):
            self.last_shoot = shader.get_time()
            self.laser_active = True
        if self.laser_active and self.last_shoot + self.laser_duration < shader.get_time():
            self.last_laser_active = shader.get_time()
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
        self.pos[1] += self.speed * shader.get_dt()
        if self.health <= 0 and self.alive:
            self.alive = False
            self.on_death()
        if self.alive:
            display.blit(self.image, self.pos)
        if self.alive and self.pos[1] >= 0 and self.auto_shoot:
            self.projectiles.shoot(self.pos[0] + self.get_width() / 2, self.pos[1] + self.get_height() / 2)
        self.projectiles.draw(display, player)
        if self.alive:
            self.draw_health_bar()
            if self.pos[1] >= display.get_height() + self.get_height() + 100:
                self.alive = False
            for p_box in player.plane.hitbox:
                if self.collide((player.abs_pos[0] + p_box.x, player.abs_pos[1] + p_box.y, p_box.w, p_box.h)):
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
        self.next_frame = shader.get_time()
        self.frame_index = 0
        self.frame_delay = 150
        hitbox = [
            pygame.Rect(0 * self.image_scale, 11 * self.image_scale, 70 * self.image_scale, 72 * self.image_scale)
        ]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox, auto_shoot=False)

    def on_death(self):
        self.projectiles.shoot(self.pos[0], self.pos[1])
        shader.shake_amount += 1.6
        super().on_death()

    def draw(self):
        if self.next_frame + self.frame_delay <= shader.get_time():
            self.next_frame = shader.get_time()
            self.frame_index += 1
            if self.frame_index >= 5:
                self.frame_index = 0
            self.image = bullet_bomb_frames[self.frame_index]
        super().draw()


class NuclearBomb(Enemy):
    def __init__(self, pos):
        speed = 1
        health = 20
        enemy_projectiles = EnemyProjectiles([], 0, display, 99999)
        image = nuclear_bomb_frames[0]
        self.image_scale = 1
        self.next_frame = shader.get_time()
        self.frame_index = 0
        self.frame_delay = 250
        hitbox = [
            pygame.Rect(0 * self.image_scale, 0 * self.image_scale, 33 * self.image_scale, 83 * self.image_scale)
        ]
        super().__init__(speed, health, enemy_projectiles, image, pos, hitbox, auto_shoot=False,
                         particles_on_death=False)

    def on_death(self):
        shader.shake_amount += 2.4
        for enemy in enemies:
            if distance_between_points(enemy.pos, self.pos) <= 350:
                enemy.health -= distance_between_points(enemy.pos, self.pos) * -1 + 400

        if distance_between_points(player.pos, self.pos) <= 350:
            player.deal_damage(distance_between_points(player.pos, self.pos) * -1 + 325)

        anim = []
        for i in death_frames[0]:
            anim.append(pygame.transform.scale_by(i, 2.5))
        visual_effects.append(
            VFX(anim, self.pos[0] + self.get_width() / 4, self.pos[1] + self.get_height() + 5,
                delay=10))
        del anim
        super().on_death()

    def draw(self):
        if self.next_frame + self.frame_delay <= shader.get_time():
            self.next_frame = shader.get_time()
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


class LevelButton(Button):
    def __init__(self, x, y, level_number):
        self.level_number = str(level_number)
        x = x * 1.22
        y = y * 1.22
        self.texture_locked = locked_level_icon.copy()
        self.reached = lambda: user_stats.data["level_reached"] - 1 >= int(self.level_number)
        super().__init__(x, y, level_icon.get_width(), level_icon.get_height(), level_icon)
        self.rect.center = (x - 18, y)

    def draw(self, display, map_pos=(100, 100)):
        self.rect.x += round(map_pos[0])
        self.rect.y += round(map_pos[1])

        if user_stats.data["level_reached"] >= int(self.level_number):
            if self.is_clicked:
                display.blit(self.texture_down, self.rect)
            else:
                display.blit(self.texture, self.rect)
        else:
            display.blit(self.texture_locked, self.rect)

        if self.is_clicked:
            surf = self.font.render(self.level_number, True, (180, 180, 180))
        else:
            surf = self.font.render(self.level_number, True, (255, 255, 255))
        display.blit(surf, (self.rect.x + 40 / 2 - surf.get_width(), self.rect.y + 72 * 0.65 - surf.get_height()))
        self.rect.x -= round(map_pos[0])
        self.rect.y -= round(map_pos[1])

    def handle_event(self, event, map_pos=(100, 100)):
        if user_stats.data["level_reached"] >= int(self.level_number):
            self.rect.x += round(map_pos[0])
            self.rect.y += round(map_pos[1])
            res = False
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.is_hovered = True
                else:
                    self.is_hovered = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and event.button == 1:
                    self.is_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_clicked and event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        self.is_clicked = False
                        res = True
                    self.is_clicked = False
            self.rect.x -= round(map_pos[0])
            self.rect.y -= round(map_pos[1])
            return res
        else:
            return False

    def get_center(self, map_pos):
        self.rect.x += round(map_pos[0])
        self.rect.y += round(map_pos[1])
        res = self.rect.x + 83 * 0.65, self.rect.y + 35 * 0.65
        self.rect.x -= round(map_pos[0])
        self.rect.y -= round(map_pos[1])
        return res

    def get_level(self):
        level_data = []
        print(get_level_phase(1), get_level_phase(2), get_level_phase(3))
        level_data.append(
            [patterns.get_line_right, [get_level_phase(1), NormalEnemy, enemy_normal_frames[0].get_size(), 10, 50]])
        level_data.append(
            [patterns.get_line_left, [get_level_phase(2), NormalEnemy2, enemy_normal2_frames[0].get_size(), 10, 50]])
        level_data.append(
            [patterns.get_random, [get_level_phase(3.6), RotatingEnemy, enemy_normal_frames[0].get_size(), 10, 100]])
        level_data.append(
            [patterns.get_2x2_right, [get_level_phase(5.7), NormalEnemy, enemy_normal_frames[0].get_size()]])
        level_data.append(
            [patterns.get_2x2_left, [get_level_phase(5.7), NormalEnemy, enemy_normal_frames[0].get_size()]])
        level_data.append(
            [patterns.get_2x2_center, [get_level_phase(5.7), NormalEnemy, enemy_normal_frames[0].get_size()]])
        level_data.append(
            [patterns.get_nuclear_center,
             [get_level_phase(5.5), NormalEnemy2, NuclearBomb, enemy_normal_frames[0].get_size(),
              nuclear_bomb_frames[0].get_size()]])
        level_data.append(
            [patterns.get_2x2_center, [get_level_phase(5.2), NormalEnemy, enemy_normal_frames[0].get_size()]])
        patterns.save(level_data, "level" + self.level_number)
        enemies.clear()
        coins.clear()
        buffs_pickup.clear()
        enemies.extend(patterns.load("level" + self.level_number))
        return Level(enemies, int(self.level_number), 1, "sprites/background/desert.png")


mouse = Mouse()
player = Player()
enemies = []
levels = [LevelButton(198, 114, 1), LevelButton(200, 200, 2), LevelButton(260, 240, 3)]
