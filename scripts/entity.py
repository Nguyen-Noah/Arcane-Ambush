import pygame, math, random
from .config import config
from .core_funcs import normalize

def collision_list(obj, obj_list):
    hit_list = []
    for r in obj_list:
        if obj.colliderect(r):
            hit_list.append(r)
    return hit_list

class Entity:
    def __init__(self, game, pos, size, type, category, controller=None, movement_type='ground'):
        self.game = game
        self.pos = list(pos).copy()
        self.home = self.pos.copy()
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
        self.i_frames = 0
        self.moving = False

        if self.type + '_walk' in self.game.assets.animations.animations:
            self.set_action('walk')

        self.controller = controller
        if self.controller not in ['player', None]:
            self.controller = controller(self)

        self.movement_type = movement_type
        if self.movement_type == 'ground':
            self.orig_particle_timer = 0.03
            self.dust_particle_timer = 0.03
        else:
            self.orig_particle_timer = 0
            self.dust_particle_timer = 0

        self.gen_mask()
        self.gen_shadow()

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

    def set_action(self, action_id, force=False):
        if force:
            self.active_animation = self.assets.new(self.type + '_' + action_id)
        elif (not self.active_animation) or (self.active_animation.data.id != self.type + '_' + action_id):
            self.active_animation = self.game.assets.animations.new(self.type + '_' + action_id)

    def set_image(self, surf):
        self.current_image = surf.copy()
        self.image_base_dimensions = list(surf.get_size())

    def draw_hitframe(self, surf, pos, anim_offset):
        mask = pygame.mask.from_surface(self.img)
        surf.blit(mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), (pos[0] - anim_offset[0], pos[1] - anim_offset[1]))

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

    def print_hitbox(self):
        pygame.draw.rect(self.game.window.display, 'blue', (self.rect[0] - self.game.world.camera.true_pos[0], self.rect[1] - self.game.world.camera.true_pos[1], self.rect[2], self.rect[3]), 1)

    def die(self, angle=0):
        #self.game.world.world_animations.spawn('death_sparks', self.center, flip=self.flip)
        self.game.world.vfx.spawn_vfx('circle', self.center.copy(), 4, 6, 25)
        #self.game.world.vfx.spawn_vfx('circle', self.center.copy(), 4, 8, 100)
        for i in range(random.randint(7, 20)):
            random_angle = angle + (random.random() - 0.5) / 3.5
            if random.randint(1, 4) == 1:
                random_angle = angle + (random.random() - 0.5) / 7 + math.pi
            random_speed = random.randint(20, 100)
            vel = [math.cos(random_angle) * random_speed, math.sin(random_angle) * random_speed]
            self.game.world.vfx.spawn_vfx('spark', self.center.copy(), vel, 1 + random.random(), drag=50)

        self.alive = False

    def damage(self, amount, angle=0):
        self.hurt = 0.2
        self.health -= amount

        if self.type == 'player':
            self.game.world.camera.add_screen_shake(20)

        if self.health <= 0:
            self.die(angle)
            return True
        return False

    def gen_mask(self):
        self.mask = pygame.mask.from_surface(self.img)

    def gen_shadow(self):
        self.shadow = pygame.Surface((self.img.get_width(), self.img.get_height() / 3))
        self.shadow.fill((0, 0, 0))
        self.shadow.set_colorkey((0, 0, 0))
        self.shadow.set_alpha(150)
        pygame.draw.ellipse(self.shadow, (17, 17, 17), (0, 0, self.shadow.get_width(), self.shadow.get_height()))

    def calculate_render_offset(self, offset=(0, 0)):
        offset = list(offset)
        if self.active_animation:
            offset[0] += self.active_animation.data.config['offset'][0]
            offset[1] += self.active_animation.data.config['offset'][1]
        if self.centered:
            offset[0] += self.img.get_width() // 2
            offset[1] += self.img.get_height() // 2
        return offset

    def render(self, surf, offset=(0, 0), anim_offset=(0, 0)):
        offset = list(offset)
        if self.active_animation:
            offset[0] += self.active_animation.data.config['offset'][0]
            offset[1] += self.active_animation.data.config['offset'][1]
        if self.centered:
            offset[0] += self.img.get_width() // 2
            offset[1] += self.img.get_height() // 2

        if self.type in self.game.world.particles.particle_groups:
            self.game.world.particles.render(self.type, surf, offset)
        render_pos = (self.pos[0] - offset[0], self.pos[1] - offset[1])
        surf.blit(self.shadow, (render_pos[0], render_pos[1] + self.height - (self.shadow.get_height() / 2)))
        surf.blit(self.img, (render_pos[0] - anim_offset[0], render_pos[1] - anim_offset[1]))
        if self.hurt:
            self.draw_hitframe(surf, render_pos, anim_offset)

    def update(self, dt):
        self.height = self.img.get_height()

        if self.i_frames > 0:
            self.i_frames = normalize(self.i_frames, dt)

        if self.moving:
            if random.randint(1, 50) == 1:
                smoke_emitter = 'smoke_' + str(random.randint(0, 2))
                self.game.world.particles.add_particle(self.type, (self.pos[0] + random.randint(0, self.img.get_width()), self.pos[1] + self.height), smoke_emitter, [0, 0], 5, random.randint(2, 4))

        if self.controller not in ['player', None]:
            self.controller.update(dt)

        if self.active_animation:
            self.active_animation.play(dt)
            if self.hurt > 0:
                self.hurt -= dt
            else:
                self.hurt = 0
        
        return self.alive