import pygame
from .config import config

class Inventory:
    def __init__(self, game):
        self.game = game
        self.max_slots = 9
        self.inventory_count = 3

    def add(self):
        if self.inventory_count < self.max_slots:
            self.inventory_count += 1

    def update(self):
        if self.game.input.mouse_state['right_click']:
            self.add()

    def render(self, surf):
        tilesize = 18

        for i in range(self.inventory_count):
            if self.inventory_count % 2 == 0:
                pos = self.game.window.display.get_width() // 2 - self.inventory_count // 2 + (i - self.inventory_count // 2 + 0.5) * tilesize
            else:
                pos = self.game.window.display.get_width() // 2 - self.inventory_count // 2 * tilesize + i * tilesize
            surf.blit(self.game.assets.misc['inventory_slot'], (pos, self.game.window.display.get_height() - tilesize))