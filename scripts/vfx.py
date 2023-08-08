import pygame, math, random

GLOW_CACHE = {}
GLOW_SURFS = []

def glow(loc, radius, angle, color):
    glow_id = (int(radius), color)
    
    if glow_id in GLOW_CACHE:
        GLOW_SURFS.append([GLOW_CACHE[glow_id], (loc[0] - radius, loc[1] - radius)])
        return None
    
    render_surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(render_surf, color, (radius, radius), radius)
    
    if render_surf.get_width() * render_surf.get_height() == 0:
        angle = 0

    if angle:
        render_surf.set_colorkey((0, 0, 0))
        rotated_surf = pygame.transform.rotate(render_surf, angle)
    else:
        rotated_surf = render_surf

    GLOW_SURFS.append([rotated_surf, (loc[0] - rotated_surf.get_width() // 2, loc[1] - rotated_surf.get_height() // 2)])
    GLOW_CACHE[glow_id] = render_surf

def render_glow(surf):
    global GLOW_SURFS
    for glow in GLOW_SURFS:
        surf.blit(glow[0], glow[1], special_flags=pygame.BLEND_RGBA_ADD)
    GLOW_SURFS = []