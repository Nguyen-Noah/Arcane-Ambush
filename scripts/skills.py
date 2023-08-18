import pygame, math

class Skill:
    def __init__(self, game, owner, skill_type):
        self.game = game
        self.owner = owner
        self.skill_type = skill_type
        self.max_charges = 1
        self.charges = self.max_charges
        self.charge_rate = 1

    def update(self):
        if self.charges < self.max_charges:
            self.charge += self.game.window.dt
            if self.charge > self.charge_rate:
                self.charge = 0
                self.charges += 1

    def use(self):
        if self.charges:
            self.charges -= 1
            return True
        else:
            return False
        
class Dagger(Skill):
    def __init__(self, game, owner):
        super().__init__(game, owner, 'dagger')

    def use(self):
        self.owner.atk_cd = self.game.window.dt * self.owner.active_animation.data.config['speed']
        if not self.owner.attacking:
            self.owner.set_action('attack', self.owner.direction)
            timer = 0
            for time in self.owner.active_animation.data.config['frames']:
                timer += time
            
            if self.owner.active_animation.frame < (timer - self.owner.active_animation.data.config['frames'][3]):
                self.owner.attacking = True

            angle = math.atan2(self.game.input.mouse_pos[1] - self.owner.center[1] + self.game.world.camera.true_pos[1], self.game.input.mouse_pos[0] - self.owner.center[0] + self.game.world.camera.true_pos[0])
            self.owner.aim_angle = angle
            if (self.owner.rotation % 360 < 270) and (self.owner.rotation % 360 > 90):
                self.game.world.weapon_animations.spawn('dagger_slash', [self.owner.center[0], self.owner.center[1]], self.owner.aim_angle, flip=[True, self.owner.flip[0]])
            else:
                if self.owner.direction == 'down' or self.owner.direction == 'up':
                    self.game.world.weapon_animations.spawn('dagger_slash', [self.owner.center[0], self.owner.center[1]], self.owner.aim_angle, flip=[False, not self.owner.flip[0]])
                else:
                    self.game.world.weapon_animations.spawn('dagger_slash', [self.owner.center[0], self.owner.center[1]], self.owner.aim_angle, flip=[False, self.owner.flip[0]])

SKILLS = {
    'dagger': Dagger
}