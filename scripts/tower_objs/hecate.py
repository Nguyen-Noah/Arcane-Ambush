from ..tower import Tower

class Hecate(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt):
        super().update(dt)

    def render(self, surf, offset):
        super().render(surf, offset)