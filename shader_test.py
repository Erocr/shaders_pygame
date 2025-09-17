from Shader import *
from Inputs import *

pg.init()
screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
display = pg.Surface((800, 600))
inputs = Inputs()

shader = Shader2D()

while not inputs.quit:
    inputs.update()
    display.fill((255, 0, 0))

    shader.add_uniform("image", display)

    shader.render()

    pg.display.flip()

pg.quit()
