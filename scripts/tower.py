import pygame, math
from .config import config
from .core_funcs import get_dis

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
        self.radius = config['towers'][self.type]['radius']
        self.rotation = 0
        self.targeting = 'closest'
        self.targeted_entity = None
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
        return (self.pos[0] - self.game.world.camera.true_pos[0] // 1, self.pos[1] - self.game.world.camera.true_pos[1] // 1)

    def in_radius(self):
        entity_list = self.game.world.entities.entities
        entities = []

        for entity in entity_list:
            if entity.category == 'enemy':
                dist = get_dis(self.center, (entity.center[0] - self.game.world.camera.true_pos[0], entity.center[1] - self.game.world.camera.true_pos[1]))
                if dist <= self.radius:
                    entities.append(entity)
            
        return entities

    def target_first(self):
        #TODO: create algorithm to find first, closest, farthest, and strongest enemy
        entity_list = self.in_radius()

        for entity in entity_list:
            if not self.targeted_entity or self.targeted_entity not in entity_list:
                self.targeted_entity = entity
            else:
                if entity.age > self.targeted_entity.age:
                    self.targeted_entity = entity
            pygame.draw.line(self.game.window.display, 'red', self.center, (self.targeted_entity.center[0] - self.game.world.camera.true_pos[0], self.targeted_entity.center[1] - self.game.world.camera.true_pos[1]))
    
    def target_closest(self):
        entity_list = self.in_radius()

        for entity in entity_list:
            dist = get_dis(self.center, (entity.center[0] - self.game.world.camera.true_pos[0], entity.center[1] - self.game.world.camera.true_pos[1]))
            if not self.targeted_entity or self.targeted_entity not in entity_list:
                self.targeted_entity = entity
            else:
                if dist < get_dis(self.center, (self.targeted_entity.center[0] - self.game.world.camera.true_pos[0], self.targeted_entity.center[1] - self.game.world.camera.true_pos[1])):
                    self.targeted_entity = entity
            pygame.draw.line(self.game.window.display, 'red', self.center, (self.targeted_entity.center[0] - self.game.world.camera.true_pos[0], self.targeted_entity.center[1] - self.game.world.camera.true_pos[1]))
                

    def target_farthest(self):
        entity_list = self.in_radius()

        for entity in entity_list:
            dist = get_dis(self.center, (entity.center[0] - self.game.world.camera.true_pos[0], entity.center[1] - self.game.world.camera.true_pos[1]))
            if not self.targeted_entity or self.targeted_entity not in entity_list:
                self.targeted_entity = entity
            else:
                if dist > get_dis(self.center, (self.targeted_entity.center[0] - self.game.world.camera.true_pos[0], self.targeted_entity.center[1] - self.game.world.camera.true_pos[1])):
                    self.targeted_entity = entity
            pygame.draw.line(self.game.window.display, 'red', self.center, (self.targeted_entity.center[0] - self.game.world.camera.true_pos[0], self.targeted_entity.center[1] - self.game.world.camera.true_pos[1]))

    def target_strongest(self):
        entity_list = self.in_radius()

        for entity in entity_list:
            if not self.targeted_entity or self.targeted_entity not in entity_list:
                self.targeted_entity = entity
            else:
                if config['entities'][self.targeted_entity.type]['rank'] < config['entities'][entity.type]['rank']:
                    self.targeted_entity = entity
            pygame.draw.line(self.game.window.display, 'red', self.center, (self.targeted_entity.center[0] - self.game.world.camera.true_pos[0], self.targeted_entity.center[1] - self.game.world.camera.true_pos[1]))

    def target_weakest(self):
        entity_list = self.game.world.entities.entities

    def allow_shot(self):
        if self.shooting:
            self.shot_counter += self.game.window.dt
            if self.shot_counter >= self.shot_cooldown:
                self.shooting = False

    def show_radius(self, surf):
        pygame.draw.circle(surf, 'white', self.center, self.radius, width=1)

    def update(self):
        pass

    def render(self, surf):
        self.show_radius(surf)
        surf.blit(self.img, (self.center[0] - (self.rect[2] // 2), self.center[1] - (self.rect[3] // 2)))
        self.target_strongest()
        #print(self.targeted_entity)