from Shader import *
from Inputs import *

pg.init()
screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
inputs = Inputs()

shader = MultiShaders2D()
shader.add_shader(Shader2D(frag_shader="old_screen_effect.glsl"))
shader.add_shader(Shader2D(frag_shader="uniform_light.glsl"))


shader[1].add_uniform("luminosity", 0.5)
time = 0

while not inputs.quit:
    time += 1
    inputs.update()
    screen.fill((255, 0, 150))
    pg.draw.rect(screen, (0, 0, 0), pg.Rect(10, 10, 200, 200))

    if inputs.isResized:
        shader.change_screen_size(inputs.new_screen_size)
    shader.add_uniform("image", screen)

    shader.render()
    pg.display.flip()

pg.quit()
