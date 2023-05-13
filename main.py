import random

import pygame.font

from scripts.game import *
from scripts.button import *
from scripts.label import Label

font = pygame.font.Font("font/font.ttf", 16)

cy = -300
for i in range(10):
    cy -= random.randint(50, 250)
    a = random.randint(0, 5)
    if a == 0:
        enemies.append(BulletBomb([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 1:
        enemies.append(BulletBomb([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 2:
        enemies.append(BulletBomb([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 3:
        enemies.append(BulletBomb([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 5:
        enemies.append(BulletBomb([
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

is_showing_dogtags = False
transparent_overlay = transparent_rect(display.get_size(), 0.65)
dogtags_timer_font = pygame.font.Font("font/font.ttf", 22)
dogtags_bg_pos = (
    display.get_width() / 2 - buy_dogtags.get_width() / 2, display.get_height() / 2 - buy_dogtags.get_height() / 2)
dogtags_bg_rect = pygame.Rect(dogtags_bg_pos[0], dogtags_bg_pos[1],
                              buy_dogtags.get_width(), buy_dogtags.get_height())
gui_title_font = pygame.font.Font("font/font.ttf", 28)
purchase_30_dogtags = Button(225, 475, gem_purchase.get_width(), gem_purchase.get_height(), gem_purchase, "10  ",
                             font="font/font.ttf", increase_font_size=0.15)
purchase_100_dogtags = Button(225, 550, gem_purchase.get_width(), gem_purchase.get_height(), gem_purchase, "30  ",
                              font="font/font.ttf", increase_font_size=0.15)
dogtags_gui_close = TexturedButton(
    display.get_width() / 2 + buy_dogtags.get_width() / 2 - gui_close.get_width() / 2 - 15,
    dogtags_bg_pos[1] - 5, gui_close.get_width(), gui_close.get_height(),
    gui_close, gui_close_hover)


dogtags_gui = pygame.Surface(display.get_size(), pygame.SRCALPHA)
dogtags_gui.blit(buy_dogtags, dogtags_bg_pos)
dogtags_gui.blit(text_label, (display.get_width() / 2 - text_label.get_width() / 2, dogtags_bg_pos[1] - 5))
surf = gui_title_font.render("CHARGE DOGTAG", False, (255, 255, 255))
dogtags_gui.blit(surf, (display.get_width() / 2 - surf.get_width() / 2, 430 - buy_dogtags.get_height() / 2))
dogtags_gui.blit(dogtags_pile, (display.get_width() / 2 - dogtags_pile.get_width() / 2, 200))
dogtags_gui.blit(single_dogtag, (purchase_100_dogtags.rect.centerx - 175, purchase_100_dogtags.rect.centery - single_dogtag.get_height() / 2))
dogtags_gui.blit(single_dogtag, (purchase_30_dogtags.rect.centerx - 175, purchase_30_dogtags.rect.centery - single_dogtag.get_height() / 2))
dogtags_gui.blit(single_dogtag, (purchase_100_dogtags.rect.centerx - 175, purchase_100_dogtags.rect.centery - single_dogtag.get_height() / 2))
surf = dogtags_timer_font.render("x100", False, (255, 255, 255))
dogtags_gui.blit(surf, (purchase_100_dogtags.rect.centerx - 125, purchase_100_dogtags.rect.centery - surf.get_height() / 2))
surf = dogtags_timer_font.render("x30", False, (255, 255, 255))
dogtags_gui.blit(surf, (purchase_30_dogtags.rect.centerx - 125, purchase_30_dogtags.rect.centery - surf.get_height() / 2))
dogtags_gui.blit(single_dogtag, (purchase_30_dogtags.rect.centerx - 175, purchase_30_dogtags.rect.centery - single_dogtag.get_height() / 2))

parking_area_1 = Button(50, 200, gui_parking_area.get_width(), gui_parking_area.get_height(), gui_parking_area)
plane_vfx = []
plane_1_scale = 1.3

current_plane = user_stats.get_plane()(plane_vfx)
# 0: main gui, 1 dogtags shop, 2 planes menu
current_gui = 0
blit_main_gui = True
while True:
    plane_surf = pygame.Surface(current_plane.image.get_size(), pygame.SRCALPHA)
    user_stats.update_dogtags()

    display.blit(ui_background, (0, 0))
    coins_label.draw(display)
    coins_label.update(user_stats.data["coins"])
    gems_label.draw(display)
    gems_label.update(user_stats.data["gems"])
    dogtags_label.draw(display)
    dogtags_label.update(user_stats.data["dogtags"])

    if blit_main_gui:
        singleplayer_button.draw(display)

        parking_area_1.draw(display)
        current_plane.update(0, plane_surf, [], (0, 0), is_dummy=True)
        plane_surf.blit(current_plane.image,
                        (0, 0))
        for vfx in plane_vfx:
            vfx.update(plane_surf)
            if vfx.ended:
                plane_vfx.remove(vfx)

        surf = pygame.transform.scale_by(plane_surf, plane_1_scale)
        display.blit(surf, (parking_area_1.rect.x+parking_area_1.rect.w/2-surf.get_width()/2,
                            parking_area_1.rect.y+parking_area_1.rect.h/2-surf.get_height()/2-15))

    if current_gui == 1:
        display.blit(transparent_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        display.blit(dogtags_gui, (0, 0))
        if mouse.collideswith(
                [display.get_width() / 2 + buy_dogtags.get_width() / 2 - gui_close.get_width() / 2 - 15 + 8,
                 dogtags_bg_pos[1] - 5 + 8,
                 gui_close.get_width() - 16, gui_close.get_height() - 16]):
            dogtags_gui_close.draw(display)
        else:
            display.blit(gui_close,
                         (display.get_width() / 2 + buy_dogtags.get_width() / 2 - gui_close.get_width() / 2 - 15,
                          dogtags_bg_pos[1] - 5))

        
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
    elif current_gui == 2:
        display.blit(planes_gui_planes_station, (display.get_width()/2-planes_gui_planes_station.get_width()/2, coins_label.get_height()))
        display.blit(planes_gui_arrow_back_frame, (-40, display.get_height()-planes_gui_arrow_back_frame.get_height()))
        display.blit(arrow_back, (16-arrow_back.get_width()/2, display.get_height()-planes_gui_arrow_back_frame.get_height()+31-arrow_back.get_height()/2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if current_gui == 0:
            if singleplayer_button.handle_event(event):
                if user_stats.can_purchase("dogtags", 5):
                    user_stats.data["dogtags"] -= 5
                    play_level(level1)
                elif not user_stats.can_purchase("dogtags", 5):
                    current_gui = 1
            if parking_area_1.handle_event(event):
                current_gui = 2
                blit_main_gui = False
        elif current_gui == 1:
            if purchase_100_dogtags.handle_event(event) and \
                user_stats.can_purchase("gems", 30):
                user_stats.data["gems"] -= 30
                user_stats.data["dogtags"] += 100

            if purchase_30_dogtags.handle_event(event) and \
                    user_stats.can_purchase("gems", 10):
                user_stats.data["gems"] -= 10
                user_stats.data["dogtags"] += 30

            if dogtags_gui_close.handle_event(event):
                current_gui = 0
        elif current_gui == 2:
            pass

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dogtags_plus_rect.collidepoint(mouse.get_pos()):
                    current_gui = 1
    
    mouse.draw()
    shader.draw()  # , "time": shader_time
    clock.tick(120)
