from scripts.engine import *


def pause(level):
    paused = True
    shader.ingame = False
    scr_copy = display.copy().convert_alpha()
    scr_copy.fill((255, 255, 255, 180), None, pygame.BLEND_RGBA_MULT)
    scr_copy_original = display.copy()
    resume_button = Button(display.get_width() / 2 - (148 * 1.25) / 2, display.get_height() / 2 - 35, 148 * 1.25,
                           40 * 1.25,
                           'sprites/ui/green_button.png',
                           text="Resume",
                           font="font/font.ttf", increase_font_size=0.1)
    exit_button = Button(display.get_width() / 2 - (148 * 1.25) / 2, display.get_height() / 2 + 35, 148 * 1.25,
                         40 * 1.25,
                         'sprites/ui/yellow_button.png',
                         text="Exit",
                         font="font/font.ttf", increase_font_size=0.1)
    mouse.unlock()
    unpause_timer = 3
    last_time = time.time()
    clicked_resume = False
    exit_popup = Popup("EXIT MISSION", "Cancel", "Exit", "Your flight results will be lost")
    screen_copy = display.copy()
    while paused:
        display.fill((0, 0, 0))
        if clicked_resume:
            display.blit(scr_copy_original, (0, 0))
        else:
            display.blit(scr_copy, (0, 0))
            resume_button.draw(display)
            exit_button.draw(display)

        if clicked_resume:
            surf = big_font.render(str(unpause_timer), True, (255, 255, 255))
            display.blit(surf, (
                display.get_width() / 2 - surf.get_width() / 2, display.get_height() / 2 - surf.get_height() / 2))
            if last_time + 1 < time.time():
                unpause_timer -= 1
                last_time = time.time()
            if unpause_timer <= 0:
                paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if not clicked_resume:
                if resume_button.handle_event(event):
                    mouse.lock()
                    clicked_resume = True
                    last_time = time.time()
                elif exit_button.handle_event(event):
                    mouse.unlock()
                    if exit_popup.get_result(screen_copy) == 2:
                        defeat_screen(level)
                        return "quit"
        shader.draw(display)
        screen_copy = display.copy()
        clock.tick(120)
    shader.ingame = True


def win_screen(level):
    shader.ingame = False
    shader.red_overlay = 0
    shader.shake_amount = 0
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
    rewards = level.get_rewards()
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
            pivot_rotate(eagle_wing_bottom_r, wings_movement * bottom_wings_mult, bottom_pivot_r, pygame.Vector2(0, 0))[
                0],
            (display.get_width() / 2 - eagle_head.get_width(), 105 + win_label.get_height()))
        display.blit(
            pivot_rotate(eagle_wing_bottom_l, -(wings_movement * bottom_wings_mult), bottom_pivot_l,
                         pygame.Vector2(0, 0))[0],
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

        display.blit(level_banner, (display.get_width() / 2 - level_banner.get_width() / 2, 300))
        surf = normal_font.render(level.name, True, (255, 255, 255))
        display.blit(surf, (
            display.get_width() / 2 - surf.get_width() / 2,
            300 + level_banner.get_height() / 2 - surf.get_height() / 2))

        display.blit(level_rewards_bg, (display.get_width() / 2 - level_rewards_bg.get_width() / 2, 375))
        level_rewards_rect = level_rewards_bg.get_rect()
        display.blit(pile_of_coins, (display.get_width() / 2 - 100,
                                     375 + level_rewards_rect.h / 2 - pile_of_coins.get_height()))
        surf = font_medium_small.render(str(rewards[0] + user_stats.data["ingame_coins"]), True, (255, 255, 255))
        display.blit(surf,
                     (display.get_width() / 2 - 100 + pile_of_coins.get_width() / 2 - surf.get_width() / 2,
                      375 + level_rewards_rect.h / 2 - pile_of_coins.get_height() + 50))
        display.blit(pile_of_gems, (display.get_width() / 2 + 100 - pile_of_gems.get_width(),
                                    375 + level_rewards_rect.h / 2 - pile_of_gems.get_height()))
        surf = font_medium_small.render(str(rewards[1]), True, (255, 255, 255))
        display.blit(surf,
                     (display.get_width() / 2 + 100 - pile_of_gems.get_width() / 2 - surf.get_width() / 2,
                      375 + level_rewards_rect.h / 2 - pile_of_coins.get_height() + 50))
        pass_lvl.draw(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if pass_lvl.handle_event(event):
                level.give_rewards()
                user_stats.add_coins(user_stats.data["ingame_coins"])
                user_stats.data["ingame_coins"] = 0
                return
        mouse.draw()
        shader.draw(display)
        clock.tick(120)


def defeat_screen(level):
    shader.ingame = False
    shader.red_overlay = 0
    shader.shake_amount = 0
    mouse.unlock()

    normal_font = pygame.font.SysFont("", 30)
    pass_lvl = Button(screen.get_width() / 2 - pass_lvl_button.get_width() / 2, 730, pass_lvl_button.get_width(),
                      pass_lvl_button.get_height(), pass_lvl_button)
    while True:
        display.blit(ui_background, (0, 0))

        display.blit(level_defeated, (display.get_width() / 2 - level_defeated.get_width() / 2, 85))

        display.blit(level_banner, (display.get_width() / 2 - level_banner.get_width() / 2, 300))
        surf = normal_font.render(level.name, True, (255, 255, 255))
        display.blit(surf, (
            display.get_width() / 2 - surf.get_width() / 2,
            300 + level_banner.get_height() / 2 - surf.get_height() / 2))

        display.blit(level_rewards_bg, (display.get_width() / 2 - level_rewards_bg.get_width() / 2, 375))
        level_rewards_rect = level_rewards_bg.get_rect()
        display.blit(pile_of_coins, (display.get_width() / 2 - pile_of_coins.get_width() / 2,
                                     375 + level_rewards_rect.h / 2 - pile_of_coins.get_height()))
        surf = font_medium_small.render(str(user_stats.data["ingame_coins"]), True, (255, 255, 255))
        display.blit(surf,
                     (display.get_width() / 2 - surf.get_width() / 2,
                      375 + level_rewards_rect.h / 2 - pile_of_coins.get_height() + 50))
        pass_lvl.draw(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if pass_lvl.handle_event(event):
                user_stats.add_coins(user_stats.data["ingame_coins"])
                user_stats.data["ingame_coins"] = 0
                return
        mouse.draw()
        shader.draw(display)
        clock.tick(120)


def play_level(level):
    player.reset()
    shader.ingame = True
    mouse.lock()
    # a lot of timers
    end_anim_trigger = False
    end_anim = time.time()
    end_anim_cooldown = 2
    started_animation = False
    end_animation_y_counter = 0
    scroll_y = -level.bg.get_height() + screen.get_height()
    bg_copy = level.bg.copy()
    before_end_timer = None
    before_end_cooldown = 2

    while True:
        # display.fill((32, 56, 212))
        scroll_y += scroll_speed
        display.blit(level.bg, (0, scroll_y))
        display.blit(bg_copy, (0, scroll_y - bg_copy.get_height()))
        if scroll_y >= level.bg.get_height():
            scroll_y = 0

        for coin in coins:
            coin.draw()
            if not coin.alive:
                coins.remove(coin)

        for buff_pickup in buffs_pickup:
            buff_pickup.draw()
            if not buff_pickup.alive:
                buffs_pickup.remove(buff_pickup)

        new_enemies = level.enemies.copy()
        for enemy in level.enemies:
            enemy.draw()
            if not enemy.alive and enemy.projectiles.projectiles == []:
                new_enemies.remove(enemy)
        level.enemies = new_enemies.copy()
        del new_enemies
        if level.enemies == [] and coins == [] and not level.finished and not end_anim_trigger:
            end_anim_trigger = True
            end_anim = time.time()

        if end_anim_trigger and end_anim + end_anim_cooldown < time.time() and not started_animation:
            level.finished = True
            level.finished_timestamp = shader.get_ingame_time()
            started_animation = True
            player.auto_controlled = True
            player.auto_rel = [0, 0]

        if level.finished:
            player.auto_controlled = True
            y_movment = ((level.finished_timestamp + level.finished_cooldown - shader.get_ingame_time()) / 1000 - 4)
            if y_movment <= 0:
                y_movment *= 4 + end_animation_y_counter * 0.13
                end_animation_y_counter += 1
            player.auto_rel = [
                0,
                y_movment * shader.get_dt()
            ]
            player.is_dummy = True

        if -100 >= player.abs_pos[1] >= -120:
            before_end_timer = time.time()

        if before_end_timer is not None and before_end_timer + before_end_cooldown < time.time() and level.finished:
            player.auto_controlled = False
            win_screen(level)
            user_stats.data["coins"] += user_stats.data["ingame_coins"]
            user_stats.data["ingame_coins"] = 0
            return True
        player.draw()  # draw, update the actual plane
        # draw the visual effects for the plane, explosions, projectiles
        for vfx in visual_effects:
            vfx.update(display)
            if vfx.ended:
                visual_effects.remove(vfx)

        player.draw_gui()  # draw the gui
        if before_end_timer is None and not player.plane.alive:
            before_end_timer = time.time()
            player.auto_controlled = True
            player.auto_rel = [0, 0]

        if not player.plane.alive and before_end_timer is not None and before_end_timer + before_end_cooldown < time.time():
            defeat_screen(level)
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pause(level) == "quit":
                        return False

        mouse.draw()
        shader.draw(display)
        clock.tick(120)
