import pygame

class InventorySlot:
    def __init__(self, game, icon, cooldown):
        self.game = game
        self.icon = icon
        self.cooldown = cooldown

    def update(self):
        self.cooldown -= self.game.window.dt

    def render(self, surf, pos, tilesize):
        surf.blit(self.game.assets.skills[self.icon], (pos + 1, self.game.window.display.get_height() - tilesize + 1))
        rect = pygame.draw.rect(pos, self.game.window.display.get_height() - tilesize, tilesize, tilesize)
        surf.blit(rect)

class Inventory:
    def __init__(self, game):
        self.game = game
        self.max_slots = 9
        self.inventory_count = 0
        self.inventory = []

    def add(self, icon, cooldown):
        if self.inventory_count < self.max_slots:
            self.inventory.append(InventorySlot(self.game, icon, cooldown))
            self.inventory_count += 1

    def update(self):
        if self.game.input.mouse_state['right_click']:
            self.add('dagger', 1)

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