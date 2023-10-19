from .entity_objs.player import Player
from .entity_objs.slime import Slime
from .entity_objs.megaslime import MegaSlime
from .entity_objs.kingslime import KingSlime
from .entity_objs.knight import Knight

entity_map = {
    'player': Player,
    'slime': Slime,
    'mega_slime': MegaSlime,
    'king_slime': KingSlime,
    'knight': Knight
}