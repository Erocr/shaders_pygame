from Shader import *
from Inputs import *

pg.init()
screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
inputs = Inputs()

shader = MultiShaders2D()
shader.add_shader(Shader2D(frag_shader="shaders/points_light.glsl"))
shader.add_shader(Shader2D(frag_shader="shaders/old_screen_effect.glsl"))


shader[0].add_uniform("luminosity", 0)
shader[0].add_uniform("luminosity_slope", 1)
shader[0].add_uniform("pointlights", [[0.5, 0.5, 0.8] for _ in range(20)])
shader[0].add_uniform("nbLights", 1)
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
