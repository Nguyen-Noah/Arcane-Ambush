import math
from ..core_funcs import load_img
from ..tower import Tower

path = 'data/graphics/towers/'
colorkey = (0, 0, 0, 0)

class WizardTower(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orb_img = load_img(path + self.type + '/' + str(self.rank) + '_orb.png', colorkey)
        self.frame = 0

    def render_orb(self, surf, offset):
        y_offset = 0 if self.hoverable else 4
        surf.blit(self.orb_img, (self.center[0] - (self.orb_img.get_size()[0] // 2) - offset[0], self.center[1] - (self.orb_img.get_size()[1] // 2 - 4) + math.sin(self.frame * 0.005) - 5 - y_offset - offset[1]))

    def update(self, dt):
        super().update(dt)
        self.frame += 1

    def render(self, surf, offset):
        super().render(surf, offset)
        self.render_orb(surf, offset)