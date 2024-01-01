from ..tower import Tower

class Aether(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt):
        super().update(dt, color=(205, 180, 20))

    def render(self, surf, offset):
        super().render(surf, offset)