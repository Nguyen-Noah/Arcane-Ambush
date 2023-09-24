import pygame, math
from .core_funcs import load_img
from .config import config
from .core_funcs import get_dis
from .projectiles import Projectile

path = 'data/graphics/towers/'
colorkey = (0, 0, 0, 0)

class Tower:
    def __init__(self, game, pos, type, rank):
        self.game = game
        self.pos = list(pos).copy()
        self.type = type
        self.rank = rank
        self.radius = config['towers'][self.type]['radius']
        self.rotation = 0
        self.targeting = 'closest'
        self.targeted_entity = None
        self.attack_timer = 0
        self.shooting = True
        self.img = load_img(path + self.type + '/' + str(self.rank) + '.png', colorkey)
        
        self.gen_mask()

    @property
    def rect(self):
        width, height = self.img.get_size()
        return pygame.Rect(self.pos[0] // 1, self.pos[1] // 1, width, height)

    @property
    def center(self):
        return (self.pos[0] - self.game.world.camera.true_pos[0] // 1, self.pos[1] - self.game.world.camera.true_pos[1] // 1)

    def set_opacity(self, opacity):
        self.img.set_alpha(opacity)

    def gen_mask(self):
        self.mask = pygame.mask.from_surface(self.img)

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
        entity_list = self.in_radius()

        if len(entity_list) == 0:
            self.targeted_entity = None

        for entity in reversed(entity_list):
            if not self.targeted_entity or self.targeted_entity:
                self.targeted_entity = entity

    def target_closest(self):
        entity_list = self.in_radius()

        if len(entity_list) == 0:
            self.targeted_entity = None

        for entity in entity_list:
            dist = get_dis(self.center, (entity.center[0] - self.game.world.camera.true_pos[0], entity.center[1] - self.game.world.camera.true_pos[1]))
            if not self.targeted_entity or self.targeted_entity not in entity_list or not entity_list:
                self.targeted_entity = entity
            else:
                if dist < get_dis(self.center, (self.targeted_entity.center[0] - self.game.world.camera.true_pos[0], self.targeted_entity.center[1] - self.game.world.camera.true_pos[1])):
                    self.targeted_entity = entity         

    def target_farthest(self):
        entity_list = self.in_radius()

        if len(entity_list) == 0:
            self.targeted_entity = None

        for entity in entity_list:
            dist = get_dis(self.center, (entity.center[0] - self.game.world.camera.true_pos[0], entity.center[1] - self.game.world.camera.true_pos[1]))
            if not self.targeted_entity or self.targeted_entity not in entity_list:
                self.targeted_entity = entity
            else:
                if dist > get_dis(self.center, (self.targeted_entity.center[0] - self.game.world.camera.true_pos[0], self.targeted_entity.center[1] - self.game.world.camera.true_pos[1])):
                    self.targeted_entity = entity

    def target_strongest(self):
        entity_list = self.in_radius()

        if len(entity_list) == 0:
            self.targeted_entity = None

        for entity in entity_list:
            if not self.targeted_entity or self.targeted_entity not in entity_list:
                self.targeted_entity = entity
            else:
                if config['entities'][self.targeted_entity.type]['rank'] < config['entities'][entity.type]['rank']:
                    self.targeted_entity = entity

    def target_weakest(self):
        entity_list = self.in_radius()

        if len(entity_list) == 0:
            self.targeted_entity = None

        for entity in entity_list:
            if not self.targeted_entity or self.targeted_entity not in entity_list:
                self.targeted_entity = entity
            else:
                if config['entities'][self.targeted_entity.type]['rank'] > config['entities'][entity.type]['rank']:
                    self.targeted_entity = entity

    def show_radius(self, surf):
        pygame.draw.circle(surf, 'white', self.center, self.radius, width=1)

        target_rect = pygame.Rect(self.center, (0, 0)).inflate((self.radius * 2, self.radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        shape_surf.set_alpha(64)
        pygame.draw.circle(shape_surf, 'white', (self.radius, self.radius), self.radius)
        surf.blit(shape_surf, target_rect)

    def outline(self, surf, loc):
        cursor_mask = pygame.mask.from_surface(self.game.window.cursor)
        cursor_offset = self.game.world.entities.player.get_mouse_pos()
        if self.mask.overlap(cursor_mask, (cursor_offset[0] - (self.pos[0] - (self.rect[2] // 2)), cursor_offset[1] - (self.pos[1] - (self.rect[3] // 2)))):
            self.show_radius(surf)
            if not self.game.world.builder_mode:
                mask = pygame.mask.from_surface(self.img)
                mask_outline = mask.outline()
                mask_surf = pygame.Surface(self.img.get_size())
                for pixel in mask_outline:
                    mask_surf.set_at(pixel, (255, 255, 255))
                mask_surf.set_colorkey((0, 0, 0))
                surf.blit(mask_surf, (loc[0] - 1, loc[1]))
                surf.blit(mask_surf, (loc[0] + 1, loc[1]))
                surf.blit(mask_surf, (loc[0], loc[1] - 1))
                surf.blit(mask_surf, (loc[0], loc[1] + 1))

    def update(self):
        self.target_weakest()
        if self.targeted_entity:
            self.attack_timer -= self.game.window.dt

            if self.attack_timer < 0:
                angle = math.atan2(self.targeted_entity.center[1] - (self.center[1] + self.game.world.camera.true_pos[1]), self.targeted_entity.center[0] - (self.center[0] + self.game.world.camera.true_pos[0]))
                self.game.world.entities.projectiles.append(Projectile(self.type + '_projectile', (self.center[0] + self.game.world.camera.true_pos[0], self.center[1] + self.game.world.camera.true_pos[1]), angle, 50, self.game, self))
                self.attack_timer = 1.5

    def render(self, surf):
        self.outline(surf, (self.center[0] - (self.rect[2] // 2), self.center[1] - (self.rect[3] // 2)))
        surf.blit(self.img, (self.center[0] - (self.rect[2] // 2), self.center[1] - (self.rect[3] // 2)))
        if self.targeted_entity:
            pygame.draw.line(self.game.window.display, 'red', self.center, (self.targeted_entity.center[0] - self.game.world.camera.true_pos[0], self.targeted_entity.center[1] - self.game.world.camera.true_pos[1]))
