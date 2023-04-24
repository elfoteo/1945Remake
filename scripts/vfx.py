import time


class VFX:
    def __init__(self, frames, x, y, delay=40, anchor=None, offset=(0, 0)):
        self.frames = frames
        self.ended = False
        self.index = 0
        self.delay = delay
        self.last_frame = time.time() * 1000
        self.x = x
        self.y = y
        self.anchor = anchor
        self.offset = offset

    def reset(self):
        self.ended = False
        self.index = 0

    def update(self, screen):
        if self.ended:
            return
        if self.last_frame + self.delay < time.time() * 1000:
            self.last_frame = time.time() * 1000
            self.index += 1
        if self.index >= len(self.frames) - 1:
            self.ended = True
            return

        img = self.frames[self.index]
        if self.anchor is not None:
            screen.blit(img, (self.anchor[0]() + self.offset[0] - img.get_width() / 2, self.anchor[1]() + self.offset[1] - img.get_width() / 2))
        else:
            screen.blit(img, (self.x - img.get_width() / 2, self.y - img.get_width() / 2))
