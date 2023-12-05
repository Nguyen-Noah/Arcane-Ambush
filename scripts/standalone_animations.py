from .core_funcs import itr

class StandaloneAnimation:
    def __init__(self, animation_obj, location, flip=[False, False]):
        self.pos = list(location)
        self.animation = animation_obj
        self.animation.flip = flip.copy()

class StandaloneAnimations:
    def __init__(self, game):
        self.game = game
        self.animations = []

    def spawn(self, animation_id, location, flip=[False, False]):
        self.animations.append(StandaloneAnimation(self.game.assets.animations.new(animation_id), location, flip))

    def update(self):
        dt = self.game.window.dt
        for i, animation in itr(self.animations):
            animation.animation.play(dt)
            if animation.animation.done:
                self.animations.pop(i)

    def render(self, surf, offset=(0, 0)):
        for animation in self.animations:
            #pygame.draw.circle(surf, 'black', (animation.pos[0] - offset[0], animation.pos[1] - offset[1]), 10)
            animation.animation.render(surf, animation.pos, offset)