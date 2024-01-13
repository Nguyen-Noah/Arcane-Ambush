import random
from .base_ai import BaseAI
from ..core_funcs import normalize

class SlimeAI(BaseAI):
    def init(self):
        self.allow_ai_movement = 1
        self.state = 'wander'           # WANDER OR PURSUIT

    def choose_new_target_pos(self):
        player = self.game.world.player

        start = self.parent.pos
        direction = (player.parent.pos[0] - self.pos[0], self.parent.pos[1] - self.pos[1])

    def set_target_position(self):
        self.target_position = self.choose_new_target_pos()
        self.arrived = False
        
    def wait(self):
        return 1 + random.random()
    
    def update(self, dt):
        if self.state == 'wander':
            pass
        else:
            pass