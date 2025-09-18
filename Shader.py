import sys
from array import array

import moderngl
import pygame as pg

# TODO: une doc
# Doc: image retournée verticalement dans le shader

_default_fragment_shader = """
#version 330 core
uniform sampler2D image;

in vec2 fragmentTexCoord;
out vec4 color;

void main() {
    color = texture(image, fragmentTexCoord);
}
"""

_default_vertex_shader = """
#version 330 core

in vec2 vert;
in vec2 texCoord;
out vec2 fragmentTexCoord;

void main() {
    fragmentTexCoord = texCoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
"""


def init_shaders():
    Shader.ctx = moderngl.create_context()
    Shader.quad_buffer = Shader.ctx.buffer(data=array('f', [
        # position (x, y), uv coords (x, y)
        -1.0, 1.0, 0.0, 0.0,  # topleft
        1.0, 1.0, 1.0, 0.0,  # topright
        -1.0, -1.0, 0.0, 1.0,  # bottomleft
        1.0, -1.0, 1.0, 1.0,  # bottomright
    ]))
    Shader.quad_buffer_invert_y = Shader.ctx.buffer(data=array('f', [
        # position (x, y), uv coords (x, y)
        -1.0, 1.0, 0.0, 1.0,  # topleft
        1.0, 1.0, 1.0, 1.0,  # topright
        -1.0, -1.0, 0.0, 0.0,  # bottomleft
        1.0, -1.0, 1.0, 0.0,  # bottomright
    ]))


class Shader:
    ctx: moderngl.Context = None
    quad_buffer: moderngl.Buffer = None
    quad_buffer_invert_y: moderngl.Buffer = None
    texture_index_max = 0

    def add_uniform(self, param, param1):
        pass

    def render(self, invert_y=False):
        pass


class Shader2D(Shader):
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

        self.program = self.ctx.program(vertex_shader=vertex_shader_source, fragment_shader=frag_shader_source)
        self.renderer = self.ctx.vertex_array(self.program, [(self.quad_buffer, "2f 2f", "vert",
                                                              "texCoord")])
        self.renderer_invert_y = self.ctx.vertex_array(self.program, [(self.quad_buffer_invert_y, "2f 2f", "vert",
                                                              "texCoord")])

        self.texture_indices = {}
        self.used_textures = {}

    def _surf_to_texture(self, surf: pg.Surface):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = "BGRA"
        tex.write(surf.get_view('1'))
        return tex

    def add_uniform(self, name, value):
        if isinstance(value, pg.Surface):
            texture = self._surf_to_texture(value)
            if name not in self.texture_indices:
                self.texture_indices[name] = self.texture_index_max
                self.texture_index_max += 1
            if name in self.used_textures:
                self.used_textures[name].release()
            texture.use(self.texture_indices[name])
            self.program[name] = self.texture_indices[name]
            self.used_textures[name] = texture
        elif isinstance(value, moderngl.Texture):
            texture = value
            if name not in self.texture_indices:
                self.texture_indices[name] = self.texture_index_max
                Shader.texture_index_max += 1
            if name in self.used_textures:
                self.used_textures[name].release()
            texture.use(self.texture_indices[name])
            self.program[name] = self.texture_indices[name]
            self.used_textures[name] = texture
            # TODO: beautify
        else:
            self.program[name] = value

    def render(self, invert_y=False):
        if invert_y:
            self.renderer_invert_y.render(mode=moderngl.TRIANGLE_STRIP)
        else:
            self.renderer.render(mode=moderngl.TRIANGLE_STRIP)
        # TODO: DOC textures destroyed after sent in the GPU


class MultiShaders2D(Shader):
    def __init__(self):
        self.shaders: list[Shader] = []
        self.frame_buffers: list[moderngl.Framebuffer] = []

    def add_shader(self, shader):
        self.shaders.append(shader)
        if len(self.shaders) > 1:
            self.frame_buffers.append(self.ctx.framebuffer(color_attachments=[self.ctx.texture((800, 600), 4)]))
            self.shaders[-1].add_uniform("image", self.frame_buffers[-1].color_attachments[0])
            # TODO: check for the good size

    def __getitem__(self, item):
        return self.shaders[item]

    def render(self, invert_y=False):
        for i in range(len(self.shaders)):
            if i < len(self.shaders) - 1:
                self.frame_buffers[i].use()
            else:
                self.ctx.screen.use()
            self.shaders[i].render(i<len(self.shaders)-1)

    def add_uniform(self, name, value):
        self.shaders[0].add_uniform(name, value)

    def __setitem__(self, key, value):
        assert isinstance(value, Shader)
        self.shaders[key] = value


# TODO: Compute shaders
