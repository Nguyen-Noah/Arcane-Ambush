import pygame, math

# don't use every frame, put into a list
def gradient_circle(radius, inner_color, outer_color):
    circle_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    for y in range(radius*2):
        for x in range(radius*2):
            dx = radius - x
            dy = radius - y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance <= radius:
                # Calculate the current ratio of the distance from the center to the radius
                ratio = distance / radius
                # Linear interpolation between the inner color and the outer color
                color = (
                    int(inner_color[0] * (1 - ratio) + outer_color[0] * ratio),
                    int(inner_color[1] * (1 - ratio) + outer_color[1] * ratio),
                    int(inner_color[2] * (1 - ratio) + outer_color[2] * ratio),
                )
                # Set the color of the pixel
                circle_surf.set_at((x, y), color)

    return circle_surf