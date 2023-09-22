from .towers.wizard_tower import WizardTower
from .towers.archer import Archer
from .towers.bomber import Bomber
from .towers.phoenix import Phoenix
from .towers.cleric import Cleric

tower_map = {
    'wizard_tower': WizardTower,
    'archer': Archer,
    'bomber': Bomber,
    'phoenix': Phoenix,
    'cleric': Cleric
}