import pygame, math, random
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

class Dash(Skill):
    def __init__(self, game, owner):
        super().__init__(game, owner, 'dash')
        self.charge_rate = 1

    def use(self):
        if super().use():
            self.owner.velocity[0] = math.cos(self.owner.aim_angle) * 700
            self.owner.velocity[1] = math.sin(self.owner.aim_angle) * 700
            self.dash_timer = 0.2
            for i in range(random.randint(30, 50)):
                self.game.world.vfx.spawn_group('arrow_impact_sparks', self.owner.center.copy(), self.owner.aim_angle)

SKILLS = {
    'dagger': Dagger,
    'dash': Dash
}