from .config import config

class Item:
    def __init__(self, game, owner, type, amount=1, is_unowned_skill=False, tags=[]):
        self.game = game
        self.owner = owner
        self.type = type
        self.amount = amount
        self.is_weapon = False
        self.is_skill = (self.info['type'] == 'skill')
        self.is_consumable = (self.info['type'] == 'consumable')
        self.is_unowned_skill = is_unowned_skill
        self.tags = tags

    @property
    def info(self):
        return config['items'][self.type]

    def deserealize(self):
        data = {
            'type': self.type,
            'amount': self.amount,
            'tags': self.tags
        }

    def stackable(self, item):
        if self.is_weapon or self.is_skill:
            return False

        if self.type == item.type:
            return True

        return False

def create_item(owner, type, amount=1, tags=[]):
    return Item(owner.game, owner, type, amount=amount, tags=tags)