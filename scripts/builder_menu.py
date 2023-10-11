import pygame
from .config import config

class Builder:
    def __init__(self, game):
        self.game = game
        self.selected_tower = None

    def update(self, tower):
        self.selected_tower = tower

    def render(self, surf):
        window_ratio = (self.game.window.base_resolution[0] // 4, self.game.window.base_resolution[1] // 4)
        pygame.draw.rect(surf, (93, 44, 40), (window_ratio[0], window_ratio[1], window_ratio[0] * 2, window_ratio[1] * 2))
        pygame.draw.rect(surf, (57, 31, 33), (window_ratio[0], window_ratio[1], window_ratio[0] * 2, window_ratio[1] * 2), 2)