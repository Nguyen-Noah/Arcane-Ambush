import pygame, math

path = 'data/graphics/towers/'
colorkey = (0, 0, 0, 0)

def load_img(path, colorkey):
    img = pygame.image.load(path).convert()
    img.set_colorkey(colorkey)
    return img

class Tower:
    def __init__(self, game, pos, size, type, rank):
        self.game = game
        self.pos = list(pos).copy()
        self.size = size
        self.type = type
        self.rank = rank
        self.rotation = 0
        self.targeting = 'closest'
        self.shot_cooldown = 1
        self.shot_counter = 0
        self.shooting = True
        self.img = load_img(path + self.type + '/' + str(self.rank) + '.png', colorkey)

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

    def render(self, surf, offset):
        surf.blit(self.img, (self.pos[0] + self.size[1] // 1, self.pos[1] + self.size[1] // 1))