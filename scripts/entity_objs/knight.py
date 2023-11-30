from ..entity import Entity

class Knight(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.category = 'enemy'
        self.velocity = [0, 0]
        self.size = (14, 14)
        self.movement_counter = [0, 0]
        self.current_index = 0
        self.direction = 'down'
        self.set_action('walk', self.direction)

    def update(self, dt):
        r = super().update(dt)

        if not r:
            return r
        else:
            self.movement = self.get_target_distance(self.game.world.player)
            self.move(self.movement, self.game.world.collideables)

        return self.alive