import pygame

class Tooltips:
    def __init__(self, game):
        self.game = game
        self.timer = 3
        self.start_timer = False
        self.render_move = True

    def update(self, dt):
        # TODO: create timer for tutorial tooltips
        self.timer += dt

    def render(self, surf, dt):
        if not self.start_timer and self.render_move and any(state for state in self.game.input.states.values()):
            self.start_timer = True

        if self.timer < 0:
            self.render_move = False

        if self.render_move:
            pos = (self.game.world.entities.player.center[0] - self.game.world.camera.true_pos[0], self.game.world.entities.player.center[1] - self.game.world.camera.true_pos[1])
            surf.blit(self.game.assets.tooltips['w'], (pos[0] - 6, pos[1] - 45))
            surf.blit(self.game.assets.tooltips['a'], (pos[0] - 22, pos[1] - 30))
            surf.blit(self.game.assets.tooltips['s'], (pos[0] - 6, pos[1] - 30))
            surf.blit(self.game.assets.tooltips['d'], (pos[0] + 10, pos[1] - 30))

            if self.start_timer:
                self.timer -= dt