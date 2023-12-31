import pygame, random
from .config import config
from .particles import ParticleManager
from .tooltips import Tooltips
from .vfx import draw_glows
import cProfile

class Renderer:
    def __init__(self, game):
        self.game = game
        self.particles = ParticleManager(self.game)
        self.overlay_particles()
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
        offset = self.game.world.camera.true_pos

        self.game.world.render(surf)
        self.game.world.entities.render(surf, offset)
        draw_glows(surf)

        self.update_overlay_particles(surf)
        
        #surf.blit(self.game.assets.misc['light'], (self.game.world.player.center[0] - offset[0] - self.game.assets.misc['light'].get_width() // 2, self.game.world.player.center[1] - offset[1] - self.game.assets.misc['light'].get_height() // 2))

        ui_color = (17, 17, 17, 255)

        # ui  ----------------------------------------------------------------------------------------------------- #
        health_ratio = self.game.world.player.health / config['entities']['player']['health']
        new_health_width = self.game.assets.misc['health'].get_width() * health_ratio
        adjusted_health = pygame.transform.scale(self.game.assets.misc['health'], (new_health_width, self.game.assets.misc['health'].get_height()))

        mana_ratio = self.game.world.player.mana / 100
        new_mana_width = self.game.assets.misc['mana'].get_width() * mana_ratio
        adjusted_mana = pygame.transform.scale(self.game.assets.misc['mana'], (new_mana_width, self.game.assets.misc['mana'].get_height()))
        
        ui_surf.blit(self.game.assets.misc['health_mana_ui'], (0, 10))
        ui_surf.blit(adjusted_health, (1, 12))
        if new_health_width > 0:
            ui_surf.blit(self.game.assets.misc['health_tip'], (1 + new_health_width, 12))
        ui_surf.blit(adjusted_mana, (1, 20))
        if new_mana_width > 0:
            ui_surf.blit(self.game.assets.misc['mana_tip'], (1 + new_mana_width, 20))

        # inventory ----------------------------------------------------------------------------------------------- #
        skills = self.game.world.entities.player.skills

        skill_count = len([skill for skill in skills if skill is not None])
        skill_padding = 10
        tilesize = 18

        for i in range(skill_count):
            pos = ((((self.game.window.display.get_width() + (tilesize // 2)) // 2) - ((skill_count * tilesize) // 2)) + (i * tilesize), self.game.window.display.get_height() - tilesize - 4)
            ui_surf.blit(self.game.assets.misc['inventory_slot'], pos)
            if skills[i]:
                skills[i].render_skill(ui_surf, (pos[0] + 1, pos[1] + 1))

        """ if self.game.world.builder_mode:
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
                    skills[i].render_skill(ui_surf, (pos + 1, surf.get_height() + self.game.window.offset[1] - tilesize + 1)) """

        # weapon ------------------------------------------------------------------------------------------------- #
        player = self.game.world.entities.player

        player_items = player.inventory.get_custom_group('active_weapons')
        weapon_masks = [pygame.mask.from_surface(self.game.assets.weapons[weapon.type]) for weapon in player_items]
        offset = 0
        base_pos = 46
        padding = 2
        for i, mask in enumerate(weapon_masks):
            color = (139, 171, 191, 255)
            if player_items[i] == player.weapon:
                color = (235, 235, 235, 255)
            weapon_img = mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
            if weapon_img.get_height() > weapon_img.get_width():
                weapon_img = pygame.transform.rotate(weapon_img, -90)
            if player_items[i] == player.weapon:
                pygame.draw.line(ui_surf, color, (10, base_pos + offset), (10, base_pos + offset + weapon_img.get_height() + (padding * i)))
            ui_surf.blit(weapon_img, (12 - mask.get_bounding_rects()[0].left, base_pos + offset + (padding * i)))
            offset += weapon_img.get_height() + 2
        
        # tooltips ----------------------------------------------------------------------------------------------- #
        #self.tooltips.render(ui_surf, self.game.window.dt)

        # builder menu ------------------------------------------------------------------------------------------- #
        if self.game.world.show_builder_menu and self.game.world.builder_mode:
            self.game.world.builder_menu.render(ui_surf)

        # display the player money ------------------------------------------------------------------------------- #
        self.game.assets.money_text.render(ui_surf, str(self.game.world.entities.player.money), (10, 27))

        # round -------------------------------------------------------------------------------------------------- #
        self.game.assets.large_text.render(ui_surf, 'ROUND', (self.game.window.display.get_size()[0] // 2, 10))
        self.game.assets.large_text.render(ui_surf, str(self.game.world.entities.spawner.wave ) + '/' + str(self.game.world.entities.spawner.max_waves), ((self.game.window.display.get_size()[0] // 2) + 4, 25))
 
        # fps ---------------------------------------------------------------------------------------------------- #
        if self.game.window.show_fps:
            self.game.assets.small_text.render(ui_surf, str(int(self.game.window.fps())) + 'FPS', (self.game.window.display.get_width() - 50, 10))