import pygame
from .config import config

class Builder:
    def __init__(self, game):
        self.game = game
        self.inventory_count = 3

    def add(self):
        pass

    def update(self):
        pass

    def render(self, surf):
        tilesize = 26
        for slot in range(self.inventory_count):
            pos = self.game.window.display.get_width() // 2 - self.inventory_count // 2 * tilesize + slot * tilesize
            surf.blit(self.game.assets.misc['builder_slot'], (pos, self.game.window.display.get_height() - tilesize))