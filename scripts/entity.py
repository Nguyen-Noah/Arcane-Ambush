import pygame
from .config import config

def collision_list(obj, obj_list):
    hit_list = []
    for r in obj_list:
        if obj.colliderect(r):
            hit_list.append(r)
    return hit_list

class Entity:
    def __init__(self, game, pos, size, type):
        self.game = game
        self.pos = list(pos).copy()
        self.size = size
        self.type = type
        self.centered = False
        self.active_animation = None
        self.flip = [False, False]
        self.scale = [1, 1]
        self.rotation = 0
        self.opacity = 255
        self.height = 0
        self.alive = True
        if self.type in config['entities']:
            self.max_health = config['entities'][self.type]['health']
            self.speed = config['entities'][self.type]['speed']
        self.bounce = 0

        if self.type + '_idle_down' in self.game.assets.animations.animations:
            self.set_action('idle', 'down')

    @property
    def img(self):
        if not self.active_animation:
            img = self.current_image
        else:
            self.set_image(self.active_animation.img)
            img = self.current_image
        if self.scale != [1, 1]:
            img = pygame.transform.scale(img, (int(self.scale[0] * self.image_base_dimensions[0]), int(self.scale[1] * self.image_base_dimensions[1])))
        if any(self.flip):
            img = pygame.transform.flip(self.current_image, self.flip[0], self.flip[1])
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        if self.opacity != 255:
            img.set_alpha(self.opacity)
        return img

    @property
    def rect(self):
        if not self.centered:
            return pygame.Rect(self.pos[0] // 1, self.pos[1] // 1, self.size[0], self.size[1])
        else:
            return pygame.Rect((self.pos[0] + self.size[0] // 2) // 1, (self.pos[1] + self.size[1] // 2))

    @property
    def center(self):
        if self.centered:
            return self.pos.copy()
        else:
            return [self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2]

    def set_action(self, action_id, direction, force=False):
        if force:
            self.active_animation = self.assets.new(self.type + '_' + action_id + '_' + direction)
        elif (not self.active_animation) or (self.active_animation.data.id != self.type + '_' + action_id + '_' + direction):
            self.active_animation = self.game.assets.animations.new(self.type + '_' + action_id + '_' + direction)

    def set_image(self, surf):
        self.current_image = surf.copy()
        self.image_base_dimensions = list(surf.get_size())

    def move(self, motion, tiles):
        self.pos[0] += motion[0]
        hit_list = collision_list(self.rect, tiles)
        temp_rect = self.rect
        directions = {k : False for k in ['top', 'left', 'right', 'bottom']}
        for tile in hit_list:
            if motion[0] > 0:
                temp_rect.right = tile.left
                self.pos[0] = temp_rect.x
                directions['right'] = True
            if motion[0] < 0:
                temp_rect.left = tile.right
                self.pos[0] = temp_rect.x
                directions['left'] = True
            if self.centered:
                self.pos[0] += self.size[0] // 2
        self.pos[1] += motion[1]
        hit_list = collision_list(self.rect, tiles)
        temp_rect = self.rect
        for tile in hit_list:
            if motion[1] > 0:
                temp_rect.bottom = tile.top
                self.pos[1] = temp_rect.y
                directions['bottom'] = True
            if motion[1] < 0:
                temp_rect.top = tile.bottom
                self.pos[1] = temp_rect.y
                directions['top'] = True
            if self.centered:
                self.pos[1] += self.size[1] // 2
        return directions


    def render(self, surf, offset=(0, 0)):
        offset = list(offset)
        if self.active_animation:
            offset[0] += self.active_animation.data.config['offset'][0]
            offset[1] += self.active_animation.data.config['offset'][1]
        if self.centered:
            offset[0] += self.img.get_width() // 2
            offset[1] += self.img.get_height() // 2
        surf.blit(self.img, ((self.pos[0] - offset[0]) // 1, (self.pos[1] - offset[1] - self.height) // 1))

    def update(self, dt):
        if self.active_animation:
            self.active_animation.play(dt)
        
        return self.alive