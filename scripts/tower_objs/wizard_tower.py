import pygame, math
from ..core_funcs import load_img
from ..tower import Tower

path = 'data/graphics/towers/'
colorkey = (0, 0, 0, 0)

class WizardTower(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orb_img = load_img(path + self.type + '/' + str(self.rank) + '_orb.png', colorkey)
        self.frame = 0

    def render_orb(self, surf):
        surf.blit(self.orb_img, (self.center[0] - (self.orb_img.get_size()[0] // 2), self.center[1] - (self.orb_img.get_size()[1] // 2) + math.sin(self.frame * 0.005) - 5))

    def update(self):
        super().update()
        self.frame += 1

    def render(self, surf):
        super().render(surf)
        self.render_orb(surf)