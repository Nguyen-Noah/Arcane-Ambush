import pygame, math
from ..entity import Entity
from ..skills import SKILLS

class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = [0, 0]
        self.allow_movement = True
        self.direction = 'down'
        self.money = 100
        self.skills = [SKILLS['dagger'](self.game, self), None, None, None]

        self.attacking = False
        self.atk_counter = 0
        self.atk_cd = 1
        
        self.counter = [False, False]

    def attempt_move(self, axis, direction):
        if self.allow_movement:
            if axis == 0:
                self.flip[0] = direction < 0
                self.direction = 'side'
            else:
                if direction == 1:
                    self.direction = 'down'
                else:
                    self.direction = 'up'
            movement_vector = pygame.math.Vector2(0, 0)
            movement_vector[axis] = direction

            if movement_vector.length() != 0:
                movement_vector.normalize_ip()

            movement_vector *= self.speed * self.game.window.dt

            self.frame_motion += movement_vector

    def swing(self):
        self.atk_cd = self.game.window.dt * self.active_animation.data.config['speed']
        if not self.attacking:
            self.set_action('attack', self.direction)
            timer = 0
            for time in self.active_animation.data.config['frames']:
                timer += time
            
            if self.active_animation.frame < (timer - self.active_animation.data.config['frames'][3]):
                self.attacking = True

            angle = math.atan2(self.game.input.mouse_pos[1] - self.center[1] + self.game.world.camera.true_pos[1], self.game.input.mouse_pos[0] - self.center[0] + self.game.world.camera.true_pos[0])
            self.aim_angle = angle
            if (self.rotation % 360 < 270) and (self.rotation % 360 > 90):
                self.game.world.world_animations.spawn('dagger_slash', [self.center[0], self.center[1]], self.aim_angle, flip=[True, self.flip[0]])
            else:
                if self.direction == 'down' or self.direction == 'up':
                    self.game.world.world_animations.spawn('dagger_slash', [self.center[0], self.center[1]], self.aim_angle, flip=[False, not self.flip[0]])
                else:
                    self.game.world.world_animations.spawn('dagger_slash', [self.center[0], self.center[1]], self.aim_angle, flip=[False, self.flip[0]])

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

        # weapon
        if self.game.input.mouse_state['left_click'] or self.attacking:
            self.atk_counter += self.game.window.dt
            self.swing()
            if self.atk_counter > self.atk_cd:
                self.attacking = False
                self.allow_movement = True
                self.atk_counter = 0

        self.collisions = self.move(self.frame_motion, self.game.world.collideables)
        self.print_hitbox()

        pygame.draw.line(self.game.window.display, 'blue', (self.rect[0] - self.game.world.camera.true_pos[0] + (self.size[0] // 2), self.rect[1] - self.game.world.camera.true_pos[1] + (self.size[1] // 2)), self.game.input.mouse_pos)

        return self.alive