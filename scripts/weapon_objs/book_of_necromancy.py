import random
from ..weapon_types.grimoire_type import GrimoireWeapon

class Book_of_necromancyWeapon(GrimoireWeapon):
    def attack(self):
        super().attack()
        
    def update(self):
        super().update(color=(random.randint(60, 80), 10, random.randint(60, 80)))