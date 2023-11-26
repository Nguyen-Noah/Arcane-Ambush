from scripts.window import Window
from scripts.input import Input
from scripts.renderer import Renderer
from scripts.world import World
from scripts.assets import Assets

class Game:
    def __init__(self):
        self.window = Window(self)
        self.assets = Assets(self)
        self.input = Input(self)
        self.renderer = Renderer(self)
        self.world = World(self)

        self.game_state = False
        self.state = 'new_format'

    def load_map(self, map_id):
        self.world.load(map_id)

    def update(self):
        self.input.update()
        self.window.render_frame()
        self.world.update()
        self.renderer.render()

    def run(self):
        while True:
            if not self.game_state:
                self.load_map(self.state)
                self.game_state = True
            self.update()

if __name__ == '__main__':
    game = Game()
    game.run()

# TODO:
    # fix dash skill by incorporating dt
    # fix wizard tower orb by incorporating dt
    # fix player movement
    # create new towers