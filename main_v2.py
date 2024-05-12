import pygame
import math
from eye import Eye

def main():
    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Eyes")

    bg_color = (254,68,36)

    rows, cols = 12, 10
    margin = 0
    grid_width = width - 2 * margin
    grid_height = height - 2 * margin
    spacing_x = grid_width // cols
    spacing_y = grid_height // rows

    # spacing_x = 60
    # spacing_y = 50
    print(spacing_x, spacing_y)

    start_x = (width - (cols - 1) * spacing_x) // 2
    start_y = (height - (rows - 1) * spacing_y) // 2

    eyes = []
    sclera_radius = 20
    pupil_radius = 12
    for y in range(rows):
        for x in range(cols):
            center_x = start_x + x * spacing_x
            center_y = start_y + y * spacing_y
            eyes.append(Eye(center_x, center_y, sclera_radius, pupil_radius, mask_color=bg_color))
    
    last_mouse_x, last_mouse_y = None, None
    running = True
    ellipse = 1   # or 2
    center_ppl = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(bg_color)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            if last_mouse_x is None or last_mouse_y is None:
                last_mouse_x, last_mouse_y = mouse_x, mouse_y
            dx, dy = mouse_x - last_mouse_x, mouse_y - last_mouse_y
            if abs(dx) > 1 or abs(dy) > 1:
                for eye in eyes:
                    eye.reset_mouse_timer()            
            last_mouse_x, last_mouse_y = mouse_x, mouse_y


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                ellipse=2
                center_ppl = True
            
        # Check for key release events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                ellipse=1
                center_ppl = False

        for eye in eyes:
            eye.ellipse = ellipse
            eye.update(mouse_x, mouse_y,force_center=center_ppl)
            eye.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
