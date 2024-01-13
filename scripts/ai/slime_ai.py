import random
from .base_ai import BaseAI
from ..core_funcs import get_dis

class SlimeAI(BaseAI):
    def init(self):
        self.allow_ai_movement = 1
        self.radius = 90
        self.state = 'wander'           # WANDER OR PURSUIT
        self.targeted_entity = self.game.world.player
        
    def wait(self):
        return 1 + random.random()
    
    def update(self, dt):
        if self.state == 'wander':
            dist = get_dis(self.parent.pos, self.targeted_entity.pos)
            if dist < self.radius:
                self.state = 'pursuit'
        else:
            print('pursuing')