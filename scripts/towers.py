from .core_funcs import round_nearest
from .config import config
from .tower_map import tower_map

class Towers:
    def __init__(self, game):
        self.game = game
        self.towers = []
        self.inventory_towers = []
        self.displayed_tower = None
<<<<<<< HEAD
<<<<<<< HEAD

        for tower in tower_map:
            self.inventory_towers.append(tower_map[tower](self.game, tower, 0, hoverable=False))
=======
>>>>>>> dd66f4a1204550f902eef134d5e08600cb6aa5c0
=======

        for tower in tower_map:
            self.inventory_towers.append(tower_map[tower](self.game, tower, 0))
>>>>>>> parent of dd66f4a (rollback to previous spawning system)
 
    def display_tower(self, type, rank, pos):
        self.displayed_tower = tower_map[type](self.game, type, rank, pos)
        self.displayed_tower.set_opacity(128)

    def add(self, game, type, rank, pos):
        cost = config['towers'][type]['cost'][rank]
        if cost <= self.game.world.player.money:
            self.towers.append(tower_map[type](game, type, rank, pos))
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