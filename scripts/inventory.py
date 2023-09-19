import itertools

from .item import Item
from .item_serializer import serialize_item

KNOWN_TAGS = []

class InventoryGroup:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        for i in self.items:
            if i.stackable(item):
                i.amount += item.amount
                return None

        self.items.append(item)

    def take_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return item
        return None

class Inventory:
    def __init__(self, owner=None):
        self.groups = {}
        self.owner = owner

    @property
    def all_items(self):
        return list(itertools.chain(*[self.groups[group].items for group in self.groups]))

    def deserialize(self):
        data = {group : [item.deserialize() for item in self.groups[group].items] for group in self.groups}
        return data

    def add_item(self, item, group_id):
        if group_id not in self.groups:
            self.groups[group_id] = InventoryGroup()
        self.groups[group_id].add_item(item)
        #(self.groups[group_id].items)

    def get_item_by_index(self, item_index, group_id):
        if group_id in self.groups:
            if len(self.groups[group_id].items) > item_index:
                return self.groups[group_id].items[item_index]
        return None

    def group_size(self, group_id):
        if group_id in self.groups:
            return len(self.groups[group_id].items)
        return 0

    # removes first instance if group not specified
    def take_item(self, item, group=None):
        if group:
            if group in self.groups:
                return self.groups[group].take_item(item)
            return None
        else:
            for group in self.groups:
                removed_item = self.groups[group].take_item(item)
                if removed_item:
                    return removed_item
            return None

    def get_by_tag(self, tag):
        tagged_items = []
        for item in self.all_items:
            if tag in item.tags:
                tagged_items.append(item)
        return tagged_items

    def get_custom_group(self, custom_group_id):
        if custom_group_id == 'active_weapons':
            active_weapons = [item for item in self.all_items if item.is_weapon and ('active' in item.tags)]
            return active_weapons
        if custom_group_id == 'active':
            active_items = self.get_by_tag('active')
            if self.owner and (self.owner.type == 'player'):
                if self.owner.skills[1]:
                    active_items.append(Item(self.owner.game, self.owner, self.owner.skills[1].skill_type, is_unowned_skill=True))
                if self.owner.skills[2]:
                    active_items.append(Item(self.owner.game, self.owner, self.owner.skills[2].skill_type, is_unowned_skill=True))
            return active_items
        if custom_group_id == 'active_ring':
            active_items = self.get_by_tag('active')
            active_rings = [item for item in active_items if item.is_ring]
            return active_rings
        if custom_group_id == 'weapons':
            return [item for item in self.all_items if item.is_weapon]

    def get_group(self, group_id):
        if group_id in self.groups:
            return self.groups[group_id]
        else:
            return InventoryGroup()

    def rough_group_lookup(self, group_id):
        items = self.get_custom_group(group_id)
        if not items:
            if group_id in KNOWN_TAGS:
                items = self.get_by_tag(group_id)
        if not items:
            items = self.get_group(group_id).items
        return items

def serialize_inventory(game, data, owner):
    new_inventory = Inventory(owner=owner)
    for group in data:
        for item in data[group]:
            new_item = serialize_item(game, item, owner)
            new_inventory.add_item(new_item, group)
    return new_inventory



'''class InventorySlot:
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
            slot.render(surf, pos, tilesize)'''