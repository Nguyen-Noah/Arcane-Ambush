import math
from ..entity import Entity

class Slime(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = 'enemy'
        self.velocity = [0, 0]
        self.size = (14, 14)
        self.anim_offset = [0, 0]

    def update(self, dt):
        self.frame_motion = self.velocity.copy()
        r = super().update(dt)
        if not r:
            return r

        #if self.game.input.mouse_state['right_click']:
            #self.active_animation.paused = not self.active_animation.paused

        print(self.anim_offset)

        return self.alive

    def render(self, surf, offset):
        super().render(surf, offset, self.anim_offset)