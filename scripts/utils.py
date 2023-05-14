import math
import os
import sys
import pygame


def angle_to_motion(angle_degrees, magnitude):
    # Convert angle from degrees to radians
    angle_radians = math.radians(angle_degrees)

    # Calculate X and Y components of motion vector
    motion_x = magnitude * math.cos(angle_radians)
    motion_y = magnitude * math.sin(angle_radians)

    return motion_x, motion_y


def distance_between_points(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance


def angle_between_points(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1
    angle = math.atan2(dy, dx)
    return math.degrees(angle)


def load_animation_frames(directory, scale=None):
    frames = []
    filenames = sorted(os.listdir(directory),
                       key=lambda x: int(os.path.splitext(x)[0]) if x[0].isdigit() else float('inf'))
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        if filename.split(".")[0].isdigit():
            print("Loaded", filepath)
            frame = pygame.image.load(filepath)
            if scale is not None:
                frame = pygame.transform.scale_by(frame, scale)
            frames.append(frame)
    return frames


def load_image(file, scale=None, no_scale_by=False, alpha=True):
    if scale is None:
        if no_scale_by:
            scale = None
        else:
            scale = 1
    print("Loaded", file)
    if no_scale_by:
        if alpha:
            return pygame.transform.scale(pygame.image.load(file), scale).convert_alpha()
        return pygame.transform.scale(pygame.image.load(file), scale).convert()
    if alpha:
        return pygame.transform.scale_by(pygame.image.load(file), scale).convert_alpha()
    return pygame.transform.scale_by(pygame.image.load(file), scale).convert()


def transparent_rect(size, intensity):
    """Returns a transparent texture with custom size and intensity"""
    w, h = size
    transparent_texture = pygame.Surface((w, h), pygame.SRCALPHA)
    transparent_color = (intensity * 255, intensity * 255, intensity * 255, 255)
    transparent_texture.fill(transparent_color)
    return transparent_texture


def _quit():
    pygame.quit()
    sys.exit()


############################################################################################
###  Code from:                                                                          ###
###  https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame  ###
############################################################################################
_circle_cache = {}


def _circle_points(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def outlined_text(text, font, fore_color=(255, 255, 255), outline_color=(50, 50, 50), outline_width=1):
    text_surf = font.render(text, True, fore_color).convert_alpha()
    w = text_surf.get_width() + 2 * outline_width
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * outline_width)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, outline_color).convert_alpha(), (0, 0))

    for dx, dy in _circle_points(outline_width):
        surf.blit(osurf, (dx + outline_width, dy + outline_width))

    surf.blit(text_surf, (outline_width, outline_width))
    return surf


# End

############################################################################################
###  Code from:                                                                          ###
###  https://stackoverflow.com/questions/15098900/how-to-set-the-pivot-point-center-of\  ###
###  -rotation-for-pygame-transform-rotate                                               ###
############################################################################################


def pivot_rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot + rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


# End

############################################################################################
###  Code from:                                                                          ###
###  https://stackoverflow.com/questions/8906926/formatting-timedelta-objects            ###
###  (modified)                                                                          ###
############################################################################################


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    if d["minutes"] == 0:
        d["minutes"] = "00"
    if len(str(d["minutes"])) == 1:
        d["minutes"] = "0" + str(d["minutes"])
    if d["seconds"] == 0:
        d["seconds"] = "00"
    if len(str(d["seconds"])) == 1:
        d["seconds"] = "0" + str(d["seconds"])
    return fmt.format(**d)

# End
