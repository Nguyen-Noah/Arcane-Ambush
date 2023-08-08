import pygame, math

class Tower:
    def __init__(self, game, pos, type):
        self.game = game
        self.pos = pos
        self.type = type
        self.rotation = 0
        self.centered = False

    @property
    def rect(self):
        if not self.centered:
            return pygame.Rect(self.pos[0] // 1, self.pos[1] // 1, self.size[0], self.size[1])
        else:
            return pygame.Rect((self.pos[0] - self.size[0] // 2) // 1, (self.pos[1] - self.size[1] // 2))
        
    def update(self):
        pass

    def render(self):
        pass