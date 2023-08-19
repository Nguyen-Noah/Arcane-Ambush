import pygame, math
from .camera import Camera
from .config import config
from .entities import EntityManager
from .tile_map import TileMap
from . import spritesheet_loader
from .hitboxes import Hitboxes
from .weapon_anim import WeaponAnimations
from .standalone_animations import StandaloneAnimations
from .particles import ParticleManager
from .vfx import VFX
import cProfile

class World:
    def __init__(self, game):
        self.game = game
        self.loaded = False
        self.collideables = []

    def load(self, map_id):
        self.tile_map = TileMap((16, 16), self.game.window.base_resolution)
        self.tile_map.load_map(map_id)

        self.weapon_animations = WeaponAnimations(self.game)
        self.world_animations = StandaloneAnimations(self.game)
        self.particles = ParticleManager(self.game)

        self.entities = EntityManager(self.game)
        self.player = self.entities.gen_player()

        self.camera = Camera(self.game)
        self.camera.set_restriction(self.player.pos)
        self.camera.set_tracked_entity(self.entities.player)

        self.hitboxes = Hitboxes(self.game)

        self.master_clock = 0

        #self.profiler = cProfile.Profile()

    def render(self, surf):
        if not self.loaded:
            self.loaded = True

        render_list = self.tile_map.get_visible(self.camera.true_pos)
        self.collideables = []
        self.render_list = []
        for layer in render_list:
            self.weapon_animations.render(surf, self.camera.pos)
            self.world_animations.render(surf, self.camera.pos)
            for tile in layer:
                offset = [-32, -32]
                if tile[1][0] in self.game.assets.spritesheet_data:
                    tile_id = str(tile[1][1]) + ';' + str(tile[1][2])
                    if tile_id in self.game.assets.spritesheet_data[tile[1][0]]:
                        if 'tile_offset' in self.game.assets.spritesheet_data[tile[1][0]][tile_id]:
                            offset = self.game.assets.spritesheet_data[tile[1][0]][tile_id]['tile_offset']
                img = spritesheet_loader.get_img(self.game.assets.spritesheets, tile[1])
                if tile[1][0] == 'obstacles':
                    self.collideables.append(self.obs_rect(tile, img))
                    pygame.draw.rect(surf, 'blue', (tile[0][0] + offset[0], tile[0][1] + offset[1], img.get_rect().x, img.get_rect().y), 1)
                    self.render_list.append([img, (tile[0][0] - self.camera.true_pos[0] + offset[0], tile[0][1] - self.camera.true_pos[1] + offset[1])])
                    #self.collideables.append(img.get_rect(topleft=(tile[0][0] + offset[0], tile[0][1] + offset[1])))
                else:
                    surf.blit(img, (math.floor(tile[0][0] - self.camera.true_pos[0] + offset[0]), math.floor(tile[0][1] - self.camera.true_pos[1] + offset[1])))

    def obs_rect(self, tile, img):
        # 0 -> big tree, 1 -> short tree, 2 -> alive bush, 3 -> stump, 4 -> fence, 5 -> log, 6 -> right-facing lamp, 7 -> down-facing lamp, 8 -> left-facing lamp, 9 -> broken lamp
        offset = config['obst_hitboxes']['level_0'][tile[1][1]]
        coord = (tile[0][0] - 32, tile[0][1] - 32)
        hitbox = (coord[0] - (offset[0] // 2) + offset[2], coord[1] - offset[1], img.get_rect().width + offset[0], img.get_rect().height + offset[1])
        pygame.draw.rect(self.game.window.display, 'red', (hitbox[0] - self.camera.true_pos[0], hitbox[1] - self.camera.true_pos[1], hitbox[2], hitbox[3]), 1)
        return pygame.Rect(hitbox)
        

    def update(self):
        self.camera.update()
        self.weapon_animations.update()
        self.world_animations.update()
        self.entities.spawn_entities()
        self.hitboxes.update()