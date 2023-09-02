import pygame, random
from .particles import ParticleManager
import cProfile

class Renderer:
    def __init__(self, game):
        self.game = game
        self.particles = ParticleManager(self.game)
        #self.overlay_particles()
        self.profiler = cProfile.Profile()

    def overlay_particles(self):
        for i in range(25):
            loc = [random.random() * self.game.window.display.get_width(), random.random() * self.game.window.display.get_height()]
            r = random.randint(1, 4)
            if r == 4:
                self.particles.add_particle('overlay', loc, 'p', [random.random() * -25 - 15, random.random() * 25 + 25], 0, random.choice([5, 5, 4]), custom_color=(200, 200, 200), glow=(10, 10, 10), glow_radius=4) #(201, 255, 229)
            else:
                self.particles.add_particle('overlay', loc, 'p', [random.random() * -25 - 15, random.random() * 25 + 25], 0, random.choice([5, 5, 4]), custom_color=(50, 50, 50))

    def update_overlay_particles(self, surf):
        self.particles.update()

        offset = [self.game.world.camera.pos[0] // 3, self.game.world.camera.pos[1] // 4]

        for particle in self.particles.particle_groups['overlay']:
            if particle.pos[0] + particle.internal_offset[0] < offset[0] - 1:
                particle.pos[0] += self.game.window.display.get_width()
            if particle.pos[0] + particle.internal_offset[0] > offset[0] + self.game.window.display.get_width() + 1:
                particle.pos[0] -= self.game.window.display.get_width()
            if particle.pos[1] + particle.internal_offset[1] < offset[1] - 1:
                particle.pos[1] += self.game.window.display.get_height()
            if particle.pos[1] + particle.internal_offset[1] > offset[1] + self.game.window.display.get_height() + 1:
                particle.pos[1] -= self.game.window.display.get_height()

        self.particles.render('overlay', surf, offset)

    def render(self):
        surf = self.game.window.display

        self.game.world.render(surf)
        self.game.world.entities.render(surf)

        #self.update_overlay_particles(surf)

        ui_color = (255, 255, 255, 255)

        # ui

        # inventory
        if self.game.world.builder_mode:
            tilesize = 26
            count = 5
            owned_towers = self.game.world.player.owned_towers
            for i in range(count):
                pos = self.game.window.display.get_width() // 2 - count // 2 * tilesize + i * tilesize
                surf.blit(self.game.assets.misc['builder_slot'], (pos, self.game.window.display.get_height() - tilesize))
                if owned_towers[i]:
                    pass
        else:
            tilesize = 18
            skill_count = 9
            skills = self.game.world.entities.player.skills
            for i in range(skill_count):
                pos = self.game.window.display.get_width() // 2 - skill_count // 2 * tilesize + i * tilesize
                surf.blit(self.game.assets.misc['inventory_slot'], (pos, self.game.window.display.get_height() - tilesize))
                if skills[i]:
                    skills[i].render_skill(surf, (pos + 1, surf.get_height() + self.game.window.offset[1] - tilesize + 1))

        # weapon
        '''player = self.game.world.entities.player

        player_items = player.inventory.get_custom_group('active_weapons')
        weapon_masks = [pygame.mask.from_surface(self.game.assets.weapons[weapon.type]) for weapon in player_items]
        offset = 0
        base_pos = 46
        for i, mask in enumerate(weapon_masks):
            color = (139, 171, 191, 255)
            if player_items[i] == player.weapon:
                color = ui_color
            weapon_img = mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
            if player_items[i] == player.weapon:
                pygame.draw.line(surf, ui_color, (22, base_pos + offset), (22, base_pos + offset + weapon_img.get_height()))
            surf.blit(weapon_img, (25 - mask.get_bounding_rects()[0].left, base_pos + offset))
            offset += weapon_img.get_height() + 2'''

        # display the player money
        self.game.assets.text.render(surf, '$' + str(self.game.world.entities.player.money), (300, 20))
