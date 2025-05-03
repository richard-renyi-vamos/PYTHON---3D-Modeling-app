import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui
from imgui.integrations.pygame import PygameRenderer

vertices = [
    [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
    [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
]
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cube Viewer with GUI")

    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    imgui.create_context()
    impl = PygameRenderer()

    rotation_speed = 1.0
    show_cube = True

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                impl.shutdown()
                pygame.quit()
                quit()
            impl.process_event(event)

        imgui.new_frame()

        # GUI SETTINGS
        imgui.begin("Settings")
        changed, rotation_speed = imgui.slider_float("Rotation Speed", rotation_speed, 0.1, 5.0)
        _, show_cube = imgui.checkbox("Show Cube", show_cube)
        imgui.end()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            glRotatef(rotation_speed, 0, 1, 0)
        if keys[K_RIGHT]:
            glRotatef(-rotation_speed, 0, 1, 0)
        if keys[K_UP]:
            glRotatef(rotation_speed, 1, 0, 0)
        if keys[K_DOWN]:
            glRotatef(-rotation_speed, 1, 0, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if show_cube:
            draw_cube()

        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
