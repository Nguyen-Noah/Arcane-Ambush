import pygame
from ..tower import Tower
from ..core_funcs import colideRectLine
from ..ease_functions import easeInOutExpo

class Artemis(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.targeted_entity = self.game.world.player
        self.target_pos = None
        self.circle_spawned = False
        self.charging = 1

        """
        1. set the target to the player
        2. IDLE time to increment attack_timer (done in the Tower class)
        3. once attack_timer >= attack_cooldown, have the tower charge up using the charging var
            - this is when the charge up animation is played
        4. shoot the beam
            - a self.shooting variable is needed to count how long the beam is shot
        5. once done, reset all variables
        """

    def update(self, dt):
        super().update(dt)
        if self.hoverable:
            # idle time
            # self.attack_timer being incremented in parent Tower class
            #print(self.attack_timer)
            if self.attack_timer >= self.attack_cd:
                self.charging -= dt
                if not self.circle_spawned:
                    self.game.world.vfx.spawn_vfx('circle', self.center, 120, 10, 8, 100, reverse=True, ease=easeInOutExpo)
                    self.circle_spawned = True
                    self.circle_status = self.game.world.vfx.get_last()
                #print(self.circle_status)
            """ if self.target_pos:
                self.charging -= dt
                #print('charging')
            else:
                if self.attack_timer >= self.attack_cd:
                    self.target_pos = self.targeted_entity.pos.copy()
                    self.attack_timer = 0
            if self.charging <= 0:
                pygame.draw.circle(self.game.window.display, 'white', (self.target_pos[0] - self.game.world.camera.true_pos[0], self.target_pos[1] - self.game.world.camera.true_pos[1]), 20)
                self.target_pos = None
                self.charging = 1
                #print('shoot') """
        
        self.game.world.add_light_source(self.center[0], self.center[1], 0.8, 0.4, (200, 200, 50))

    def render(self, surf, offset):
        super().render(surf, offset)