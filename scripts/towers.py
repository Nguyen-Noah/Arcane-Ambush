from .tower import Tower
from .core_funcs import round_nearest
from .config import config

class Towers:
    def __init__(self, game):
        self.game = game
        self.towers = []
        self.displayed_tower = None
 
    def display_tower(self, game, pos, type, rank):
        self.displayed_tower = Tower(game, pos, type, rank)
        self.displayed_tower.set_opacity(128)

    def add(self, game, pos, type, rank):
        cost = config['towers'][type]['cost'][rank]
        if cost <= self.game.world.player.money:
            self.towers.append(Tower(game, pos, type, rank))
            self.game.world.player.money -= cost

    def update(self):
        for tower in self.towers:
            tower.update()

        if self.displayed_tower:
            self.displayed_tower.pos = (round_nearest(self.game.world.entities.player.get_mouse_pos()[0], 4), round_nearest(self.game.world.entities.player.get_mouse_pos()[1], 4))

    def render(self, surf):
        for tower in self.towers:
            tower.render(surf)
        
        if self.displayed_tower:
            self.displayed_tower.render(surf)