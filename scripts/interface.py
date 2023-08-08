import pygame
from .config import config
from .builder import Builder
from .inventory import Inventory

class Interface:
    def __init__(self, game):
        self.game = game
        self.inventory = Inventory(self.game)
        self.builder = Builder(self.game)
        self.mode = 'inventory'

    def swap(self):
        if self.mode == 'builder':
            self.mode = 'inventory'
        else:
            self.mode = 'builder'

    def update(self):
        self.inventory.update()
        self.builder.update()

    def render(self, surf):
        if self.game.input.states['swap_inventory']:
            self.swap()

        if self.mode == 'inventory':
            self.inventory.render(surf)
        elif self.mode == 'builder':
            self.builder.render(surf)