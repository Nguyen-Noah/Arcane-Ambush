import pygame, math
from ..tower import Tower
from ..core_funcs import colideRectLine
from ..ease_functions import easeInOutExpo

class Artemis(Tower):
    def __init__(self, *args, **kwargs):
        self.color = (200, 200, 50)
        super().__init__(*args, **kwargs)
        self.target_pos = None
        self.since_first_circle = 0
        self.second_circle_spawned = False
        self.shooting_counter = 1               # shoot the beam for 1 second
        self.beam_rect = pygame.Rect(self.center[0], self.center[1], 100, 100)
        self.shooting = False

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
        super().update(dt, color=(200, 200, 50))
        if self.hoverable:
            # idle time
            # self.attack_timer being incremented in parent Tower class
            #print(self.attack_timer)
            if self.attack_timer >= self.attack_cd:
                # spawn the first vfx circle
                if not self.since_first_circle:
                    self.game.world.vfx.spawn_vfx('circle', self.center, 170, 10, 150, reverse=True, ease=easeInOutExpo)
                
                # once 0.5 seconds passed since the first circle, start the second one
                self.since_first_circle += dt
                if self.since_first_circle >= 0.5:
                    if not self.second_circle_spawned:
                        self.game.world.vfx.spawn_vfx('circle', self.center, 150, 10, 150, reverse=True, ease=easeInOutExpo)
                        self.second_circle_spawned = True
                        self.circle_status = self.game.world.vfx.get_last()

                    # once the last circle is gone, shoot the beam
                    if not self.circle_status.alive:
                        self.shooting = True
                        self.shooting_counter -= dt
                        if self.shooting_counter <= 0:
                            self.shooting = False
                            self.shooting_counter = 1
                            self.attack_timer = 0
                            self.since_first_circle = 0
                            self.second_circle_spawned = False
                        #print('BVVVV')

    def render(self, surf, offset=[0, 0]):
        super().render(surf, offset)
        #if self.shooting:
        pygame.draw.line(self.game.window.display, 'red', (self.center[0] - offset[0], self.center[1] - offset[1]), (self.targeted_entity.center[0] - offset[0], self.targeted_entity.center[1] - offset[1]), 1)