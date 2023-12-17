import pygame
from ..tower import Tower

class Archer(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.targeted_entity = self.game.world.player
        self.target_pos = None
        self.charging = 1

    def update(self, dt):
        if self.hoverable:
            self.attack_timer += dt
            if self.target_pos:
                self.charging -= dt
                print('charging')
            else:
                if self.attack_timer >= self.attack_cd:
                    self.target_pos = self.targeted_entity.pos.copy()
                    self.attack_timer = 0
            if self.charging <= 0:
                pygame.draw.circle(self.game.window.display, 'white', (self.target_pos[0] - self.game.world.camera.true_pos[0], self.target_pos[1] - self.game.world.camera.true_pos[1]), 20)
                self.target_pos = None
                self.charging = 1
                print('shoot')

    def render(self, surf, offset):
        super().render(surf, offset)