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
        self.state = 'new_test_graphics'
        #self.state = 'new_format'

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

""" 
import pygame, math, sys
from pygame.locals import *

WIDTH = 360
HEIGHT = 480
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("<Your game>")
clock = pygame.time.Clock()

# Game loop
while True:
    screen.fill(BLACK)

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == 27):
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
    pygame.display.update() """