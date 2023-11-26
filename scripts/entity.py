import pygame, math, random
from .config import config
from .core_funcs import tuplify, round_nearest

def collision_list(obj, obj_list):
    hit_list = []
    for r in obj_list:
        if obj.colliderect(r):
            hit_list.append(r)
    return hit_list

class Entity:
    def __init__(self, game, pos, size, type, category):
        self.game = game
        self.pos = list(pos).copy()
        self.size = size
        self.type = type
        self.category = category
        self.centered = False
        self.active_animation = None
        self.flip = [False, False]
        self.direction = 'side'
        self.scale = [1, 1]
        self.rotation = 0
        self.opacity = 255
        self.height = 0
        self.alive = True
        self.targetable = True
        self.hurt = 0
        if self.type in config['entities']:
            self.max_health = config['entities'][self.type]['health']
            self.speed = config['entities'][self.type]['speed']
        self.bounce = 0
        self.health = self.max_health

        if self.type + '_walk_side' in self.game.assets.animations.animations:
            self.set_action('walk', 'side')

        self.target_index = 1
        self.offset = [0, 0]
        self.path_complete = True

        self.gen_mask()

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
            return [self.rect[0] + (self.size[0] // 2), self.rect[1] + (self.size[1] // 2)]

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

    def follow_path(self):
        self.path = tuplify(config['level_data']['tutorial']['path'])

        # getting path -------------------------------------------------------------------------------------- #
        if self.target_index < len(self.path):
            self.target_position = pygame.math.Vector2(self.path[self.target_index])
            self.movement = self.target_position - self.pos - self.offset
            if self.path_complete:
                self.offset = [0, 0]
                if self.target_index != 1:
                    random_offset = random.randint(-8, 8)
                else:
                    random_offset = 0
                if abs(self.movement[0]) > abs(self.movement[1]):
                    self.offset[1] += self.movement[1] + random_offset
                else:
                    self.offset[0] += self.movement[0] + random_offset
        else:
            self.die()

        dist = self.movement.length()

        # animation handling -------------------------------------------------------------------------------- #
        if self.path_complete:
            if abs(self.movement[0]) < abs(self.movement[1]):
                if self.movement[1] > 0:
                    self.direction = 'down'
                else:
                    self.direction = 'up'
            else:
                self.direction = 'side'
                if self.movement[0] > 0:
                    self.flip[0] = False
                else:
                    self.flip[0] = True
                    
            self.path_complete = False

        # movement handling --------------------------------------------------------------------------------- #
        # 0.5 is used for how strict the enemies will follow the path; the lower, the more strict
        if dist >= 0.5:
            self.pos += self.movement.normalize() * self.speed * self.game.window.dt
        else:
            #if dist != 0:
                #self.pos += self.movement.normalize() * self.speed * self.game.window.dt
            self.path_complete = True
            self.target_index += 1

        self.set_action('walk', self.direction)

    def print_hitbox(self):
        pygame.draw.rect(self.game.window.display, 'blue', (self.rect[0] - self.game.world.camera.true_pos[0], self.rect[1] - self.game.world.camera.true_pos[1], self.rect[2], self.rect[3]), 1)

    def die(self, angle=0):
        if self.type != 'player':
            self.game.world.world_animations.spawn('death_sparks', self.center, flip=self.flip)
            for i in range(random.randint(7, 20)):
                random_angle = angle + (random.random() - 0.5) / 3.5
                if random.randint(1, 4) == 1:
                    random_angle = angle + (random.random() - 0.5) / 7 + math.pi
                random_speed = random.randint(20, 100)
                vel = [math.cos(random_angle) * random_speed, math.sin(random_angle) * random_speed]
                self.game.world.vfx.spawn_vfx('spark', self.center.copy(), vel, 1 + random.random(), (15, 15, 8), drag=50)

            self.alive = False
        else:
            self.active_animation = self.game.assets.animations.new(self.type + '_die_side')
            self.death_frames = sum(self.active_animation.data.config['frames'])

            self.targetable = False
            print(self.targetable)

    def damage(self, amount, angle=0):
        self.hurt = 1
        self.health -= amount
        if self.health <= 0:
            self.die(angle)
            return True
        return False

    def gen_mask(self):
        self.mask = pygame.mask.from_surface(self.img)

    def calculate_render_offset(self, offset=(0, 0)):
        offset = list(offset)
        if self.active_animation:
            offset[0] += self.active_animation.data.config['offset'][0]
            offset[1] += self.active_animation.data.config['offset'][1]
        if self.centered:
            offset[0] += self.img.get_width() // 2
            offset[1] += self.img.get_height() // 2
        return offset

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
            #self.print_hitbox()
            self.active_animation.play(dt)
        
        return self.alive