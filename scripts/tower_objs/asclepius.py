from ..tower import Tower

class Asclepius(Tower):
    #healer
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt):
        super().update(dt, color=(246, 129, 129))

    def render(self, surf, offset):
        super().render(surf, offset)