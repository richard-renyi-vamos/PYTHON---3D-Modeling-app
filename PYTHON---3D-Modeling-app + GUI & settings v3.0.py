import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui
from imgui.integrations.pygame import PygameRenderer

# Cube geometry
vertices = [
    [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
    [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
]
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Draw cube
def draw_cube(color=(1, 1, 1), wireframe=True):
    glColor3f(*color)
    glBegin(GL_LINES if wireframe else GL_QUADS)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Reset view
def reset_view():
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

# Rotation handler
def handle_rotation_keys(rotation_speed):
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        glRotatef(rotation_speed, 0, 1, 0)
    if keys[K_RIGHT]:
        glRotatef(-rotation_speed, 0, 1, 0)
    if keys[K_UP]:
        glRotatef(rotation_speed, 1, 0, 0)
    if keys[K_DOWN]:
        glRotatef(-rotation_speed, 1, 0, 0)

# Zoom handler
def zoom_control(z_translate):
    glTranslatef(0, 0, z_translate)

# Main loop
def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("🔷 Cube Viewer with GUI 🔶")

    reset_view()

    imgui.create_context()
    impl = PygameRenderer()

    rotation_speed = 1.0
    z_translate = 0.0
    show_cube = True
    wireframe_mode = True
    cube_color = [1.0, 1.0, 1.0]

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                impl.shutdown()
                pygame.quit()
                quit()
            impl.process_event(event)

        imgui.new_frame()

        # GUI Panel
        imgui.begin("Settings")
        _, show_cube = imgui.checkbox("Show Cube", show_cube)
        _, wireframe_mode = imgui.checkbox("Wireframe Mode", wireframe_mode)
        changed, rotation_speed = imgui.slider_float("Rotation Speed", rotation_speed, 0.1, 5.0)
        changed, z_translate = imgui.slider_float("Zoom", z_translate, -10.0, 5.0)
        _, cube_color = imgui.color_edit3("Cube Color", *cube_color)
        if imgui.button("Reset View"):
            reset_view()
        imgui.end()

        handle_rotation_keys(rotation_speed)
        zoom_control(z_translate)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if show_cube:
            draw_cube(color=cube_color, wireframe=wireframe_mode)

        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
