import pygame, math

class Hitbox:
    def __init__(self, game):
        self.game = game

    def update(self):
        pass

class Hitboxes:
    def __init__(self, game):
        self.game = game
        self.hitboxes = []
    
    def add(self):
        self.hitboxes.append(Hitbox(self.game))

    def update(self):
        for i, hitbox in enumerate(self.hitboxes):
            alive = hitbox.update()
            if not alive:
                self.hitboxes.pop(i)