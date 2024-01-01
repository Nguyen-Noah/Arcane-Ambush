import random
from ..weapon_types.grimoire_type import GrimoireWeapon

class FireGrimoireWeapon(GrimoireWeapon):
    def attack(self):
        super().attack()
        
    def update(self):
        super().update(color=(random.randint(235, 255), 2 * random.randint(0,100), 0))