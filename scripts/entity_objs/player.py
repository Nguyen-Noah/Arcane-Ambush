import pygame, math
from ..core_funcs import get_dis
from ..entity import Entity
from ..skills import SKILLS
from ..inventory import Inventory
from ..item import Item

class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = [0, 0]
        self.allow_movement = True
        self.moving = False
        self.direction = 'side'
        self.vx = 0
        self.vy = 0
        self.last_move_attempt = 0
        self.money = 100
        self.skills = [None, None, None, None, None, None, None, None, None]
        self.owned_towers = ['wizard_tower', None, None, None, None]
        self.inventory = Inventory(self)
        self.selected_slot = 0
        self.weapon_hide = 0
        self.attacking = False
        self.atk_counter = 0
        self.combo_counter = 0
        self.counter = [False, False]
        self.aim_angle = 0

    @property
    def weapon(self):
        if self.selected_slot < len(self.inventory.get_custom_group('active_weapons')):
            return self.inventory.get_custom_group('active_weapons')[self.selected_slot]
        else:
            return None

    def give_item(self, item, slot_group='items'):
        # remove existing active tags
        item.tags = [tag for tag in item.tags if tag != 'active']

        if not len(self.inventory.get_custom_group('active_weapons')):
            self.weapon_hide = 3
        if slot_group == 'active':
            item.tags.append('active')
        self.inventory.add_item(item, slot_group if slot_group != 'active' else 'items')

    def load_actives(self):
        active_items = self.inventory.get_custom_group('active')
        for item in active_items:
            if item.is_skill and not item.is_unowned_skill:
                self.skills[0] = SKILLS[item.type](self.game, self)
            if item.is_consumable:
                self.skills[3] = item

    def get_mouse_pos(self):
        val = get_dis((self.rect[0] - self.game.world.camera.true_pos[0] + (self.size[0] // 2), self.rect[1] - self.game.world.camera.true_pos[1] + (self.size[1] // 2)), self.game.input.mouse_pos)
        x_offset = (self.rect[0] + (self.size[0] // 2)) + (val * math.cos(self.aim_angle))
        y_offset = (self.rect[1] + (self.size[1] // 2)) + (val * math.sin(self.aim_angle))
        return (x_offset, y_offset)

    def attempt_move(self, axis, direction):
        if self.allow_movement:
            if axis == 0:
                self.flip[0] = direction < 0
                self.direction = 'side'
            if not self.moving:
                if direction != self.last_move_attempt:
                    self.game.world.world_animations.spawn('player_dust', [self.center[0], self.center[1]], flip=self.flip)

            movement_vector = pygame.math.Vector2(0, 0)
            movement_vector[axis] = direction

            if movement_vector.length() != 0:
                movement_vector.normalize_ip()

            movement_vector *= self.speed * self.game.window.dt

            self.frame_motion += movement_vector
        self.moving = True
        
    def update(self, dt):
        self.frame_motion = self.velocity.copy()

        r = super().update(dt)
        if not r:
            return r
        
        # movement
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

        # animations code
        if self.targetable:
            if not self.attacking:
                if self.counter[0] or self.counter[1]:
                    self.set_action('walk', self.direction)
                else:
                    self.set_action('idle', self.direction)
                    self.moving = False

        # weapon
        if (self.game.input.mouse_state['left_click'] or self.attacking) and not self.game.world.builder_mode and self.targetable:
            self.atk_counter += self.game.window.dt
            self.weapon.attempt_attack()
            if self.atk_counter > self.weapon.attack_rate:
                self.attacking = False
                self.allow_movement = True
                self.atk_counter = 0

        # collisions and move ---------------------------------------------------------- #
        self.collisions = self.move(self.frame_motion, self.game.world.collideables)
        #pygame.draw.circle(self.game.window.display, 'red', (self.center[0] - self.game.world.camera.true_pos[0], self.center[1] - self.game.world.camera.true_pos[1]), 6)

        # inventory -------------------------------------------------------------------- #
        if self.game.input.mouse_state['scroll_up']:
            self.weapon_hide = 3
            self.selected_slot -= 1
            if self.selected_slot < 0:
                self.selected_slot = len(self.inventory.get_custom_group('active_weapons')) - 1
        if self.game.input.mouse_state['scroll_down']:
                self.weapon_hide = 3
                self.selected_slot += 1
                if self.selected_slot >= len(self.inventory.get_custom_group('active_weapons')):
                    self.selected_slot = 0

        # weapon stuff ----------------------------------------------------------------- #
        angle = math.atan2(self.game.input.mouse_pos[1] - self.center[1] + self.game.world.camera.render_offset[1], self.game.input.mouse_pos[0] - self.center[0] + self.game.world.camera.render_offset[0])
        self.aim_angle = angle
        #print(self.aim_angle)
        if self.weapon:
            self.weapon.rotation = math.degrees(angle)

        pygame.draw.line(self.game.window.display, 'blue', (self.rect[0] - self.game.world.camera.true_pos[0] + (self.size[0] // 2), self.rect[1] - self.game.world.camera.true_pos[1] + (self.size[1] // 2)), self.game.input.mouse_pos)

        if not self.targetable:
            self.allow_movement = False
            self.weapon_hide = 0
        print(self.health)

        return self.alive

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)
        if self.weapon and self.weapon_hide:
            self.weapon.render(surf, (self.rect[0] - self.game.world.camera.true_pos[0] + (self.size[0] // 2), self.rect[1] - self.game.world.camera.true_pos[1] + (self.size[1] // 2)))