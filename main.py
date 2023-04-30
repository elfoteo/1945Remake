import random

import pygame.font

from scripts.game import *
from scripts.button import Button
from scripts.label import Label

font = pygame.font.Font("font/font.ttf", 16)

cy = -300
for i in range(10):
    cy -= random.randint(50, 250)
    a = random.randint(0, 5)
    if a == 0:
        enemies.append(LaserEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 1:
        enemies.append(LaserEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 2:
        enemies.append(LaserEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 3:
        enemies.append(LaserEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 5:
        enemies.append(LaserEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))

mouse.unlock()
singleplayer_button = Button(display.get_width() / 2 - (148 * 1.5) / 2, 700, 148 * 1.5, 37 * 1.5,
                             'sprites/ui/green_button.png',
                             text="Single Player",
                             font="font/font.ttf", increase_font_size=0.1)

dogtags_label = Label(user_stats.data["dogtags"], dogtag_icon, (0, 0), font, suffix="/100")
coins_label = Label(user_stats.data["coins"], coin_icon, (dogtags_label.get_width(), 0), font)
gems_label = Label(user_stats.data["gems"], gem_icon, (coins_label.get_width() + dogtags_label.get_width(), 0), font)

level1 = Level(enemies, 1, 1)

dogtags_plus_rect = pygame.Rect(93 * 1.25, 3 * 1.25, 22 * 1.25, 21 * 1.25)
dogtags_plus = False
transparent_overlay = transparent_rect(display.get_size(), 0.65)
dogtags_timer_font = pygame.font.Font("font/font.ttf", 22)
dogtags_transparent_bg_blitpos = (
    display.get_width() / 2 - buy_dogtags.get_width() / 2, display.get_height() / 2 - buy_dogtags.get_height() / 2)
dogtags_transparent_bg_rect = pygame.Rect(dogtags_transparent_bg_blitpos[0], dogtags_transparent_bg_blitpos[1],
                                          buy_dogtags.get_width(), buy_dogtags.get_height())
gui_title_font = pygame.font.Font("font/font.ttf", 28)
purchase_30_dogtags = Button(225, 475, gem_purchase.get_width(), gem_purchase.get_height(), gem_purchase, "10  ",
                             font="font/font.ttf", increase_font_size=0.15)
purchase_100_dogtags = Button(225, 550, gem_purchase.get_width(), gem_purchase.get_height(), gem_purchase, "30  ",
                              font="font/font.ttf", increase_font_size=0.15)
while True:
    shader_time += 1
    user_stats.update_dogtags()

    display.blit(ui_background, (0, 0))
    coins_label.draw(display)
    coins_label.update(user_stats.data["coins"])
    gems_label.draw(display)
    gems_label.update(user_stats.data["gems"])
    dogtags_label.draw(display)
    dogtags_label.update(user_stats.data["dogtags"])
    singleplayer_button.draw(display)

    if dogtags_plus:
        display.blit(transparent_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        display.blit(buy_dogtags, dogtags_transparent_bg_blitpos)
        display.blit(text_label, (display.get_width() / 2 - text_label.get_width() / 2,
                                  dogtags_transparent_bg_blitpos[1] - 5))
        surf = gui_title_font.render("CHARGE DOGTAG", False, (255, 255, 255))
        display.blit(surf, (display.get_width() / 2 - surf.get_width() / 2, 430 - buy_dogtags.get_height() / 2))

        if mouse.collideswith(
                [display.get_width() / 2 + buy_dogtags.get_width() / 2 - gui_close.get_width() / 2 - 15 + 8,
                 dogtags_transparent_bg_blitpos[1] - 5 + 8,
                 gui_close.get_width() - 16, gui_close.get_height() - 16]):
            display.blit(gui_close_hover,
                         (display.get_width() / 2 + buy_dogtags.get_width() / 2 - gui_close.get_width() / 2 - 15,
                          dogtags_transparent_bg_blitpos[1] - 5))
            if mouse.get_button(0):
                dogtags_plus = False
        else:
            display.blit(gui_close,
                         (display.get_width() / 2 + buy_dogtags.get_width() / 2 - gui_close.get_width() / 2 - 15,
                          dogtags_transparent_bg_blitpos[1] - 5))

        display.blit(dogtags_pile, (display.get_width() / 2 - dogtags_pile.get_width() / 2, 200))
        if user_stats.dogtags_full:
            surf = dogtags_timer_font.render("Full Dogtag!", False, (183, 240, 80))
            display.blit(surf, (display.get_width() / 2 - surf.get_width() / 2, 375))
        else:
            surf = dogtags_timer_font.render("Time until next tag: ", False, (183, 240, 80))
            display.blit(surf, (display.get_width() / 2 - surf.get_width() / 2, 375))
            surf = dogtags_timer_font.render(user_stats.get_next_dogtag_time(), False, (183, 240, 80))
            display.blit(surf, (display.get_width() / 2 - surf.get_width() / 2, 425))
        purchase_30_dogtags.draw(display)
        purchase_100_dogtags.draw(display)
        display.blit(gem_icon, (
            purchase_30_dogtags.rect.centerx + 10, purchase_30_dogtags.rect.centery - gem_icon.get_height() / 2))
        display.blit(gem_icon, (
            purchase_100_dogtags.rect.centerx + 10, purchase_100_dogtags.rect.centery - gem_icon.get_height() / 2))
        display.blit(single_dogtag, (
            purchase_30_dogtags.rect.centerx - 175, purchase_30_dogtags.rect.centery - single_dogtag.get_height() / 2))
        display.blit(single_dogtag, (
            purchase_100_dogtags.rect.centerx - 175,
            purchase_100_dogtags.rect.centery - single_dogtag.get_height() / 2))
        display.blit(single_dogtag, (
            purchase_30_dogtags.rect.centerx - 175, purchase_30_dogtags.rect.centery - single_dogtag.get_height() / 2))
        display.blit(single_dogtag, (
            purchase_100_dogtags.rect.centerx - 175,
            purchase_100_dogtags.rect.centery - single_dogtag.get_height() / 2))
        surf = dogtags_timer_font.render("x100", False, (255, 255, 255))
        display.blit(surf, (
            purchase_100_dogtags.rect.centerx - 125, purchase_100_dogtags.rect.centery - surf.get_height() / 2))
        surf = dogtags_timer_font.render("x30", False, (255, 255, 255))
        display.blit(surf,
                     (purchase_30_dogtags.rect.centerx - 125, purchase_30_dogtags.rect.centery - surf.get_height() / 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if not dogtags_plus and singleplayer_button.handle_event(event) and \
                user_stats.can_purchase("dogtags", 5):
            user_stats.data["dogtags"] -= 5
            play_level(level1)

        if dogtags_plus and purchase_100_dogtags.handle_event(event) and \
                user_stats.can_purchase("gems", 30):
            user_stats.data["gems"] -= 30
            user_stats.data["dogtags"] += 100

        if dogtags_plus and purchase_30_dogtags.handle_event(event) and \
                user_stats.can_purchase("gems", 10):
            user_stats.data["gems"] -= 10
            user_stats.data["dogtags"] += 30

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dogtags_plus and not dogtags_transparent_bg_rect.collidepoint(mouse.get_pos()):
                    dogtags_plus = False
                if dogtags_plus_rect.collidepoint(mouse.get_pos()):
                    dogtags_plus = True

    mouse.draw()
    shader.draw(program_args={"tex": 0})  # , "time": shader_time
    clock.tick(120)
