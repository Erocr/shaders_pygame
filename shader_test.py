from Shader import *
from Inputs import *
from math import cos

pg.init()
screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
inputs = Inputs()

shader = MultiShaders2D()
shader.add_shader(Shader2D(frag_shader="ecran_chelou.glsl"))
shader.add_shader(Shader2D(frag_shader="uniform_light.glsl"))
shader.add_shader(Shader2D())


shader[1].add_uniform("luminosity", 0.5)
time = 0

while not inputs.quit:
    time += 1
    inputs.update()
    screen.fill((255, 0, 150))
    pg.draw.rect(screen, (0, 0, 0), pg.Rect(10, 10, 200, 200))

    shader.add_uniform("image", screen)

    shader.render()
    pg.display.flip()

pg.quit()
