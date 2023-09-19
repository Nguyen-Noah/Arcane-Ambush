from .tower import Tower
from .config import config

class Towers:
    def __init__(self, game):
        self.game = game
        self.towers = []

    def add(self, game, pos, size, type, rank):
        cost = config['towers'][type]['cost'][rank]
        if cost <= self.game.world.player.money:
            self.towers.append(Tower(game, pos, size, type, rank))
            self.game.world.player.money -= cost

    def update(self):
        for tower in self.towers:
            tower.update()

    def render(self, surf):
        for tower in self.towers:
            tower.render(surf)