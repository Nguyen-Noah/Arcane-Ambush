import pygame, math
from .core_funcs import swap_color

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
        
    def render_skill(self, surf, loc):
        img = self.game.assets.skills[self.skill_type].copy()
        img.set_colorkey((0, 0, 0))
        if not self.charges:
            progress = self.charge / self.charge_rate
            charge_surf = pygame.Surface((img.get_width(), int(img.get_height() * (1 - progress))))
            charge_surf.fill((120, 120, 120))
            img.blit(charge_surf, (0, img.get_height() - charge_surf.get_height()), special_flags=pygame.BLEND_RGB_SUB)
        surf.blit(img, loc)
        if self.charges > 1:
            self.game.assets.fonts['small'].render(str(self.charges), surf, (loc[0] + img.get_width() // 2 - self.game.assets.fonts['small'].width(str(self.charges)) // 2 + 1, loc[1] - 8))
        
class Dagger(Skill):
    def __init__(self, game, owner):
        super().__init__(game, owner, 'dagger')
        self.charge_rate = 0.4

    def use(self):
        self.owner.atk_cd = self.game.window.dt * self.owner.active_animation.data.config['speed']
        if not self.owner.attacking:
            #self.owner.set_action('attack', self.owner.direction)
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