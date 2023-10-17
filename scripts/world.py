import pygame, math
from .core_funcs import round_nearest
from .camera import Camera
from .config import config
from .entities import EntityManager
from .towers import Towers
#from .tile_map import TileMap
from . import spritesheet_loader
from .hitboxes import Hitboxes
from .standalone_animations import StandaloneAnimations
from .particles import ParticleManager
from .builder_menu import Builder
from .vfx import VFX

class World:
    def __init__(self, game):
        self.game = game
        self.loaded = False
        self.collideables = []
        self.builder_mode = False
        self.show_builder_menu = False
        self.selected_tower = 'wizard_tower'

    def load(self, map_id):
        print(self.game.assets.maps)
        self.map = self.game.assets.maps[map_id]
        #self.tile_map = TileMap((16, 16), self.game.window.base_resolution)
        #self.tile_map.load_map(map_id)

        # polish ----------------------------------------------------------------------- #
        self.world_animations = StandaloneAnimations(self.game)
        self.particles = ParticleManager(self.game)
        self.vfx = VFX(self.game)

        # entities --------------------------------------------------------------------- #
        self.towers = Towers(self.game)
        self.entities = EntityManager(self.game)

        # player ----------------------------------------------------------------------- #
        self.player = self.entities.gen_player()

        # camera ----------------------------------------------------------------------- #
        self.camera = Camera(self.game)
        self.camera.set_restriction(self.player.pos)
        self.camera.set_tracked_entity(self.player)

        # hitboxes --------------------------------------------------------------------- #
        self.hitboxes = Hitboxes(self.game)

        # building --------------------------------------------------------------------- #
        self.builder_menu = Builder(self.game)

        self.master_clock = 0

    def render(self, surf):
        if not self.loaded:
            self.loaded = True

        self.collideables = []
        self.render_list = []

        surf.blit(self.map, (0 - self.camera.true_pos[0], 0 - self.camera.true_pos[1]))

        self.world_animations.render(surf, self.camera.pos)

        self.vfx.render_back(surf)
        self.towers.render(surf)
        self.vfx.render_front(surf)

    def obs_rect(self, tile, img):
        # 0 -> big tree, 1 -> short tree, 2 -> alive bush, 3 -> stump, 4 -> fence, 5 -> log, 6 -> right-facing lamp, 7 -> down-facing lamp, 8 -> left-facing lamp, 9 -> broken lamp
        offset = config['obst_hitboxes']['level_0'][tile[1][1]]
        coord = (tile[0][0] - 32, tile[0][1] - 32)
        hitbox = (coord[0] - (offset[0] // 2) + offset[2], coord[1] - offset[1], img.get_rect().width + offset[0], img.get_rect().height + offset[1])
        #pygame.draw.rect(self.game.window.display, 'red', (hitbox[0] - self.camera.true_pos[0], hitbox[1] - self.camera.true_pos[1], hitbox[2], hitbox[3]), 1)
        return pygame.Rect(hitbox)
        
    def update(self):
        self.camera.update()
        self.world_animations.update()
        self.vfx.update()
        self.towers.update()
        self.hitboxes.update()
        self.towers.update()
        self.entities.update()

        # builder mode handler -------------------------------------------------------- #
        if self.game.input.states['open_build_mode']:
            self.entities.render_entities = False
            self.game.input.hold_reset()
            self.camera.set_tracked_entity(None)
            self.builder_mode = True
            self.game.input.input_mode = 'builder'
            self.show_builder_menu = False
            self.towers.display_tower(self.selected_tower, 0, (round_nearest(self.player.get_mouse_pos()[0], 4), round_nearest(self.player.get_mouse_pos()[1], 4)))

        if self.game.input.states['close_build_mode']:
            self.entities.render_entities = True
            self.camera.set_tracked_entity(self.player)
            self.camera.mode = None
            self.builder_mode = False
            self.game.input.input_mode = 'core'
            self.towers.displayed_tower = None

        if self.builder_mode:
            self.game.window.add_freeze(0.0001, 0.1)
            self.player.weapon.invisible = 0.2

            if self.game.input.mouse_state['left_click']:
                self.towers.add(self.game, self.selected_tower, 0, (round_nearest(self.player.get_mouse_pos()[0], 4), round_nearest(self.player.get_mouse_pos()[1], 4)))

            if self.game.input.mouse_state['right_click']:
                self.show_builder_menu = not self.show_builder_menu