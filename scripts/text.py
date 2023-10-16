import pygame
from .core_funcs import clip

class Text:
    def __init__(self, path):
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '?', '.', ',', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '$']
        self.spacing = 1
        font_img = pygame.image.load(path).convert()
        font_img.set_colorkey((255, 255, 255))
        current_char_width = 0
        self.characters = {}
        character_count = 0

        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 100:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1

        self.space_width = self.characters['A'].get_width()
    
    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing