import pygame, math
from .core_funcs import load_img
from .config import config
from .core_funcs import get_dis
from .projectiles import Projectile
from .quadtree import Circle

path = 'data/graphics/towers/'
colorkey = (0, 0, 0, 0)

class Tower:
    def __init__(self, game, type, rank, pos=(0, 0), hoverable=True):
        self.game = game
        self.pos = list(pos).copy()
        self.type = type
        self.rank = rank
        self.hoverable = hoverable
        self.radius = config['towers'][self.type]['radius']
        self.player_skill = config['towers'][self.type]['player_skill']
        self.rotation = 0
        self.targeting = 'closest'
        self.targeted_entity = None
        self.attack_timer = 0
        self.shooting = True
        self.img = load_img(path + self.type + '/' + str(self.rank) + '.png', colorkey)
        
        self.gen_mask()

    @property
    def rect(self):
        if self.hoverable:
            width, height = self.img.get_size()
            # add 8 to the rect value to allow y-overlapping
            return pygame.Rect((self.pos[0] - width // 2) - self.game.world.camera.true_pos[0] // 1, (self.pos[1] - height // 2) - self.game.world.camera.true_pos[1] + 8 // 1, width, height - 8)
        else:
            width, height = self.img.get_size()
            return pygame.Rect((self.pos[0] - width // 2) - self.game.world.camera.true_pos[0] // 1, (self.pos[1] - height // 2) - self.game.world.camera.true_pos[1] // 1, width, height)

    @property
    def center(self):
        return self.pos

    def set_opacity(self, opacity):
        self.img.set_alpha(opacity)

    def gen_mask(self):
        if self.hoverable:
            self.mask = pygame.mask.from_surface(self.img)
        else:
            self.mask = pygame.mask.Mask((self.rect[2], self.rect[3]))
            self.mask.fill()

    def in_radius(self):
        entity_list = self.game.world.entities.entities
        entities = []

        for entity in entity_list:
            if entity.category == 'enemy':
                dist = get_dis(self.center, entity.center)
                if dist <= self.radius:
                    entities.append(entity)
            
        return entities

    def print_hitbox(self):
        pygame.draw.rect(self.game.window.display, 'blue', self.rect, 1)

    def target_closest(self, offset=(0, 0)):
        entity_list = self.in_radius()

        if len(entity_list) == 0:
            self.targeted_entity = None

        for entity in entity_list:
            dist = get_dis((self.center[0], self.center[1]), (entity.center[0], entity.center[1]))
            if not self.targeted_entity or self.targeted_entity not in entity_list:
                self.targeted_entity = entity
            else:
                if not self.targeted_entity.targetable:
                    if dist < get_dis(self.center, self.targeted_entity.center):
                        self.targeted_entity = entity         

    def target(self):
        cir = Circle(self.center, self.radius)
        entity_list = self.game.world.quadtree.query_range(Circle(self.center, self.radius))
        
        #self.targeted_entity = self.game.world.quadtree.query_closest(cir, self.center)
        cir.draw(self.game.window.display, self.game.world.camera.true_pos)

    def show_radius(self, surf, offset=(0, 0)):
        pygame.draw.circle(surf, 'white', (self.center[0] - offset[0], self.center[1] - offset[1]), self.radius, width=1)

        target_rect = pygame.Rect((self.center[0] - offset[0], self.center[1] - offset[1]), (0, 0)).inflate((self.radius * 2, self.radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        shape_surf.set_alpha(64)
        pygame.draw.circle(shape_surf, 'white', (self.radius, self.radius), self.radius)
        surf.blit(shape_surf, target_rect)

    def tower_hover(self):
        cursor_mask = pygame.mask.from_surface(self.game.window.cursor)
        cursor_offset = self.game.input.get_mouse_pos()
        if self.mask.overlap(cursor_mask, (cursor_offset[0] - (self.pos[0] - (self.rect[2] // 2)), cursor_offset[1] - (self.pos[1] - (self.rect[3] // 2)))):
            return self

    def outline(self, surf, loc):
        cursor_mask = pygame.mask.from_surface(self.game.window.cursor)
        cursor_offset = self.game.input.get_mouse_pos()
        if self.mask.overlap(cursor_mask, (cursor_offset[0] - (self.pos[0] - (self.rect[2] // 2)), cursor_offset[1] - (self.pos[1] - (self.rect[3] // 2)))):
            self.show_radius(surf, self.game.world.camera.true_pos)
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
        offset = self.game.world.camera.true_pos
        if self.hoverable:
            #self.target_closest(offset)
            self.target()
            if self.targeted_entity:
                self.attack_timer -= self.game.window.dt

                if self.attack_timer < 0:
                    angle = math.atan2(self.targeted_entity.center[1] - self.center[1], self.targeted_entity.center[0] - self.center[0])
                    self.game.world.entities.projectiles.append(Projectile(self.type + '_projectile', self.center, angle, 50, self.game, self))
                    self.attack_timer = 1.5
            self.print_hitbox()

    def render(self, surf, offset=(0, 0)):
        if self.hoverable:
            self.outline(surf, (self.center[0] - (self.rect[2] // 2) - offset[0], self.center[1] - (self.rect[3] // 2) - offset[1]))

        surf.blit(self.img, (self.center[0] - (self.rect[2] // 2) - offset[0], self.center[1] - (self.rect[3] // 2) - offset[1]))
        
        if self.targeted_entity:
            pygame.draw.line(self.game.window.display, 'red', (self.center[0] - offset[0], self.center[1] - offset[1]), (self.targeted_entity.center[0] - offset[0], self.targeted_entity.center[1] - offset[1]))
