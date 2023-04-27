import random
from scripts.game import *
from scripts.button import Button
from scripts.label import Label

coin_icon = pygame.transform.scale_by(pygame.image.load("sprites/ui/coin.png"), 1)
gem_icon = pygame.transform.scale_by(pygame.image.load("sprites/ui/gem.png"), 1)
dogtag_icon = pygame.transform.scale_by(pygame.image.load("sprites/ui/dogtag.png"), 1)
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
singleplayer_button = Button(display.get_width() / 2 - (148 * 1.5) / 2, 700, 148 * 1.5, 37 * 1.5, 'sprites/ui/green_button.png',
                text="Single Player",
                font="font/font.ttf", increase_font_size=0.1)

dogtags_label = Label(user_stats.data["dogtags"], dogtag_icon, (0, 0), font, suffix="/100")
coins_label = Label(user_stats.data["coins"], coin_icon, (dogtags_label.get_width(), 0), font)
gems_label = Label(user_stats.data["gems"], gem_icon, (coins_label.get_width() + dogtags_label.get_width(), 0), font)

level1 = Level(enemies, 1, 1)

dogtags_plus_rect = pygame.Rect(93 * 1.25, 3 * 1.25, 22 * 1.25, 21 * 1.25)
dogtags_plus = False
dogtags_timer_font = pygame.font.Font("font/font.ttf", 24)
dogtags_transparent_bg = transparent_rect((screen.get_width()/1.5, screen.get_height()/2), 0.5)
dogtags_transparent_bg_blitpos = (screen.get_width()/2-dogtags_transparent_bg.get_width()/2, screen.get_height()/2-dogtags_transparent_bg.get_height()/2)
dogtags_transparent_bg_rect = pygame.Rect(dogtags_transparent_bg_blitpos[0], dogtags_transparent_bg_blitpos[1], dogtags_transparent_bg.get_width(), dogtags_transparent_bg.get_height())
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
        
        display.blit(dogtags_transparent_bg, dogtags_transparent_bg_blitpos, special_flags=pygame.BLEND_RGBA_MULT)
        surf = dogtags_timer_font.render("Time until next tag: ", False, (255, 255, 255)) 
        display.blit(surf, (screen.get_width()/2-surf.get_width()/2, 250))
        surf = dogtags_timer_font.render(user_stats.get_next_dogtag_time(), False, (255, 255, 255))
        display.blit(surf, (screen.get_width()/2-surf.get_width()/2, 300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if not dogtags_plus and singleplayer_button.handle_event(event) and\
            user_stats.can_purchase("dogtags", 5):
            user_stats.data["dogtags"] -= 5
            play_level(level1)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dogtags_plus and not dogtags_transparent_bg_rect.collidepoint(mouse.get_pos()):
                    dogtags_plus = False
                if dogtags_plus_rect.collidepoint(mouse.get_pos()):
                    dogtags_plus = True

    shader.draw(program_args={"tex": 0})  # , "time": shader_time
    clock.tick(120)
