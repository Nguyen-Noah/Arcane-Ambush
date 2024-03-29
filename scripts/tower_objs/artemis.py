import pygame, math, random
from ..tower import Tower
from ..core_funcs import colideRectLine, pivot_rotate
from ..ease_functions import easeInOutExpo

class Artemis(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_pos = None
        self.since_first_circle = 0
        self.second_circle_spawned = False
        self.shooting_counter = 100               # shoot the beam for 1 second
        self.beam_rect = pygame.Rect(self.center[0], self.center[1], 100, 100)
        self.shooting = False
        self.beam_angle = 0
        self.beam_delay = 0.9
        self.beam_calculated = False
        self.true_pos = [0, 0]
        self.beam_img = self.game.assets.projectiles['artemis_beam']

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
                # spawn the first vfx circle
                if not self.since_first_circle:
                    self.game.world.vfx.spawn_vfx('circle', self.center, 170, 10, 150, reverse=True, ease=easeInOutExpo)
                
                # once 0.5 seconds passed since the first circle, start the second one
                self.since_first_circle += dt
                if self.since_first_circle >= 0.5:
                    if not self.second_circle_spawned:
                        self.beam_angle = self.rotation             # get the beam angle once the second circle is spawned
                        self.game.world.vfx.spawn_vfx('circle', self.center, 150, 10, 150, reverse=True, ease=easeInOutExpo)
                        self.second_circle_spawned = True

                    self.beam_delay -= dt
                    if self.beam_delay <= 0:
                        # SHOOTING
                        self.shooting = True
                        self.shooting_counter -= dt
                        angle = self.beam_angle + random.random() * math.pi / 8
                        vfx_color = (random.randint(0, 100), random.randint(0, 127), 255)

                        if random.randint(1, 20) == 1:
                            self.game.world.vfx.spawn_group('aether_sparks', self.center, angle + math.pi, color=vfx_color)

                        self.game.world.camera.add_screen_shake(1, 'light')

                        if self.shooting_counter <= 0:
                            # resetting everything
                            self.shooting = False
                            self.shooting_counter = 1
                            self.attack_timer = 0
                            self.since_first_circle = 0
                            self.second_circle_spawned = False
                            self.beam_delay = 0.9
                            self.beam_angle = 0
                            self.beam_calculated = False

    def render(self, surf, offset=[0, 0]):
        super().render(surf, offset)
        if self.beam_angle != 0 and self.beam_delay > 0:
            beam_surf = pygame.Surface(self.game.window.base_resolution)
            beam_surf.fill((0, 0, 0))
            beam_surf.set_colorkey((0, 0, 0))
            beam_surf.set_alpha(255 * (1 - self.beam_delay))
            endpoint = (self.center[0] - offset[0] + (math.cos(self.beam_angle) * 300), self.center[1] - offset[1] + (math.sin(self.beam_angle) * 300))
            pygame.draw.line(beam_surf, 'red', (self.center[0] - offset[0], self.center[1] - offset[1]), endpoint, int(3 * (1 - self.beam_delay)))
            surf.blit(beam_surf, (0, 0))

        # MAKE THIS ONLY CALCULATE ONCE
        if self.shooting:
            if self.beam_calculated:
                surf.blit(self.beam_img, (self.true_pos[0] - offset[0], self.true_pos[1] - offset[1]))
            else:
                self.beam_img, pos = pivot_rotate(self.beam_img, math.degrees(self.beam_angle), self.center, pygame.math.Vector2(self.beam_img.get_width() // 2, 0))
                self.game.world.hitboxes.add_hitbox(self.game, 'artemis', duration=self.shooting_counter, rect=self.beam_img, owner=self, angle=self.beam_angle, offset=pos)
                self.beam_calculated = True
                self.true_pos = pos