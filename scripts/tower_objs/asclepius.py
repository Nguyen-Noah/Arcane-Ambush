from ..tower import Tower

class Asclepius(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, surf, offset):
        super().render(surf, offset)