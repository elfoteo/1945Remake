import pickle
import random

import pygame

display: pygame.Surface = None


def init(dis):
    global display
    display = dis.copy()


def get_nuclear_left(y, surrounding, inside, spacing_ext, spacing_int):
    pattern = []
    base_x = 35
    pattern.append(surrounding([base_x, y]))
    pattern.append(surrounding([base_x + 10 + spacing_ext[0], y]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext[0] * 2, y]))
    pattern.append(surrounding([base_x, y + 10 + spacing_ext[1]]))
    pattern.append(inside(
        [base_x + 10 + spacing_ext[0] * 1.5 - spacing_int[0] / 2, y + 10 + spacing_ext[1]]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext[0] * 2, y + 10 + spacing_ext[1]]))
    return pattern


def get_nuclear_center(y, surrounding, inside, spacing_ext, spacing_int):
    pattern = []
    base_x = display.get_width() / 2 - 10 * 1.5 - spacing_ext[0] * 1.5
    pattern.append(surrounding([base_x, y]))
    pattern.append(surrounding([base_x + 10 + spacing_ext[0], y]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext[0] * 2, y]))
    pattern.append(surrounding([base_x, y + 10 + spacing_ext[1]]))
    pattern.append(inside(
        [base_x + 10 + spacing_ext[0] * 1.5 - spacing_int[0] / 2, y + 10 + spacing_ext[1]]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext[0] * 2, y + 10 + spacing_ext[1]]))
    return pattern


def get_nuclear_right(y, surrounding, inside, spacing_ext, spacing_int):
    pattern = []
    base_x = display.get_width() - 10 * 3 - spacing_ext[0] * 3
    pattern.append(surrounding([base_x, y]))
    pattern.append(surrounding([base_x + 10 + spacing_ext[0], y]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext[0] * 2, y]))
    pattern.append(surrounding([base_x, y + 10 + spacing_ext[1]]))
    pattern.append(inside(
        [base_x + 10 + spacing_ext[0] * 1.5 - spacing_int[0] / 2, y + 10 + spacing_ext[1]]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext[0] * 2, y + 10 + spacing_ext[1]]))
    return pattern


def get_line_right(y, enemy, size, count, sep_y):
    pattern = []
    base_x = display.get_width() - size[0]*1.5
    for i in range(count):
        pattern.append(enemy([base_x, y-size[1]*i-i*sep_y]))
    return pattern


def get_line_left(y, enemy, size, count, sep_y):
    pattern = []
    base_x = size[0]/2
    for i in range(count):
        pattern.append(enemy([base_x, y-size[1]*i-i*sep_y]))
    return pattern


def get_line_center(y, enemy, size, count, sep_y):
    pattern = []
    base_x = display.get_width()/2-size[0]/2
    for i in range(count):
        pattern.append(enemy([base_x, y-size[1]*i-i*sep_y]))
    return pattern


def get_random(y, enemy, size, count, sep_y):
    pattern = []
    min_x = size[0]/2
    max_x = display.get_width()-size[0]*1.5
    for i in range(count):
        pattern.append(enemy([random.randint(min_x, max_x), y-size[1]*i-i*sep_y]))
    return pattern


def get_2x2_right(y, enemy, size):
    pattern = []
    base_x = display.get_width() - size[0] * 2 - 15
    pattern.append(enemy([base_x, y]))
    pattern.append(enemy([base_x, y+10+size[1]]))
    pattern.append(enemy([base_x+size[0]+10, y]))
    pattern.append(enemy([base_x+size[0]+10, y+10+size[1]]))
    return pattern


def get_2x2_left(y, enemy, size):
    pattern = []
    base_x = 5
    pattern.append(enemy([base_x, y]))
    pattern.append(enemy([base_x, y+10+size[1]]))
    pattern.append(enemy([base_x+size[0]+10, y]))
    pattern.append(enemy([base_x+size[0]+10, y+10+size[1]]))
    return pattern


def get_2x2_center(y, enemy, size):
    pattern = []
    base_x = display.get_width()/2-size[0]-5
    pattern.append(enemy([base_x, y]))
    pattern.append(enemy([base_x, y+10+size[1]]))
    pattern.append(enemy([base_x+size[0]+10, y]))
    pattern.append(enemy([base_x+size[0]+10, y+10+size[1]]))
    return pattern


def save(patterns, level_name="level1"):
    print(patterns)
    pickle.dump(patterns, open("levels/"+level_name+".lvl", "wb"))


def load(level_name):
    patterns = pickle.load(open("levels/"+level_name+".lvl", "rb"))
    enemies = []
    print(patterns)
    for pattern in patterns:
        print(pattern)
        enemies.extend(pattern[0](*pattern[1]))
    return enemies
