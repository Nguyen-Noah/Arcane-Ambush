from ..tower import Tower

class Archer(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, surf):
        super().render(surf)