from .slime import Slime

class MegaSlime(Slime):
    def __init__(self, *args):
        super().__init__(*args)
        
    def update(self, dt):
        super().update(dt)