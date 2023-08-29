from .slime import Slime

class MegaSlime(Slime):
    def __init__(self, *args):
        super().__init__(*args)
        
    def update(self, dt):
        r = super().update(dt)

        if not r:
            return r

        return self.alive