import pygame
import math




min_length = 0
max_length = 20

def draw_arrow(surface, start, end, length, color=(255, 255, 255)):
    """ Draw an arrow from start to end coordinates on the given surface. """
    pygame.draw.line(surface, color, start, end, 2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0])) + 90
    
    # if not length<=min_length :
    #     pygame.draw.polygon(surface, color, (
    #         (end[0] + 5 * math.sin(math.radians(rotation      )), end[1] + 5 * math.cos(math.radians(rotation))),
    #         (end[0] + 5 * math.sin(math.radians(rotation - 120)), end[1] + 5 * math.cos(math.radians(rotation - 120))),
    #         (end[0] + 5 * math.sin(math.radians(rotation + 120)), end[1] + 5 * math.cos(math.radians(rotation + 120)))
    #     ))

def calculate_length(distance, min_length, max_length):
    """ Adjust the arrow length based on the distance from the cursor, reversing the dynamics.
        Arrows are shortest when the cursor is within 10 pixels and longest when far away. """
    if distance <= 10:
        return min_length
    else:
        # Increase the length linearly based on the distance, scaling down the distance effect
        scaled_length = min_length + (distance / 50) * (max_length - min_length)
        return min(max_length, max(min_length, scaled_length))


def main():
    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dynamic Arrow Lengths Based on Distance")

    # Grid settings
    rows, cols = 50, 50
    margin = 0
    grid_width = width - 2 * margin
    grid_height = height - 2 * margin
    spacing_x = 20 + grid_width // cols
    spacing_y = 20 + grid_height // rows

    # Calculate the starting offset to center the grid
    start_x = (width - (cols - 1) * spacing_x) // 2
    start_y = (height - (rows - 1) * spacing_y) // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear the screen

        # Get current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Update and draw arrows with dynamic lengths
        for y in range(rows):
            for x in range(cols):
                start_pos = (start_x + x * spacing_x, start_y + y * spacing_y)
                distance = math.hypot(mouse_x - start_pos[0], mouse_y - start_pos[1])
                length = calculate_length(distance, min_length, max_length)  # Calculate dynamic length
                angle = math.atan2(mouse_y - start_pos[1], mouse_x - start_pos[0])
                end_pos = (start_pos[0] + length * math.cos(angle), start_pos[1] + length * math.sin(angle))
                draw_arrow(screen, start_pos, end_pos, length)

        pygame.display.flip()  # Update the full display Surface to the screen

    pygame.quit()

if __name__ == "__main__":
    main()
