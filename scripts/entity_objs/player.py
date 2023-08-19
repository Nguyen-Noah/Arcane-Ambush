import pygame, math
from ..entity import Entity
from ..skills import SKILLS
from ..inventory import Inventory

class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = [0, 0]
        self.allow_movement = True
        self.moving = False
        self.direction = 'down'
        self.money = 100
        self.skills = [SKILLS['dagger'](self.game, self), None, None, None]
        self.inventory = Inventory(self)

        self.attacking = False
        self.atk_counter = 0
        
        self.counter = [False, False]

    def give_item(self, item, slot_group='items'):
        # remove existing active tags
        item.tags = [tag for tag in item.tags if tag != 'active']

        if not len(self.inventory.get_custom_group('active_weapons')):
            self.weapon_hide = 3
        if slot_group == 'active':
            item.tags.append('active')
        self.inventory.add_item(item, slot_group if slot_group != 'active' else 'items')

    def attempt_move(self, axis, direction):
        if self.allow_movement:
            
            if axis == 0:
                self.flip[0] = direction < 0
                self.direction = 'side'
            #else:
                #if direction == 1:
                    #self.direction = 'down'
                #else:
                    #self.direction = 'up'
            if not self.moving:
                self.game.world.world_animations.spawn('player_dust', [self.center[0], self.center[1]], flip=self.flip)

            movement_vector = pygame.math.Vector2(0, 0)
            movement_vector[axis] = direction

            if movement_vector.length() != 0:
                movement_vector.normalize_ip()

            movement_vector *= self.speed * self.game.window.dt

            self.frame_motion += movement_vector
        self.moving = True

    def print_hitbox(self):
        pygame.draw.rect(self.game.window.display, 'blue', (self.rect[0] - self.game.world.camera.true_pos[0], self.rect[1] - self.game.world.camera.true_pos[1], self.rect[2], self.rect[3]), 1)

    def update(self, dt):
        self.frame_motion = self.velocity.copy()

        r = super().update(dt)
        if not r:
            return r
        
        if self.game.input.states['left']:
            self.attempt_move(0, -1)
            self.counter[0] = True
        if self.game.input.states['right']:
            self.attempt_move(0, 1)
            self.counter[0] = True

        if self.game.input.states['up']:
            self.attempt_move(1, -1)
            self.counter[1] = True
        if self.game.input.states['down']:
            self.attempt_move(1, 1)
            self.counter[1] = True

        if not self.game.input.states['left'] and not self.game.input.states['right']:
            self.counter[0] = False
        if not self.game.input.states['up'] and not self.game.input.states['down']:
            self.counter[1] = False

        if not self.attacking:
            if self.counter[0] or self.counter[1]:
                self.set_action('walk', self.direction)
            else:
                self.set_action('idle', self.direction)
                self.moving = False

        # weapon
        if self.game.input.mouse_state['left_click'] or self.attacking:
            self.atk_counter += self.game.window.dt
            self.skills[0].use()
            if self.atk_counter > self.skills[0].cooldown:
                self.attacking = False
                self.allow_movement = True
                self.atk_counter = 0

        self.collisions = self.move(self.frame_motion, self.game.world.collideables)
        self.print_hitbox()

        pygame.draw.line(self.game.window.display, 'blue', (self.rect[0] - self.game.world.camera.true_pos[0] + (self.size[0] // 2), self.rect[1] - self.game.world.camera.true_pos[1] + (self.size[1] // 2)), self.game.input.mouse_pos)

        return self.alive