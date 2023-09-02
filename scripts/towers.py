from .tower import Tower
from .config import config

class Towers:
    def __init__(self, game):
        self.game = game
        self.towers = []

    def add(self, game, pos, size, type, rank):
        self.towers.append(Tower(game, pos, size, type, rank))

    def update(self):
        for tower in self.towers:
            tower.update()

    def render(self, surf, offset):
        for tower in self.towers:
            tower.render(surf, offset)