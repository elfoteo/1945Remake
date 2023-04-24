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
        enemies.append(RotatingEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 1:
        enemies.append(RotatingEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 2:
        enemies.append(RotatingEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 3:
        enemies.append(RotatingEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))
    elif a == 5:
        enemies.append(RotatingEnemy([
            random.randint(enemy_normal_img.get_width(), display.get_width() - enemy_normal_img.get_width()), cy]))

mouse.unlock()
button = Button(display.get_width() / 2 - (148 * 1.5) / 2, 700, 148 * 1.5, 37 * 1.5, 'sprites/ui/green_button.png',
                text="Single Player",
                font="font/font.ttf", increase_font_size=0.1)

dogtags_label = Label(user_stats.data["dogtags"], dogtag_icon, (0, 0), font, suffix="/100")
coins_label = Label(user_stats.data["coins"], coin_icon, (dogtags_label.get_width(), 0), font)
gems_label = Label(user_stats.data["gems"], gem_icon, (coins_label.get_width() + dogtags_label.get_width(), 0), font)

while True:
    shader_time += 1
    display.blit(ui_background, (0, 0))
    coins_label.draw(display)
    coins_label.update(user_stats.data["coins"])
    gems_label.draw(display)
    gems_label.update(user_stats.data["gems"])
    dogtags_label.draw(display)
    dogtags_label.update(user_stats.data["dogtags"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if button.handle_event(event):
            game(enemies)

    button.draw(display)

    shader.draw(program_args={"tex": 0})  # , "time": shader_time
    clock.tick(120)
