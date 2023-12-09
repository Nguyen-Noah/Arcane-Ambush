import pygame, math
from .core_funcs import import_csv_layout
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

from .quadtree import QuadTree, Rectangle

class World:
    def __init__(self, game):
        self.game = game
        self.loaded = False
        self.collideables = []
        self.builder_mode = False
        self.show_builder_menu = False
        self.world_timer = 0
        self.lights = []
        self.visible_lights = []

        """ self.world_rects = {}
        for i, obstacle in enumerate(config['obst_hitboxes']['tutorial']):
            self.world_rects[i] = self.set_obstacle_hitbox(i, obstacle) """

    def set_obstacle_hitbox(self, idx, offset):
        img = self.game.assets.collideables[str(idx)]
        hitbox = (offset[2] + offset[0] // 2, offset[1], img.get_width() + offset[0], img.get_height() + offset[1])
        return pygame.Rect(hitbox)

    def obs_rect(self, tile, img, idx):
        # 0 -> big tree, 1 -> short tree, 2 -> alive bush, 3 -> stump, 4 -> fence, 5 -> log, 6 -> right-facing lamp, 7 -> down-facing lamp, 8 -> left-facing lamp, 9 -> broken lamp
        offset = config['obst_hitboxes']['tutorial'][idx]
        coord = (tile[0], tile[1])
        hitbox = (coord[0] - (offset[0] // 2) + offset[2], coord[1] - offset[1], img.get_rect().width + offset[0], img.get_rect().height + offset[1])
        #pygame.draw.rect(self.game.window.display, 'red', (hitbox[0] - self.camera.true_pos[0], hitbox[1] - self.camera.true_pos[1], hitbox[2], hitbox[3]), 1)
        return pygame.Rect(hitbox)

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
        self.lights = config['level_data'][self.map_id]['light_sources']

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

    def render(self, surf):
        if not self.loaded:
            self.loaded = True

        self.vfx.render_back(surf, self.camera.true_pos)

        self.collideables = []
        self.render_list = []

        surf.blit(self.floor, (0 - self.camera.true_pos[0], 0 - self.camera.true_pos[1]))
        offset = config['level_data'][self.game.state]['tile_offset']
        for row_index, row in enumerate(self.map_data):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * 16
                    y = row_index * 16
                    img = self.game.assets.collideables[col]
                    self.collideables.append(self.obs_rect((x + offset[0], y + offset[1] - img.get_size()[1]), img, int(col)))
                    #rect = self.world_rects[int(col)]
                    #self.collideables.append((x + offset[0] - rect[0], y + offset[1] - rect[1], rect[2], rect[3]))
                    if col != '10':
                        self.render_list.append([img, (x + offset[0] - self.camera.true_pos[0], y + offset[1] - self.camera.true_pos[1] - img.get_size()[1])])

        self.world_animations.render(surf, self.camera.pos)
        self.weapon_anims.render(surf, self.camera.pos)

        self.towers.render(surf, self.camera.true_pos)
        self.destruction_particles.render(surf, self.camera.true_pos)
        self.vfx.render_front(surf, self.camera.true_pos)
        for light in self.visible_lights:
            #print(light)
            pygame.draw.circle(surf, 'white', light, 10)
        
    def update(self):
        self.camera.update()
        self.world_animations.update()
        self.weapon_anims.update()
        self.vfx.update()
        self.towers.update()
        self.hitboxes.update()
        self.towers.update()
        self.entities.update()
        self.destruction_particles.update()

        self.visible_lights = []
        for light in self.lights:
            self.visible_lights.append(((light[0] - self.camera.true_pos[0]) / self.game.window.display.get_width(), (light[1] - self.camera.true_pos[1]) / self.game.window.display.get_height()))

        """ self.quadtree.clear()
        for entity in self.entities.entities:
            if entity.category == 'enemy':
                self.quadtree.insert(entity) """

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
            self.camera.mode = None
            self.builder_mode = False
            self.game.input.input_mode = 'core'
            self.towers.displayed_tower = None

        if self.builder_mode:
            self.game.window.add_freeze(0.0001, 0.1)
            self.player.weapon.invisible = 0.2

        if self.game.input.mouse_state['right_click']:
            print((self.player.center[0] + self.camera.true_pos[0], self.player.center[1] + self.camera.true_pos[1]))

        self.world_timer += self.game.window.dt