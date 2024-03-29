import pygame, os
from .animation_handler import AnimationManager
from .text import Text

class Assets:
    def __init__(self, game):
        self.game = game
        
        self.animations = AnimationManager()
        self.maps = self.load_dir('data/maps/maps')
        self.collideables = self.load_dir('data/graphics/tilesets')
        self.particles = self.load_dirs('data/graphics/particles')
        self.weapons = self.load_dir('data/graphics/weapons')
        self.cursor = self.load_dir('data/graphics/cursor')
        #self.towers = self.load_dirs('data/graphics/towers')
        self.projectiles = self.load_dir('data/graphics/projectiles')
        self.skills = self.load_dir('data/graphics/skills')
        self.misc = self.load_dir('data/graphics/misc')
        self.large_text = Text('data/fonts/large.png')
        self.small_text = Text('data/fonts/small.png')
        self.money_text = Text('data/fonts/money.png', nums=True)
        self.tooltips = self.load_dir('data/graphics/tooltips')

    def load_dirs(self, path):
        dirs = {}
        for dir in os.listdir(path):
            dirs[dir] = self.load_dir(path + '/' + dir)
        return dirs

    def load_dir(self, path):
        image_dir = {}
        for file in os.listdir(path):
            image_dir[file.split('.')[0]] = self.load_img(path + '/' + file, (0, 0, 0))
        return image_dir
    
    def load_img(self, path, colorkey):
        img = pygame.image.load(path).convert_alpha()
        img.set_colorkey(colorkey)
        return img