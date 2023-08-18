import pygame

class InventorySlot:
    def __init__(self, game, icon):
        self.game = game
        self.icon = icon

    def update(self):
        pass

    def render(self, surf, pos, tilesize):
        surf.blit(self.game.assets.skills[self.icon], (pos + 1, self.game.window.display.get_height() - tilesize + 1))
        
        if self.game.world.player.attacking:
            cd = (self.game.world.player.atk_counter / self.game.world.player.atk_cd) * tilesize
            cd_surf = pygame.Surface((tilesize - 4, tilesize - 4), pygame.SRCALPHA)
            pygame.draw.rect(cd_surf, (255, 255, 255, 100), pygame.Rect(0, cd, tilesize, tilesize))
            surf.blit(cd_surf, (pos + 2, self.game.window.display.get_height() - tilesize + 2))

class Inventory:
    def __init__(self, game):
        self.game = game
        self.max_slots = 9
        self.inventory_count = 0
        self.inventory = []

    def add(self, icon):
        if self.inventory_count < self.max_slots:
            self.inventory.append(InventorySlot(self.game, icon))
            self.inventory_count += 1

    def update(self):
        if self.game.input.mouse_state['right_click']:
            self.add('dagger')

        for slot in self.inventory:
            slot.update()

    def render(self, surf):
        tilesize = 18
        for i, slot in enumerate(self.inventory):
            if self.inventory_count % 2 == 0:
                pos = self.game.window.display.get_width() // 2 - self.inventory_count // 2 + (i - self.inventory_count // 2 + 0.5) * tilesize
            else:
                pos = self.game.window.display.get_width() // 2 - self.inventory_count // 2 * tilesize + i * tilesize
            surf.blit(self.game.assets.misc['inventory_slot'], (pos, self.game.window.display.get_height() - tilesize))
            slot.render(surf, pos, tilesize)

''' def add(self):
        if self.inventory_count < self.max_slots:
            self.inventory_count += 1

    def update(self):
        if self.game.input.mouse_state['right_click']:
            self.add()

    def render(self, surf):
        tilesize = 18

        for i in range(self.inventory_count):
            if self.inventory_count % 2 == 0:
                pos = self.game.window.display.get_width() // 2 - self.inventory_count // 2 + (i - self.inventory_count // 2 + 0.5) * tilesize
            else:
                pos = self.game.window.display.get_width() // 2 - self.inventory_count // 2 * tilesize + i * tilesize
            surf.blit(self.game.assets.misc['inventory_slot'], (pos, self.game.window.display.get_height() - tilesize))'''