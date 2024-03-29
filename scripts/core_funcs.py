import pygame, math
from csv import reader

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
    
def normalize_color(color):
    return (color[0] / 255, color[1] / 255, color[2] / 255)

def normalize(value, amount, around=0):
    if (value - amount) > around:
        value -= amount
    elif (value + amount) < around:
        value += amount
    else:
        value = around
    return value

def normalize_vector(vector, amount, around=0):
    angle = math.atan2(vector[1], vector[0])
    magnitude = math.sqrt(vector[1] ** 2 + vector[0] ** 2)
    magnitude = normalize(magnitude, amount, around=around)
    vector[1] = math.sin(angle) * magnitude
    vector[0] = math.cos(angle) * magnitude

def clamp_between(tuple, min_offset=(0, 0), max_offset=(100, 100)):
    clamped_x = max(min_offset[0], min(tuple[0], max_offset[0]))
    clamped_y = max(min_offset[1], min(tuple[1], max_offset[1]))
    return [clamped_x, clamped_y]

def lerp(a, b, t):
    return a + (b - a) * t

def easeInBack(x, overshoot=1.70158):
    return x * x * ((overshoot + 1) * x - overshoot)

def read_f(path):
    f = open(path, 'r')
    dat = f.read()
    f.close()
    return dat

def write_f(path, dat):
    f = open(path, 'w')
    f.write(dat)
    f.close()

def load_img(path, colorkey):
    img = pygame.image.load(path).convert()
    img.set_colorkey(colorkey)
    return img

def swap_color(img, old_c, new_c):
    global e_colorkey
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img,(0,0))
    return surf

def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

def rect_corners(points):
    point_1 = points[0]
    point_2 = points[1]
    out_1 = [min(point_1[0], point_2[0]), min(point_1[1], point_2[1])]
    out_2 = [max(point_1[0], point_2[0]), max(point_1[1], point_2[1])]
    return [out_1, out_2]

def corner_rect(points):
    points = rect_corners(points)
    r = pygame.Rect(points[0][0], points[0][1], points[1][0] - points[0][0], points[1][1] - points[0][1])
    return r

def points_between_2d(points):
    points = rect_corners(points)
    width = points[1][0] - points[0][0] + 1
    height = points[1][1] - points[0][1] + 1
    point_list = []
    for y in range(height):
        for x in range(width):
            point_list.append([points[0][0] + x, points[0][1] + y])
    return point_list

def to_cart(angle, dis):
    return [math.cos(angle) * dis, math.sin(angle) * dis]

def to_polar(vector):
    return [math.atan2(*(vector[::-1])), get_dis([0, 0], vector)]

def angle_to(points):
    return math.atan2(points[1][1] - points[0][1], points[1][0] - points[0][0])

def blit_center(target_surf, surf, loc, add=False):
    if not add:
        target_surf.blit(surf, (loc[0] - surf.get_width() // 2 + 1, loc[1] - surf.get_height() // 2 + 1))
    else:
        target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2), special_flags=pygame.BLEND_RGBA_ADD)

def itr(l):
    return sorted(enumerate(l), reverse=True)

def advance(pos, angle, amt):
    pos[0] += math.cos(angle) * amt
    pos[1] += math.sin(angle) * amt
    return pos

def get_dis(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def round_nearest(x, base):
    return base * round(x/base)

def tuplify(list):
    new_tuple = []
    for i in list:
        new_tuple.append(tuple(i))
    return new_tuple

# make sure to multiply this by dt and speed
"""
self.frame_motion[0] += dist[0] * speed * dt
self.frame_motion[1] += dist[1] * speed * dt
"""
def get_target_dist(origin, target):
    dist = [target[0] - origin[0], target[1] - origin[1]]

    magnitude = math.sqrt(dist[0] ** 2 + dist[1] ** 2)
    if magnitude == 0:
        return [0, 0]

    return [dist[0] / magnitude, dist[1] / magnitude]

# used in tandem to check for collisions of a rotated rect
def collideLineLine(P0, P1, Q0, Q1):  
    d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
    if d == 0:
        return False
    t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
    u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
    return 0 <= t <= 1 and 0 <= u <= 1

def colideRectLine(rect, p1, p2):
    return (collideLineLine(p1, p2, rect.topleft, rect.bottomleft) or
            collideLineLine(p1, p2, rect.bottomleft, rect.bottomright) or
            collideLineLine(p1, p2, rect.bottomright, rect.topright) or
            collideLineLine(p1, p2, rect.topright, rect.topleft))

def outline(img, color=(255, 255, 255)):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    mask_surf = pygame.Surface(img.get_size())
    for pixel in mask_outline:
        mask_surf.set_at(pixel, color)
    mask_surf.set_colorkey((0, 0, 0))
    center = ((img.get_width() // 2) - (mask_surf.get_width() // 2), (img.get_height() // 2) - (mask_surf.get_height() // 2))
    surf = pygame.Surface((img.get_width() + 2, img.get_height() + 2))
    surf.set_colorkey((0, 0, 0))
    surf.blit(mask_surf, (center[0]-1, center[1]))
    surf.blit(mask_surf, (center[0]+1, center[1]))
    surf.blit(mask_surf, (center[0], center[1]-1))
    surf.blit(mask_surf, (center[0], center[1]+1))

    return surf

def pivot_rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotate(surface, -angle)  # Rotate the image.
    rotated_image.set_colorkey((0, 0, 0))
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

def collision_list(obj, obj_list):
    hit_list = []
    for r in obj_list:
        if obj.colliderect(r):
            hit_list.append(r)
    return hit_list
