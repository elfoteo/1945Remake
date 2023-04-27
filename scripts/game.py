import math
import sys

import pygame

from scripts.button import Button
from scripts.engine import *


def pause():
    paused = True
    scr_copy = display.copy().convert_alpha()
    scr_copy.fill((255, 255, 255, 180), None, pygame.BLEND_RGBA_MULT)
    mouse.unlock()
    while paused:
        display.fill((0, 0, 0))
        display.blit(scr_copy, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                    mouse.lock()
        shader.draw(program_args={"tex": 0})
        clock.tick(120)


def win_screen(level_name="Level 31 - EASY"):
    mouse.unlock()
    head_movement_mult = 2

    wings_linear = 0
    wings_rot_mult = 2
    min_x = -1.0
    max_x = 1.0
    direction = True
    pivot_r = 116 * 1.2, 47 * 1.2
    pivot_l = eagle_wing_l.get_width() - (116 * 1.2), (47 * 1.2)
    bottom_pivot_r = 21 * 1.2, 12 * 1.2
    bottom_pivot_l = eagle_wing_bottom_l.get_width() - (21 * 1.2), 12 * 1.2
    bottom_wings_mult = 4
    wings_speed = 0.012

    normal_font = pygame.font.SysFont("", 30)
    pass_lvl = Button(screen.get_width() / 2 - pass_lvl_button.get_width() / 2, 730, pass_lvl_button.get_width(),
                      pass_lvl_button.get_height(), pass_lvl_button)
    while True:
        display.blit(ui_background, (0, 0))

        wings_linear += wings_speed if direction else -wings_speed
        if wings_linear <= -1:
            direction = True
        elif wings_linear >= 1:
            direction = False
        wings_movement = (2 * (wings_linear - min_x) / (max_x - min_x) - 1) * wings_rot_mult

        display.blit(eagle_head,
                     (display.get_width() / 2 - eagle_head.get_width() / 2, 85 + wings_movement * head_movement_mult))
        display.blit(pivot_rotate(eagle_wing_r, wings_movement, pivot_r, pygame.Vector2(0, 0))[0],
                     (display.get_width() / 2 - eagle_head.get_width() - eagle_wing_r.get_width() / 2 - 25,
                      60 + wings_movement * head_movement_mult))
        display.blit(pivot_rotate(eagle_wing_l, -wings_movement, pivot_l, pygame.Vector2(0, 0))[0],
                     (display.get_width() / 2 + eagle_head.get_width() - eagle_wing_r.get_width() / 2 + 25,
                      60 + wings_movement * head_movement_mult))

        display.blit(
            pivot_rotate(eagle_wing_bottom_r, wings_movement * bottom_wings_mult, bottom_pivot_r, pygame.Vector2(0, 0))[0],
            (display.get_width() / 2 - eagle_head.get_width(), 105 + win_label.get_height()))
        display.blit(
            pivot_rotate(eagle_wing_bottom_l, -(wings_movement * bottom_wings_mult), bottom_pivot_l, pygame.Vector2(0, 0))[0],
            (display.get_width() / 2 + eagle_head.get_width() - eagle_wing_bottom_r.get_width(),
             105 + win_label.get_height()))

        display.blit(win_star_circle,
                     (display.get_width() / 2 - win_star_circle.get_width() / 2, 120 + win_label.get_height()))

        display.blit(win_tail_r, (
            display.get_width() / 2 - win_label.get_width() / 2 - win_tail_r.get_width(),
            115 + win_label.get_height() / 2))
        display.blit(win_shadow_r, (display.get_width() / 2 - win_label.get_width() / 2 - win_shadow_r.get_width(),
                                    134 + win_label.get_height() / 2))
        display.blit(win_front_r, (display.get_width() / 2 - win_label.get_width() / 2 - win_shadow_r.get_width(),
                                   107 + win_label.get_height() / 2))

        display.blit(win_tail_l,
                     (display.get_width() / 2 + win_label.get_width() / 2, 115 + win_label.get_height() / 2))
        display.blit(win_shadow_l,
                     (display.get_width() / 2 + win_label.get_width() / 2, 134 + win_label.get_height() / 2))
        display.blit(win_front_l, (display.get_width() / 2 + win_label.get_width() / 2 - win_shadow_r.get_width(),
                                   107 + win_label.get_height() / 2))

        display.blit(win_label, (display.get_width() / 2 - win_label.get_width() / 2, 120))

        display.blit(win_star,
                     (round(display.get_width() / 2 - win_star.get_width() / 2),
                      round(
                          120 + win_label.get_height() - win_star.get_height() / 2 + win_star_circle.get_height() / 2 - 12)))

        display.blit(level_banner, (display.get_width() / 2 - level_banner.get_width() / 2, 270))
        surf = normal_font.render(level_name, True, (255, 255, 255))
        display.blit(surf, (
        display.get_width() / 2 - surf.get_width() / 2, 270 + level_banner.get_height() / 2 - surf.get_height() / 2))

        display.blit(level_banner, (display.get_width() / 2 - level_banner.get_width() / 2, 550))
        surf = normal_font.render("REWARDS", True, (255, 255, 255))
        display.blit(surf,
                     (display.get_width() / 2 - surf.get_width() / 2, 550 + level_banner.get_height() / 2 - surf.get_height() / 2))

        display.blit(level_rewards_bg, (display.get_width()/2-level_rewards_bg.get_width()/2, 600))

        pass_lvl.draw(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if pass_lvl.handle_event(event):
                return
        mouse.draw()
        shader.draw(program_args={"tex": 0})
        clock.tick(120)


def play_level(level):
    mouse.lock()
    # TODO: change all to work with delta time
    # win_screen()
    while True:
        display.fill((32, 56, 212))
        for coin in coins:
            coin.draw()
            if not coin.alive:
                coins.remove(coin)

        new_enemies = level.enemies.copy()
        for enemy in level.enemies:
            enemy.draw()
            if not enemy.alive and enemy.projectiles.projectiles == []:
                new_enemies.remove(enemy)
                # TODO: Explosion
        level.enemies = new_enemies.copy()
        del new_enemies
        if level.enemies == [] and coins == [] and not level.finished:
            level.finished = time.time() * 1000

        if level.finished + level.finished_cooldown < time.time() * 1000 and level.finished:
            win_screen(level_name=level.name)
            user_stats.data["coins"] += user_stats.data["ingame_coins"]
            user_stats.data["ingame_coins"] = 0
            return
        player.draw()

        for vfx in visual_effects:
            vfx.update(display)
            if vfx.ended:
                visual_effects.remove(vfx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        mouse.draw()
        shader.draw(program_args={"tex": 0})
        clock.tick(120)
