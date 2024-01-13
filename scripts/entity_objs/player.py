import pygame, math
from ..core_funcs import normalize_vector, normalize
from ..entity import Entity
from ..skills import SKILLS
from ..inventory import Inventory
from ..config import config

class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = [0, 0]
        self.allow_movement = True
        self.moving = False
        self.vx = 0
        self.vy = 0
        self.last_move_attempt = 0
        self.money = 100000
        self.skills = [SKILLS['dash'](self.game, self), None, None, None, None, None, None, None, None]
        self.inventory = Inventory(self)
        self.selected_inventory_slot = 0
        self.counter = [False, False]
        self.aim_angle = 0
        self.attacking = False
        self.attack_movement_slow = 0
        self.movement_skill = False
        self.base_health = config['entities']['player']['health']

        # PUT THIS IN THE CONFIG EVENTUALLY
        self.mana = 100

        self.game.world.lights.attach_owner('player', self)

    @property
    def weapon(self):
        if self.selected_inventory_slot < len(self.inventory.get_custom_group('active_weapons')):
            return self.inventory.get_custom_group('active_weapons')[self.selected_inventory_slot]
        else:
            return None
        
    def heal(self, amount):
        self.health += amount
        self.health = min(self.health, self.base_health)

    def give_item(self, item, slot_group='items'):
        # remove existing active tags
        item.tags = [tag for tag in item.tags if tag != 'active']

        if slot_group == 'active':
            item.tags.append('active')
        self.inventory.add_item(item, slot_group if slot_group != 'active' else 'items')

    def load_actives(self):
        active_items = self.inventory.get_custom_group('active')
        for item in active_items:
            if item.is_skill and not item.is_unowned_skill:
                self.skills[0] = SKILLS[item.type](self.game, self)
                
    def attempt_move(self, axis, direction):
        if self.allow_movement:
            if axis == 0:
                self.flip[0] = direction < 0
            if not self.moving:
                if direction != self.last_move_attempt:
                    self.game.world.world_animations.spawn('player_dust', self.center.copy(), flip=self.flip)

            movement_vector = pygame.math.Vector2(0, 0)
            movement_vector[axis] = direction

            if movement_vector.length() != 0:
                movement_vector.normalize_ip()

            movement_vector *= self.speed * self.game.window.dt

            self.frame_motion += movement_vector
        self.moving = True
    
    def process_kill(self, entity):
        pass

    def die(self, angle=0):
        self.game.world.world_animations.spawn('player_die_side', (self.pos[0] - self.img.get_width() // 2, self.pos[1] - self.img.get_height() // 2), flip=self.flip)
        self.death_frames = sum(self.active_animation.data.config['frames'])

        self.alive = False
        
    def update(self, dt):
        self.frame_motion = self.velocity.copy()

        r = super().update(dt)
        if not r:
            return r
        
        for skill in self.skills:
            if skill:
                skill.update()

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

        # weapon stuff ----------------------------------------------------------------- #
        angle = math.atan2(self.game.input.mouse_pos[1] - self.center[1] + self.game.world.camera.render_offset[1], self.game.input.mouse_pos[0] - self.center[0] + self.game.world.camera.render_offset[0])
        self.aim_angle = angle
        if self.weapon:
            self.weapon.rotation = math.degrees(angle)

            if self.weapon.enable_update:
                self.weapon.update()

        # animations code
        if self.targetable:
            if self.game.input.states['left'] or self.game.input.states['right'] or self.game.input.states['up'] or self.game.input.states['down']:
                self.set_action('walk')
            else:
                self.set_action('idle')
                self.moving = False

            # weapon
            if self.weapon:
                if self.game.input.mouse_state['left_click'] and not self.game.world.builder_mode:
                    self.weapon.attacking = True
                    self.speed = config['entities']['player']['speed'] // 2
                    self.weapon.attempt_attack()
                if self.weapon.attacking:
                    self.attack_movement_slow += dt
                    if self.attack_movement_slow >= self.weapon.attack_rate:
                        self.weapon.attacking = False
                        self.speed = config['entities']['player']['speed'] 
                        self.attack_movement_slow = 0

            if (math.degrees(self.aim_angle) % 360 < 270) and (math.degrees(self.aim_angle) % 360 > 90):
                self.flip[0] = True
            else:
                self.flip[0] = False

            if self.invincible > 0:
                self.invincible = normalize(self.invincible, dt)
            
            if not self.movement_skill:
                normalize_vector(self.velocity, dt * 8)
        else:
            #self.velocity = [0, 0]
            self.weapon.invisible = 0.2

        # collisions and move ---------------------------------------------------------- #
        self.collisions = self.move(self.frame_motion, self.game.world.collideables)

        # inventory -------------------------------------------------------------------- #
        if self.game.input.mouse_state['scroll_down']:
            self.selected_inventory_slot += 1
            if self.selected_inventory_slot >= self.inventory.max_slots:
                self.selected_inventory_slot = 0
        if self.game.input.mouse_state['scroll_up']:
                self.selected_inventory_slot -= 1
                if self.selected_inventory_slot < 0:
                    self.selected_inventory_slot = self.inventory.max_slots - 1

        # skills ----------------------------------------------------------------------- #
        if self.game.input.states['dash']:
            if self.game.input.input_mode == 'core':
                if self.skills[0]:
                    self.skills[0].use()

        if not self.targetable:
            self.allow_movement = False

        return self.alive

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)
        if self.weapon:
            self.weapon.render(surf, (self.rect[0] + (self.size[0] // 2) + 2, self.rect[1] + (self.size[1] // 2)), offset)