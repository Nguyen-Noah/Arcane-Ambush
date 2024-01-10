import pygame, math, random
from .core_funcs import import_csv_layout, normalize_color
from .camera import Camera
from .config import config
from .entities import EntityManager
from .towers import Towers
from .hitboxes import Hitboxes
from .standalone_animations import StandaloneAnimations
from .destruction_particles import DestructionParticles
from .weapon_anims import WeaponAnimations
from .particles import ParticleManager
from .builder_menu import Builder
from .vfx import VFX, set_glow_surf
from .ease_functions import easeInExpo, easeInOutExpo
from .lights import Lights

from .quadtree import QuadTree, Rectangle

class World:
    def __init__(self, game):
        self.game = game
        self.loaded = False
        self.collideables = []
        self.builder_mode = False
        self.show_builder_menu = False
        self.world_timer = 0

    def load(self, map_id):
        self.map_id = map_id
        self.floor = self.game.assets.maps[self.map_id]
        self.map_data = import_csv_layout('data/maps/' + self.map_id + '/' + self.map_id + '_Collideables.csv')

        # polish ----------------------------------------------------------------------- #
        self.destruction_particles = DestructionParticles(self.game)
        self.world_animations = StandaloneAnimations(self.game)
        self.particles = ParticleManager(self.game)
        self.vfx = VFX(self.game)
        self.weapon_anims = WeaponAnimations(self.game)
        self.lights = Lights(self.game)

        self.camera = Camera(self.game)

        set_glow_surf(self.game.assets.misc['light'])

        # entities --------------------------------------------------------------------- #
        self.entities = EntityManager(self.game)
        self.player = self.entities.gen_player()
        self.towers = Towers(self.game)
        self.quadtree = QuadTree(4, Rectangle(pygame.math.Vector2(0, 0), pygame.math.Vector2(self.floor.get_size())))

        # camera ----------------------------------------------------------------------- #
        #self.camera.set_restriction(self.player.pos)
        self.camera.set_tracked_entity(self.player)

        # hitboxes --------------------------------------------------------------------- #
        self.hitboxes = Hitboxes(self.game)

        # building --------------------------------------------------------------------- #
        self.builder_menu = Builder(self.game)

        self.master_clock = 0

    def update(self):
        dt = self.game.window.dt

        self.camera.update()
        self.world_animations.update()
        self.weapon_anims.update()
        self.vfx.update()
        self.hitboxes.update()
        self.towers.update()
        self.entities.update(dt)
        self.destruction_particles.update()
        self.lights.update()

        # builder mode handler -------------------------------------------------------- #
        if self.game.input.states['open_build_mode']:
            self.entities.render_entities = False
            self.game.input.hold_reset()
            self.camera.set_tracked_entity(None)
            self.builder_mode = True
            self.game.input.input_mode = 'builder'
            self.show_builder_menu = False
            self.towers.set_display_tower(self.towers.selected_tower, 0, self.game.input.get_mouse_pos())

        if self.game.input.states['close_build_mode']:
            self.entities.render_entities = True
            self.camera.set_tracked_entity(self.player)
            self.builder_mode = False
            self.game.input.input_mode = 'core'
            self.towers.displayed_tower = None

        if self.builder_mode:
            self.game.window.add_freeze(0.0001, 0.1)
            if self.player.weapon:
                self.player.weapon.invisible = 0.2

        if self.game.input.mouse_state['right_click']:
            #self.game.world.vfx.spawn_vfx('circle', self.game.input.get_mouse_pos(), 100, 12, 100, reverse=True, ease=easeInExpo)#
            self.towers.selected_tower = 'artemis'

        self.world_timer += self.game.window.dt

    def render(self, surf):
        if not self.loaded:
            self.loaded = True
        
        offset = self.camera.true_pos

        self.vfx.render_back(self.game.window.ui_surf, offset)

        self.collideables = []
        self.render_list = []

        surf.blit(self.floor, (0 - self.camera.true_pos[0], 0 - self.camera.true_pos[1]))
        map_offset = config['level_data'][self.game.state]['tile_offset']
        for row_index, row in enumerate(self.map_data):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * 16
                    y = row_index * 16
                    #img = self.game.assets.collideables[col]
                    #self.collideables.append(self.obs_rect((x + map_offset[0], y + map_offset[1] - img.get_size()[1]), img, int(col)))
                    self.collideables.append(pygame.Rect(x, y, 16, 16))
                    #rect = self.world_rects[int(col)]
                    #self.collideables.append((x + map_offset[0] - rect[0], y + map_offset[1] - rect[1], rect[2], rect[3]))
                    """ if col != '10':
                        self.render_list.append([img, (x + offset[0] - self.camera.true_pos[0], y + offset[1] - self.camera.true_pos[1] - img.get_size()[1])]) """

        self.world_animations.render(surf, offset)
        self.weapon_anims.render(surf, offset)

        self.lights.render(self.game.window.light_surf, offset)
        self.towers.render(surf, offset)
        self.destruction_particles.render(surf, self.camera.true_pos)
        self.vfx.render_front(self.game.window.ui_surf, offset)
