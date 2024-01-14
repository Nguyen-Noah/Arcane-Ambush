import math, random
from .base_ai import BaseAI
from ..core_funcs import get_dis, get_target_dist

class SlimeAI(BaseAI):
    def init(self):
        self.allow_ai_movement = 1
        self.radius = 90
        self.state = 'wander'           # WANDER OR PURSUIT
        self.targeted_entity = self.game.world.player
        self.target_pos = self.parent.home.copy()
        self.wait_time = self.wait(1)
        self.jump_vector = [0, 0]
        self.jump_timer = 0.5
        self.interest_timer = 2             # timer for how long it takes for the slime to lose interest and go back to wandering
        
    def choose_new_wander_pos(self):
        angle = math.radians(random.randint(0, 360))
        distance = 60
        target = [self.parent.home[0] + (math.cos(angle) * distance), self.parent.home[1] + (math.sin(angle) * distance)]
        self.jump_vector = get_target_dist(self.parent.pos, target)
        self.parent.flip[0] = True if self.jump_vector[0] < 0 else False
    
    def get_target_pos(self):
        self.jump_vector = get_target_dist(self.parent.pos, self.targeted_entity.pos)
        self.parent.flip[0] = True if self.jump_vector[0] < 0 else False

    def wait(self, min):
        return min + random.random()
    
    def update(self, dt):
        if self.state == 'wander':
            # the parent finished the random movement, pick another after a short delay and pick a new wander position
            if not any(self.jump_vector):
                # only allow pursuit if the entity is done moving
                dist = get_dis(self.parent.pos, self.targeted_entity.pos)
                if dist < self.radius:
                    self.state = 'pursuit'

                if self.wait_time >= 0:
                    self.wait_time -= dt
                else:
                    self.parent.anim_offset = [0, 0]
                    self.choose_new_wander_pos()
                    self.wait_time = self.wait(1)
        else:
            # switch back to wandering if out of radius for 2 seconds
            dist = get_dis(self.parent.pos, self.targeted_entity.pos)
            if dist > self.radius:
                self.interest_timer -= dt
                if self.interest_timer <= 0:
                    self.state = 'wander'
                    self.interest_timer = 2
            
            if not any(self.jump_vector):
                if self.wait_time >= 0:
                    self.wait_time -= dt
                else:
                    self.parent.anim_offset = [0, 0]
                    self.get_target_pos()
                    self.wait_time = self.wait(0.2)

        if any(self.jump_vector) and int(self.parent.active_animation.frame) == 5:
            self.parent.move((self.jump_vector[0] * self.parent.speed * dt, self.jump_vector[1] * self.parent.speed * dt), self.game.world.collideables)
            self.parent.active_animation.paused = True
            self.jump_timer -= dt
            if self.jump_timer <= 0:
                self.jump_vector = [0, 0]
                self.parent.active_animation.paused = False
                self.jump_timer = 0.5

            if self.jump_timer > 0.5 / 2:
                self.parent.anim_offset[1] += 0.1
            else:
                self.parent.anim_offset[1] -= 0.1