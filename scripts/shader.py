import random
from array import array
import time

import moderngl
import pygame


class ShaderDisplay(pygame.Surface):
    def __init__(self, size):
        super().__init__(size)


class Shader:
    def __init__(self):
        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,  # topright
            -1.0, -1.0, 0.0, 1.0,  # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))
        print("Loading shaders...")
        with open("shaders/vertex.vert") as shader_file:
            self.vert_shader = shader_file.read()
        with open("shaders/frag.frag") as shader_file:
            self.frag_shader = shader_file.read()
        print("Shaders loaded")
        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
        self.shake_amount = 0
        self.red_overlay = 0
        self.ticks = 0
        self.ingame_ticks = 0
        self.ingame = False
        self.ingame_dt = 0
        self.current_time = time.time()
        self.last_time = time.time()

    def get_ctx(self):
        return self.ctx

    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

    def get_time(self):
        # 120 because we have 120 frames in 1 second
        # and * 1000 because we want the result in milliseconds
        return self.ticks/120*1000

    def get_ingame_time(self):
        # 120 because we have 120 frames in 1 second
        # and * 1000 because we want the result in milliseconds
        return self.ingame_ticks/120*1000

    def get_dt(self):
        return self.ingame_dt

    def draw(self, display, program_args=None):
        if program_args is None:
            program_args = {}
        pygame.draw.rect(display, (0, 0, 0), (-20, -20, display.get_width() + 40, display.get_height() + 40), 20)
        frame_tex = self.surf_to_texture(display)
        frame_tex.use(0)
        self.program["tex"] = 0
        self.program["shake_x"] = random.uniform(-self.shake_amount, self.shake_amount)
        self.program["shake_y"] = random.uniform(-self.shake_amount, self.shake_amount)
        self.program["red_overlay"] = self.red_overlay
        for arg in program_args:
            self.program[arg] = program_args[arg]
        # self.program["time"] = time.time()*1000
        self.shake_amount = round(self.shake_amount / 1.04, 2)
        self.red_overlay = round(self.red_overlay / 1.03, 2)
        self.red_overlay -= 0.002
        if self.shake_amount <= 0.5:
            self.shake_amount = 0
        if self.red_overlay <= 0.1:
            self.red_overlay = 0

        self.last_time = self.current_time
        self.current_time = time.time()
        self.ingame_dt = (self.current_time-self.last_time)*120
        self.ticks += 1*self.get_dt()
        if self.ingame:
            self.ingame_ticks += 1*self.get_dt()
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        pygame.display.flip()
        frame_tex.release()
