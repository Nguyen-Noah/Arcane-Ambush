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

    @property
    def rect(self):
        width, height = self.img.get_size()
        return pygame.Rect(self.pos[0] // 1, self.pos[1] // 1, width, height)

    @property
    def center(self):
        rect = self.img.get_rect()
        return ((self.pos[0] + rect[0] // 2) // 1, (self.pos[1] + rect[1] // 2) // 1)

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
        surf.blit(self.img, (self.pos[0] - offset[0] - (self.rect[2] // 2) // 1, self.pos[1] - offset[1] - (self.rect[3] // 2) // 1))