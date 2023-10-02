import pygame
from .config import config

class Builder:
    def __init__(self, game):
        self.game = game

    def render(self, surf):
        display = self.game.window.display
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, self.game.window.base_resolution[0], self.game.window.base_resolution[1]))