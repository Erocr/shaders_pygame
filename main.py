# Importation des bibliothèques
import moderngl
import pygame as pg
import pygame_shaders
from Inputs import *

# initialisation des bibliothèques
size = Vec(600, 600)
screen = pg.display.set_mode(size.get(), pg.OPENGL | pg.DOUBLEBUF)
inputs = Inputs()


# compilation des shaders
shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, "shaders/points_light_normal_map.glsl", screen)
shader.send("luminosity", 0.4)

shader.send("luminosity_slope", 2)


def pygame2frag(pos):
    pos = pos / size
    pos = Vec(pos.x, -pos.y + 1)
    return pos


def send_surf(name, surf, shader: pygame_shaders.Shader):
    tex = shader.ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = "BGRA"
    tex.write(pg.transform.flip(surf, False, True).get_view("1"))
    tex.use(1)
    shader.shader[name] = 1


def send_lights(lights_list, shader):
    assert len(lights_list) < 20
    shader.send("nbLights", len(lights_list))
    shader.send("pointlights", lights_list + [[0, 0, 0]] * (20 - len(lights_list)))


normal_map = pg.Surface((600, 600))

im = pg.image.load("assets/stand_with_sword.png")
normal = pg.image.load("assets/normal_map.png")
im = pg.transform.scale2x(im)
normal = pg.transform.scale2x(normal)

while not inputs.quit:
    inputs.update()

    # On affiche ce qu'on a à afficher
    screen.fill((40, 60, 100))
    normal_map.fill((127, 127, 255))
    screen.blit(im, (200, 200))
    normal_map.blit(normal, (200, 200))

    mouse_pos_shader = pygame2frag(inputs.mouse_pos)
    send_lights([[mouse_pos_shader.x, mouse_pos_shader.y, 1], [0, 0, 0.5], [0, 1, 0.5], [1, 0, 0.5], [1, 1, 0.5]], shader)
    send_surf("normal_map", normal_map, shader)
    # On applique le shader
    shader.render_direct(pg.Rect(0, 0, 600, 600))

    # On affiche à l'écran
    pg.display.flip()

pg.quit()
