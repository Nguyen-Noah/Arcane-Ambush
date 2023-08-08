import pygame

class Skill:
    def __init__(self, game, owner, skill_type):
        self.game = game
        self.owner = owner
        self.skill_type = skill_type
        self.max_charges = 1
        self.charges = self.max_charges
        self.charge_rate = 1

    def update(self):
        if self.charges < self.max_charges:
            self.charge += self.game.window.dt
            if self.charge > self.charge_rate:
                self.charge = 0
                self.charges += 1

    def use(self):
        if self.charges:
            self.charges -= 1
            return True
        else:
            return False
        
class Dagger(Skill):
    def __init__(self, game, owner):
        super().__init__(game, owner, 'dash')




SKILLS = {
    'dagger': Dagger
}