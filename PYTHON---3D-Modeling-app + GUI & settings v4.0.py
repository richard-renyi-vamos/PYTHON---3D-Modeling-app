import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui
from imgui.integrations.pygame import PygameRenderer

# Cube geometry (Updated for proper Quad face rendering)
vertices = [
    [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
    [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Define faces for solid rendering (each tuple is a face of the cube)
faces = [
    (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
    (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
]

def draw_cube(color=(1, 1, 1), wireframe=True, scale=1.0):
    glPushMatrix()          # Save coordinate system
    glScalef(scale, scale, scale) # Apply scaling factor
    glColor3f(*color)
    
    if wireframe:
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
    else:
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()
    glPopMatrix()           # Restore coordinate system

def reset_view():
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

def handle_rotation_keys(rotation_speed):
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]: glRotatef(rotation_speed, 0, 1, 0)
    if keys[K_RIGHT]: glRotatef(-rotation_speed, 0, 1, 0)
    if keys[K_UP]: glRotatef(rotation_speed, 1, 0, 0)
    if keys[K_DOWN]: glRotatef(-rotation_speed, 1, 0, 0)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("🚀 Pro Cube Modeler")

    imgui.create_context()
    impl = PygameRenderer()
    reset_view()

    # --- App State Variables ---
    rotation_speed = 1.0
    cube_scale = 1.0         # New: Controls size
    auto_rotate = False      # New: Toggle for automatic spinning
    bg_color = [0.1, 0.1, 0.1] # New: Background color
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

        # --- Enhanced GUI Panel ---
        imgui.begin("Control Panel")
        
        imgui.text("Visibility & Style")
        _, show_cube = imgui.checkbox("Show Cube", show_cube)
        _, wireframe_mode = imgui.checkbox("Wireframe Mode", wireframe_mode)
        _, cube_color = imgui.color_edit3("Cube Color", *cube_color)
        _, bg_color = imgui.color_edit3("Background", *bg_color)
        
        imgui.separator()
        imgui.text("Transformation")
        _, cube_scale = imgui.slider_float("Scale", cube_scale, 0.1, 3.0)
        _, rotation_speed = imgui.slider_float("Manual Speed", rotation_speed, 0.1, 5.0)
        
        # Auto-rotation feature
        _, auto_rotate = imgui.checkbox("Auto-Rotate Orbit", auto_rotate)
        
        if imgui.button("Reset Camera"):
            reset_view()
            
        imgui.end()

        # Handle transformations
        handle_rotation_keys(rotation_speed)
        if auto_rotate:
            glRotatef(0.5, 1, 1, 0) # Smoothly rotate on multiple axes

        # Set background color and clear buffers
        glClearColor(bg_color[0], bg_color[1], bg_color[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST) # Ensure 3D depth is rendered correctly

        if show_cube:
            draw_cube(color=cube_color, wireframe=wireframe_mode, scale=cube_scale)

        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
