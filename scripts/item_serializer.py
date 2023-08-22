from .weapons import create_weapon
from .item import create_item
from .config import config

def serialize_item(game, data, owner):
    if data['type'] in config['weapons']:
        return create_weapon(game, owner, data['type'], tags=data['tags'])