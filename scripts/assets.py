import pygame, os
from . import spritesheet_loader
from .config import config
from .animation_handler import AnimationManager
from .text import Text


class Assets:
    def __init__(self, game):
        self.game = game

        self.animations = AnimationManager()
        self.spritesheets, self.spritesheet_data = spritesheet_loader.load_spritesheets('data/graphics/tilesets')
        self.particles = self.load_dirs('data/graphics/particles')
        self.weapons = self.load_dir('data/graphics/weapons')
        self.skills = self.load_dir('data/graphics/skills')
        self.misc = self.load_dir('data/graphics/misc')
        self.text = Text('data/fonts/large.png')

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
        img = pygame.image.load(path).convert()
        img.set_colorkey(colorkey)
        return img