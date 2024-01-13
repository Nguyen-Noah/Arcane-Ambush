from .core_funcs import round_nearest, tuplify
from .config import config
from .tower_map import tower_map
from .skills import SKILLS
import pygame

class Towers:
    def __init__(self, game):
        self.game = game
        self.towers = []
        self.inventory_towers = []
        self.selected_tower = 'aether'
        self.displayed_tower = None

        for tower in tower_map:
            self.inventory_towers.append(tower_map[tower](self.game, tower, 0, hoverable=False))
 
    def set_display_tower(self, type, rank, pos):
        self.displayed_tower = tower_map[type](self.game, type, rank, pos)
        self.displayed_tower.set_opacity(128)

    def add(self, game, type, rank, pos):
        cost = config['towers'][type]['cost'][rank]

        skills = self.game.world.player.skills

        if not any(skill.skill_type == config['towers'][type]['player_skill'] for skill in skills if skill is not None):
            index = skills.index(None)
            skills[index] = SKILLS[config['towers'][type]['player_skill']](self.game, self.game.world.player)

        if cost <= self.game.world.player.money:
            new_tower = tower_map[type](game, type, rank, pos)
            self.towers.append(new_tower)
            self.game.world.lights.add_light(180, new_tower.color, new_tower)
            self.game.world.player.money -= cost

    def get_selected_tower(self):
        tilesize = 26
        count = 5
        tower_index = []
        for i in range(count):
            pos = (((self.game.window.display.get_width() + (tilesize // 2)) // 2) - ((count * tilesize) // 2)) + (i * tilesize)
            tower_index.append(pygame.Rect(pos, self.game.window.display.get_height() - tilesize, tilesize, tilesize))

    def update(self):
        for i, tower in enumerate(self.towers):
            """ if tower.tower_hover() and self.game.input.mouse_state['right_click']:
                self.towers.pop(i) """
            tower.update(self.game.window.dt)

        if self.displayed_tower:
            self.displayed_tower.pos = (round_nearest(self.game.input.get_mouse_pos()[0], 8), round_nearest(self.game.input.get_mouse_pos()[1], 8))

        if self.game.world.builder_mode and self.game.input.mouse_state['left_click']:
            self.add(self.game, self.selected_tower, 0, (round_nearest(self.game.input.get_mouse_pos()[0], 8), round_nearest(self.game.input.get_mouse_pos()[1], 8)))

    def render(self, surf, offset):
        if self.displayed_tower:
            self.displayed_tower.render(surf, offset)

        if self.game.world.builder_mode:
            self.get_selected_tower()

    def output_stats(self):
        print('-------tower--------')
        print('number of towers', len(self.towers))