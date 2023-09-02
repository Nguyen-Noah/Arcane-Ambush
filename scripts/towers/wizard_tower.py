import pygame
from ..tower import Tower

class WizardTower(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)