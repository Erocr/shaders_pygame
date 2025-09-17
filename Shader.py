import sys
from array import array

import moderngl
import pygame as pg


_default_fragment_shader = """
#version 330 core
uniform sampler2D image;

in vec2 coord;
out vec4 color;

void main() {
    color = texture(image, coord);
}
"""

_default_vertex_shader = """
#version 330 core

in vec2 vert;
in vec2 texCoord;
out vec2 coord;

void main() {
    coord = texCoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
"""


def init_shaders():
    Shader2D.ctx = moderngl.create_context()


class Shader2D:
    ctx = None

    def __init__(self, vertex_shader=None, frag_shader=None):
        if self.ctx is None:
            init_shaders()

        if vertex_shader is None:
            vertex_shader_source = _default_vertex_shader
        else:
            with open(vertex_shader, "r") as file:
                vertex_shader_source = file.read()
        if frag_shader is None:
            frag_shader_source = _default_fragment_shader
        else:
            with open(frag_shader, "r") as file:
                frag_shader_source = file.read()

        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,  # topright
            -1.0, -1.0, 0.0, 1.0,  # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))  # TODO: change where it is applied

        self.program = self.ctx.program(vertex_shader=vertex_shader_source, fragment_shader=frag_shader_source)
        self.renderer = self.ctx.vertex_array(self.program, [(self.quad_buffer, "2f 2f", "vert",
                                                                 "texCoord")])

        self.texture_indices = {}
        self.used_textures = []
        self.texture_index_max = 0

    def _surf_to_texture(self, surf: pg.Surface):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

    def add_uniform(self, name, value):
        if isinstance(value, pg.Surface):
            texture = self._surf_to_texture(value)
            if name not in self.texture_indices:
                self.texture_indices[name] = self.texture_index_max
                self.texture_index_max += 1
            texture.use(self.texture_indices[name])
            self.program[name] = self.texture_indices[name]
            self.used_textures.append(texture)
        # TODO: other uniform types

    def render(self):
        self.renderer.render(mode=moderngl.TRIANGLE_STRIP)
        for texture in self.used_textures:
            texture.release()
        self.used_textures = []

