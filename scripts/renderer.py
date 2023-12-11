import pygame, random
from .config import config
from .particles import ParticleManager
from .tooltips import Tooltips
import cProfile

class Renderer:
    def __init__(self, game):
        self.game = game
        self.particles = ParticleManager(self.game)
        #self.overlay_particles()
        self.tooltips = Tooltips(self.game)
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
        ui_surf = self.game.window.ui_surf
        light_surf = self.game.window.light_surf
        offset = self.game.world.camera.true_pos

        self.game.world.render(surf)
        self.game.world.entities.render(surf, offset)

        #self.update_overlay_particles(surf)

        
        #surf.blit(self.game.assets.misc['light'], (self.game.world.player.center[0] - offset[0] - self.game.assets.misc['light'].get_width() // 2, self.game.world.player.center[1] - offset[1] - self.game.assets.misc['light'].get_height() // 2))
        for light in self.game.world.visible_lights:
            light_surf.blit(self.game.assets.misc['light'], (light[0] - self.game.assets.misc['light'].get_width() // 2, light[1] - self.game.assets.misc['light'].get_height() // 2))

        ui_color = (17, 17, 17, 255)

        # ui  ----------------------------------------------------------------------------------------------------- #
        ui_surf.blit(self.game.assets.misc['ui_bar'], (10, 10))

        ratio = self.game.world.player.health / config['entities']['player']['health']
        new_width = self.game.assets.misc['main_health'].get_width() * ratio
        main_health = pygame.transform.scale(self.game.assets.misc['main_health'], (new_width, self.game.assets.misc['main_health'].get_height()))

        secondary_health = pygame.transform.scale(self.game.assets.misc['under_health'], (new_width + 1, self.game.assets.misc['under_health'].get_height()))

        ui_surf.blit(secondary_health, (12, 12))
        ui_surf.blit(main_health, (12, 12))
        ui_surf.blit(self.game.assets.misc['ui_bar_overlay'], (10, 10))
        """ pygame.draw.rect(ui_surf, ui_color, (10, 10, 100, 10))
        ratio = self.game.world.player.health / config['entities']['player']['health']
        # multiply by 98 instead of 100 to compensate for padding
        current_health = 98 * ratio
        pygame.draw.rect(ui_surf, 'red', (11, 11, current_health, 8)) """

        # inventory ----------------------------------------------------------------------------------------------- #
        if self.game.world.builder_mode:
            tilesize = 26
            count = 5
            owned_towers = self.game.world.towers.inventory_towers
            for i in range(count):
                pos = (((self.game.window.display.get_width() + (tilesize // 2)) // 2) - ((count * tilesize) // 2)) + (i * tilesize)
                ui_surf.blit(self.game.assets.misc['builder_slot'], (pos, self.game.window.display.get_height() - tilesize))
                if owned_towers[i]:
                    owned_towers[i].pos = (pos + offset[0] + (owned_towers[i].img.get_size()[0] // 2) + 1, self.game.window.display.get_height() - tilesize + offset[1] + (owned_towers[i].img.get_size()[1] // 2))
                    owned_towers[i].render(ui_surf, offset)
        else:
            tilesize = 18
            skill_count = 9
            skills = self.game.world.entities.player.skills
            for i in range(skill_count):
                pos = (((self.game.window.display.get_width() + (tilesize // 2)) // 2) - ((skill_count * tilesize) // 2)) + (i * tilesize)
                ui_surf.blit(self.game.assets.misc['inventory_slot'], (pos, self.game.window.display.get_height() - tilesize))
                if skills[i]:
                    skills[i].render_skill(ui_surf, (pos + 1, surf.get_height() + self.game.window.offset[1] - tilesize + 1))
                if i == self.game.world.entities.player.selected_inventory_slot:
                    ui_surf.blit(self.game.assets.misc['selected_inventory_slot'], (pos, self.game.window.display.get_height() - tilesize))

        # weapon ------------------------------------------------------------------------------------------------- #
        player = self.game.world.entities.player

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
                pygame.draw.line(ui_surf, ui_color, (22, base_pos + offset), (22, base_pos + offset + weapon_img.get_height()))
            ui_surf.blit(weapon_img, (25 - mask.get_bounding_rects()[0].left, base_pos + offset))
            offset += weapon_img.get_height() + 2
        
        # tooltips ----------------------------------------------------------------------------------------------- #
        self.tooltips.render(ui_surf, self.game.window.dt)

        # builder menu ------------------------------------------------------------------------------------------- #
        if self.game.world.show_builder_menu and self.game.world.builder_mode:
            self.game.world.builder_menu.render(ui_surf)

        # display the player money ------------------------------------------------------------------------------- #
        self.game.assets.large_text.render(ui_surf, '$' + str(self.game.world.entities.player.money), (10, 25))

        # round -------------------------------------------------------------------------------------------------- #
        self.game.assets.large_text.render(ui_surf, 'ROUND', (self.game.window.display.get_size()[0] // 2, 10))
        self.game.assets.large_text.render(ui_surf, str(self.game.world.entities.spawner.wave ) + '/' + str(self.game.world.entities.spawner.max_waves), ((self.game.window.display.get_size()[0] // 2) + 4, 25))
 
        # fps ---------------------------------------------------------------------------------------------------- #
        if self.game.window.show_fps:
            self.game.assets.small_text.render(ui_surf, str(int(self.game.window.fps())) + 'FPS', (self.game.window.display.get_width() - 50, 10))