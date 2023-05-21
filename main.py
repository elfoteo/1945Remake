import pygame.draw

from scripts.game import *
from scripts.label import Label
from scripts.planes import all_planes

mouse.unlock()
singleplayer_button = Button(display.get_width() / 2 - (148 * 1.5) / 2, 700, 148 * 1.5, 37 * 1.5,
                             green_button,
                             text="Single Player",
                             font="font/font.ttf", increase_font_size=0.1)

dogtags_label = Label(user_stats.data["dogtags"], dogtag_icon, (0, 0), font_small, suffix="/100")
coins_label = Label(user_stats.data["coins"], coin_icon, (dogtags_label.get_width(), 0), font_small)
gems_label = Label(user_stats.data["gems"], gem_icon, (coins_label.get_width() + dogtags_label.get_width(), 0),
                   font_small)

dogtags_plus_rect = pygame.Rect(93 * 1.25, 3 * 1.25, 22 * 1.25, 21 * 1.25)

is_showing_dogtags = False
transparent_overlay = transparent_rect(display.get_size(), 0.65)
dogtags_timer_font = pygame.font.Font("font/font.ttf", 22)
dogtags_bg_pos = (
    display.get_width() / 2 - buy_dogtags.get_width() / 2, display.get_height() / 2 - buy_dogtags.get_height() / 2)
dogtags_bg_rect = pygame.Rect(dogtags_bg_pos[0], dogtags_bg_pos[1],
                              buy_dogtags.get_width(), buy_dogtags.get_height())
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
dogtags_gui.blit(single_dogtag, (
    purchase_100_dogtags.rect.centerx - 175, purchase_100_dogtags.rect.centery - single_dogtag.get_height() / 2))
dogtags_gui.blit(single_dogtag, (
    purchase_30_dogtags.rect.centerx - 175, purchase_30_dogtags.rect.centery - single_dogtag.get_height() / 2))
dogtags_gui.blit(single_dogtag, (
    purchase_100_dogtags.rect.centerx - 175, purchase_100_dogtags.rect.centery - single_dogtag.get_height() / 2))
surf = dogtags_timer_font.render("x100", False, (255, 255, 255))
dogtags_gui.blit(surf,
                 (purchase_100_dogtags.rect.centerx - 125, purchase_100_dogtags.rect.centery - surf.get_height() / 2))
surf = dogtags_timer_font.render("x30", False, (255, 255, 255))
dogtags_gui.blit(surf,
                 (purchase_30_dogtags.rect.centerx - 125, purchase_30_dogtags.rect.centery - surf.get_height() / 2))
dogtags_gui.blit(single_dogtag, (
    purchase_30_dogtags.rect.centerx - 175, purchase_30_dogtags.rect.centery - single_dogtag.get_height() / 2))

parking_area_1 = Button(50, 200, gui_parking_area.get_width(), gui_parking_area.get_height(), gui_parking_area)
arrow_back_btn = Button(57 * 1.2 - 40, display.get_height() - planes_gui_arrow_back_frame.get_height() + 33 * 1.2,
                        arrow_back.get_width(), arrow_back.get_height(), arrow_back)
plane_vfx = []
plane_parking_scale = 1.3

plane_level = user_stats.data["planes"][user_stats.get_plane()][1]
current_plane = user_stats.get_plane()(plane_vfx, plane_level)
previous_plane = current_plane
map_pos = (0, display.get_height() - italy_map.get_height() - planes_gui_arrow_back_frame.get_height() / 2)
# 0: main gui, 1 dogtags shop, 2 planes menu, 3 level selection
current_gui = 0
blit_main_gui = True
was_mouse_button_down = False
mouse_button_up_event = False
# Drawing all main-menu GUI/s components
surf = pygame.Surface((101, 30), pygame.SRCALPHA)
surf.fill((0, 0, 0, 0))
upgrade_button = Button(display.get_width() / 2 - planes_gui_progressbar_container.get_width() / 2+43,
                        display.get_height() - planes_gui_container.get_height() - planes_gui_progressbar_container.get_height()+52,
                        101, 30, surf, "", font="font/font.ttf", increase_font_size=0.25)
surf = pygame.Surface((101, 30), pygame.SRCALPHA)
surf.fill((0, 0, 0, 50))
upgrade_button.texture_down = surf

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

        surf = pygame.transform.scale_by(plane_surf, plane_parking_scale)
        display.blit(surf, (parking_area_1.rect.x + parking_area_1.rect.w / 2 - surf.get_width() / 2,
                            parking_area_1.rect.y + parking_area_1.rect.h / 2 - surf.get_height() / 2 - 24))

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
            surf = dogtags_timer_font.render("Restore 1 in: " + user_stats.get_next_dogtag_time(), True, (183, 240, 80))
            display.blit(surf, (display.get_width() / 2 - surf.get_width() / 2, 375))
        purchase_30_dogtags.draw(display)
        purchase_100_dogtags.draw(display)
        display.blit(gem_icon, (
            purchase_30_dogtags.rect.centerx + 10, purchase_30_dogtags.rect.centery - gem_icon.get_height() / 2))
        display.blit(gem_icon, (
            purchase_100_dogtags.rect.centerx + 10, purchase_100_dogtags.rect.centery - gem_icon.get_height() / 2))
    elif current_gui == 2:
        x = 0
        y = 0
        plane_img_scale = 0.435
        for plane in all_planes:
            if plane.name != current_plane.name:
                is_plane_unlocked = user_stats.data["planes"][type(plane)][0]
                base_coord = (5 + x * 237 * plane_img_scale,
                              display.get_height() - planes_gui_container.get_height() + planes_gui_plane_name_label.get_height() + 2 + y * 246 * plane_img_scale)
                display.blit(planes_gui_not_selected_plane if is_plane_unlocked else planes_gui_not_unlocked_plane,
                             base_coord)
                display.blit(plane.icon, (
                    base_coord[0] + planes_gui_not_selected_plane.get_width() / 2 - plane.icon.get_width() / 2,
                    base_coord[1] + planes_gui_not_selected_plane.get_height() / 2 - plane.icon.get_height() / 2 - 10))
                for i in range(plane.rank):
                    display.blit(plane_star_rank, (base_coord[0] + planes_gui_not_selected_plane.get_width() / 2 - plane.icon.get_width() / 2 + i*10,
                                                   base_coord[1] + planes_gui_not_selected_plane.get_height()-26))
                if mouse_button_up_event and not was_mouse_button_down and \
                        pygame.Rect(base_coord[0],
                                    base_coord[1],
                                    planes_gui_not_selected_plane.get_width(),
                                    planes_gui_not_selected_plane.get_height()).collidepoint(mouse.get_pos()):
                    plane_vfx = []
                    if is_plane_unlocked:  # if the player has unlocked the plane we change his previous plane to be the current last plane
                        previous_plane = current_plane
                    level = user_stats.data["planes"][type(plane)][1]
                    current_plane = type(plane)(plane_vfx, level)
                    user_stats.set_plane(type(plane))
                    player.refresh_plane()
            x += 1
            if x >= 4:
                y += 1
                x = 0
        display.blit(planes_gui_container, (
            0, display.get_height() - planes_gui_container.get_height() + planes_gui_plane_name_label.get_height()))
        # 2 loops to blit the selected plane on top of the unselected ones
        x = 0
        y = 0
        for plane in all_planes:
            if plane.name == current_plane.name:
                is_plane_unlocked = user_stats.data["planes"][type(plane)][0]
                base_coord = (5 + x * 237 * plane_img_scale,
                              display.get_height() - planes_gui_container.get_height() + planes_gui_plane_name_label.get_height() + 2 + y * 246 * plane_img_scale)
                display.blit(planes_gui_selected_plane if is_plane_unlocked else planes_gui_not_unlocked_selected_plane,
                             (5 + x * 237 * plane_img_scale,
                              display.get_height() - planes_gui_container.get_height() + planes_gui_plane_name_label.get_height() + 2 + y * 246 * plane_img_scale))
                new_icon = pygame.transform.scale_by(plane.icon, 1.07)
                display.blit(plane.icon, (
                    base_coord[0] + planes_gui_not_selected_plane.get_width() / 2 - plane.icon.get_width() / 2,
                    base_coord[1] + planes_gui_not_selected_plane.get_height() / 2 - plane.icon.get_height() / 2 - 10))
                for i in range(plane.rank):
                    display.blit(plane_star_rank, (base_coord[0] + planes_gui_not_selected_plane.get_width() / 2 - plane.icon.get_width() / 2 + i*10,
                                                   base_coord[1] + planes_gui_not_selected_plane.get_height()-26))

            x += 1
            if x >= 4:
                y += 1
                x = 0
        display.blit(planes_gui_plane_station,
                     (display.get_width() / 2 - planes_gui_plane_station.get_width() / 2, coins_label.get_height()))
        display.blit(planes_gui_plane_name_label,
                     (display.get_width() / 2 - planes_gui_plane_name_label.get_width() / 2,
                      display.get_height() - planes_gui_container.get_height() - planes_gui_progressbar_container.get_height() + 45))
        surf = font_small.render(current_plane.name, True, (255, 255, 255))
        display.blit(surf, (display.get_width() / 2 - surf.get_width() / 2,
                            display.get_height() - planes_gui_container.get_height() - planes_gui_progressbar_container.get_height() + 45 + planes_gui_plane_name_label.get_height() / 2 - surf.get_height() / 2))
        display.blit(planes_gui_progressbar_container, (
            display.get_width() / 2 - planes_gui_progressbar_container.get_width() / 2,
            display.get_height() - planes_gui_container.get_height() - planes_gui_progressbar_container.get_height()))
        # upgrade button
        upgrade_button.draw(display)
        is_selected_plane_unlocked = user_stats.data["planes"][type(current_plane)][0]
        if not is_selected_plane_unlocked:
            buy_cost = int(100 + current_plane.rank * 50)
            upgrade_button.text = str(buy_cost)+" "*2
            display.blit(small_gem_icon, (upgrade_button.rect.centerx + 20, upgrade_button.rect.centery - small_gem_icon.get_height() / 2))
        else:
            upgrade_cost = int(250+current_plane.level*300+current_plane.rank*current_plane.level/2)
            upgrade_button.text = str(upgrade_cost)+" "*2
            display.blit(small_coin_icon, (upgrade_button.rect.centerx+20, upgrade_button.rect.centery-small_coin_icon.get_height()/2))

        # arrow back
        display.blit(planes_gui_arrow_back_frame,
                     (-40, display.get_height() - planes_gui_arrow_back_frame.get_height()))
        arrow_back_btn.draw(display)
        current_plane.update(0, plane_surf, [], (0, 0), is_dummy=True)
        plane_surf.blit(current_plane.image,
                        (0, 0))
        for vfx in plane_vfx:
            vfx.update(plane_surf)
            if vfx.ended:
                plane_vfx.remove(vfx)
        surf = pygame.transform.scale_by(plane_surf, plane_parking_scale)
        display.blit(surf, (display.get_width() / 2 - surf.get_width() / 2,
                            coins_label.get_height() - 32 + 120 - surf.get_height() / 2))
    elif current_gui == 3:
        display.blit(italy_map, map_pos)
        c = 0
        for level in levels:
            if level.reached() and c < len(levels) - 1:
                line_of_points(display, (12, 255, 47), level.get_center(map_pos), levels[c + 1].get_center(map_pos),
                               width=1, dash_length=2, blank_length=6)
            level.draw(display, map_pos)
            c += 1

        display.blit(planes_gui_arrow_back_frame,
                     (-40, display.get_height() - planes_gui_arrow_back_frame.get_height()))
        arrow_back_btn.draw(display)

    mouse_button_up_event = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_selected_plane_unlocked = user_stats.data["planes"][type(current_plane)][0]
            if not is_selected_plane_unlocked:
                current_plane = previous_plane
                user_stats.data["selected_plane"] = type(current_plane)
            quit_game()

        if current_gui == 0:
            if singleplayer_button.handle_event(event):
                current_gui = 3
                blit_main_gui = False
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
        elif current_gui == 2 or current_gui == 3:
            if arrow_back_btn.handle_event(event):
                if current_gui == 2:  # if the user presses the arrow back button and is in the plane selection gui we
                    # we check if it has unlocked the selected plane if not then we reset it to a plane it has unlocked

                    is_selected_plane_unlocked = user_stats.data["planes"][type(current_plane)][0]
                    if not is_selected_plane_unlocked:
                        current_plane = previous_plane
                        user_stats.data["selected_plane"] = type(current_plane)
                        plane_vfx = []
                current_gui = 0
                blit_main_gui = True
        if current_gui == 3:
            for level in levels:
                if level.handle_event(event, map_pos):
                    if user_stats.can_purchase("dogtags", 5):
                        user_stats.data["dogtags"] -= 5
                        level_won = play_level(level.get_level())
                        if level_won and user_stats.data["level_reached"] == int(level.level_number):
                            user_stats.data["level_reached"] += 1
                        current_gui = 0
                        blit_main_gui = True
                    elif not user_stats.can_purchase("dogtags", 5):
                        current_gui = 1
                        blit_main_gui = True

        elif current_gui == 2:
            if upgrade_button.handle_event(event):
                is_selected_plane_unlocked = user_stats.data["planes"][type(current_plane)][0]
                # TODO: add sfx and particles
                if not is_selected_plane_unlocked:
                    buy_cost = int(100 + current_plane.rank * 50)
                    if user_stats.can_purchase("gems", buy_cost):
                        user_stats.data["gems"] -= buy_cost
                        user_stats.data["planes"][type(current_plane)][0] = True
                else:
                    upgrade_cost = int(250+current_plane.level*300+current_plane.rank*current_plane.level/2)
                    if user_stats.can_purchase("coins", upgrade_cost):
                        user_stats.data["coins"] -= upgrade_cost  # TODO: add level and purchase
                        user_stats.data["planes"][type(current_plane)][1] += 1
                        current_plane.level += 1
                player.refresh_plane()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dogtags_plus_rect.collidepoint(mouse.get_pos()):
                    current_gui = 1
                mouse_button_up_event = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                if current_gui == 1:
                    current_gui = 0
                elif current_gui == 2:
                    current_gui = 0
                    blit_main_gui = True
                    is_selected_plane_unlocked = user_stats.data["planes"][type(current_plane)][0]
                    if not is_selected_plane_unlocked:
                        current_plane = previous_plane
                        user_stats.data["selected_plane"] = type(current_plane)
                        plane_vfx = []

    if current_gui == 0:
        blit_main_gui = True
    mouse.draw()
    shader.draw(display)  # , "time": shader_time
    clock.tick(120)
