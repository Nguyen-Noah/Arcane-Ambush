import pygame, math

class Tower:
    def __init__(self, game, pos, type):
        self.game = game
        self.pos = list(pos).copy()
        self.type = type
        self.rotation = 0
        self.targetted = 'closest'
        self.shot_cooldown = 1
        self.shot_counter = 0
        self.shooting = True
        
    def target_enemy(self):
        #TODO: create algorithm to find closest, farthest, and strongest enemy
        entity_list = self.game.world.entities
        for entity in entity_list:
            pass

    def allow_shot(self):
        if self.shooting:
            self.shot_counter += self.game.window.dt
            if self.shot_counter >= self.shot_cooldown:
                self.shooting = False

    def update(self):
        pass

    def render(self):
        pass