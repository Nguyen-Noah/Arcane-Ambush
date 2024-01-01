from ..tower import Tower

class Asclepius(Tower):
    #healer
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt):
        super().update(dt)

        self.game.world.add_light_source(self.center[0], self.center[1], 0.8, 0.8, (246, 129, 129))

    def render(self, surf, offset):
        super().render(surf, offset)