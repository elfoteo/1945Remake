display = None


def init(dis):
    global display
    display = dis.copy()


def get_nuclear_left(y, surrounding, inside, spacing_ext, spacing_int):
    pattern = []
    base_x = 35
    pattern.append(surrounding([base_x, y]))
    pattern.append(surrounding([base_x + 10 + spacing_ext.get_width(), y]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext.get_width() * 2, y]))
    pattern.append(surrounding([base_x, y + 10 + spacing_ext.get_height()]))
    pattern.append(inside(
        [base_x + 10 + spacing_ext.get_width() * 1.5 - spacing_int.get_width() / 2, y + 10 + spacing_ext.get_height()]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext.get_width() * 2, y + 10 + spacing_ext.get_height()]))
    return pattern


def get_nuclear_center(y, surrounding, inside, spacing_ext, spacing_int):
    pattern = []
    base_x = display.get_width() / 2 - 10 * 1.5 - spacing_ext.get_width() * 1.5
    pattern.append(surrounding([base_x, y]))
    pattern.append(surrounding([base_x + 10 + spacing_ext.get_width(), y]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext.get_width() * 2, y]))
    pattern.append(surrounding([base_x, y + 10 + spacing_ext.get_height()]))
    pattern.append(inside(
        [base_x + 10 + spacing_ext.get_width() * 1.5 - spacing_int.get_width() / 2, y + 10 + spacing_ext.get_height()]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext.get_width() * 2, y + 10 + spacing_ext.get_height()]))
    return pattern


def get_nuclear_right(y, surrounding, inside, spacing_ext, spacing_int):
    pattern = []
    base_x = display.get_width() - 10 * 3 - spacing_ext.get_width() * 3
    pattern.append(surrounding([base_x, y]))
    pattern.append(surrounding([base_x + 10 + spacing_ext.get_width(), y]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext.get_width() * 2, y]))
    pattern.append(surrounding([base_x, y + 10 + spacing_ext.get_height()]))
    pattern.append(inside(
        [base_x + 10 + spacing_ext.get_width() * 1.5 - spacing_int.get_width() / 2, y + 10 + spacing_ext.get_height()]))
    pattern.append(surrounding([base_x + 10 * 2 + spacing_ext.get_width() * 2, y + 10 + spacing_ext.get_height()]))
    return pattern
