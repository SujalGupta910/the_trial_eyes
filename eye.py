import pygame
import sys
import math
import time

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
grey = (0,0,0)
light_blue = (4, 161, 223)
random_color = (205,161,95)


class Eye:
    def __init__(self, x, y, sclera_radius, pupil_radius, mask_color=grey):
        self.x = x
        self.y = y
        self.sclera_radius = sclera_radius
        self.pupil_radius = pupil_radius
        self.mask_color = mask_color
        self.last_mouse_move = time.time()  # Time of the last mouse movement
        self.mask1 = self.create_mask()
        self.mask2 = self.create_mask2()

    def update(self, mouse_x, mouse_y, force_center=False):
        # Check if 10 seconds have passed
        time_diff = time.time() - self.last_mouse_move
        if time_diff >= 5 or force_center:
            # Interpolate the pupil's position towards the center smoothly
            # Calculate the vector from the current position to the center
            dx, dy = self.x - self.pupil_x, self.y - self.pupil_y
            speed = 0.1  # Control the speed of the movement, smaller values for slower movement
            self.pupil_x += dx * speed
            self.pupil_y += dy * speed

            # Ensure the pupil stops moving once it is close enough to the center
            if math.hypot(dx, dy) < 1:
                self.pupil_x, self.pupil_y = self.x, self.y
        else:
            dx, dy = mouse_x - self.x, mouse_y - self.y
            angle = math.atan2(dy, dx)
            
            distance = min(self.sclera_radius - self.pupil_radius, math.hypot(dx, dy))
            self.pupil_x = self.x + distance * math.cos(angle)
            self.pupil_y = self.y + distance * math.sin(angle)

    def draw(self, surface):
        pygame.draw.circle(surface, white, (self.x, self.y), self.sclera_radius)  # Sclera
        pygame.draw.circle(surface, light_blue, (int(self.pupil_x), int(self.pupil_y)), self.pupil_radius)  # Outer Blue Pupil
        pygame.draw.circle(surface, black, (int(self.pupil_x), int(self.pupil_y)), int(0.8*self.pupil_radius))  # Inner Black Pupil

        mask = self.mask1 if self.ellipse==1 else self.mask2
        surface.blit(mask, (self.x - self.sclera_radius, self.y - self.sclera_radius))

    def reset_mouse_timer(self):
        # Reset the last_mouse_move time to current time
        self.last_mouse_move = time.time()

    def create_mask(self):
        self.ellipse_height_ratio = 0.55
        mask_size = self.sclera_radius * 2
        mask_surface = pygame.Surface((mask_size, mask_size), pygame.SRCALPHA)

        pygame.draw.rect(mask_surface, self.mask_color, [0, 0, mask_size, mask_size])

        ellipse_width = mask_size
        ellipse_height = mask_size * self.ellipse_height_ratio

        ellipse_rect = [
            (mask_size - ellipse_width) // 2,
            (mask_size - ellipse_height) // 2,
            ellipse_width,
            ellipse_height
        ]
        pygame.draw.ellipse(mask_surface, (0, 0, 0, 0), ellipse_rect, 0)
        return mask_surface

    def create_mask2(self):
        # Create a surface with per-pixel alpha
        mask_size = self.sclera_radius * 2
        mask_surface = pygame.Surface((mask_size, mask_size), pygame.SRCALPHA)
        # Fill with grey color
        pygame.draw.rect(mask_surface, self.mask_color, [0, 0, mask_size, mask_size])
        
        # Define ellipse dimensions
        ellipse_width = mask_size
        ellipse_height = mask_size * 0.6  # Height is less than width for an elongated ellipse
        ellipse_rect = [
            (mask_size - ellipse_width) // 2,
            (mask_size - ellipse_height) // 2,
            ellipse_width,
            ellipse_height
        ]
        
        # Draw ellipse
        pygame.draw.ellipse(mask_surface, (0, 0, 0, 0), ellipse_rect, 0)

        # Draw pointy ends by adding triangles or trapezoids
        # Define points for a triangle at the left end
        left_triangle = [
            (ellipse_rect[0], ellipse_rect[1] + ellipse_rect[3] // 2),  # Top of the center line
            (ellipse_rect[0] - 10, ellipse_rect[1]),  # Point extends past left edge
            (ellipse_rect[0] - 10, ellipse_rect[1] + ellipse_rect[3])  # Bottom point
        ]
        # Define points for a triangle at the right end
        right_triangle = [
            (ellipse_rect[0] + ellipse_rect[2], ellipse_rect[1] + ellipse_rect[3] // 2),  # Top of the center line
            (ellipse_rect[0] + ellipse_rect[2] + 10, ellipse_rect[1]),  # Point extends past right edge
            (ellipse_rect[0] + ellipse_rect[2] + 10, ellipse_rect[1] + ellipse_rect[3])  # Bottom point
        ]
        # Draw triangles with transparent color
        pygame.draw.polygon(mask_surface, (0, 0, 0, 0), left_triangle, 0)
        pygame.draw.polygon(mask_surface, (0, 0, 0, 0), right_triangle, 0)

        return mask_surface
