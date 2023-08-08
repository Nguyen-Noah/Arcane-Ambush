import pygame, time
from .config import config

class Window:
    def __init__(self, game):
        self.game = game

        pygame.init()

        self.scaled_resolution = config['window']['scaled_resolution']
        self.base_resolution = config['window']['base_resolution']
        self.offset = [0, 0]
        self.background_color = config['window']['background_color']
        self.title = config['window']['title']

        self.screen = pygame.display.set_mode(self.scaled_resolution)
        self.display = pygame.Surface((self.base_resolution[0], self.base_resolution[1]))
        
        self.icon = pygame.image.load('data/graphics/icon/icon.png')
        pygame.display.set_icon(self.icon)
        
        pygame.display.set_caption(self.title)

        self.freeze_frame = {}

        self.dt = 0.1
        self.frame_history = [0.01]
        self.frame_start = time.time()

        self.timer = 0

    def add_freeze(self, rate, duration):
        self.freeze_frame[rate] = duration

    def render_frame(self):
        pygame.display.update()

        self.dt = time.time() - self.frame_start
        self.ui_dt = self.dt

        delete_list = []

        orig_dt = self.dt

        if self.freeze_frame != {}:
            slowest_freeze = min(list(self.freeze_frame))
            if self.freeze_frame[slowest_freeze] > self.dt:
                self.dt *= slowest_freeze
            else:
                self.dt -= self.freeze_frame[slowest_freeze] * (1 - slowest_freeze)

        for freeze_amount in self.freeze_frame:
            if self.freeze_frame[freeze_amount] > orig_dt:
                self.freeze_frame[freeze_amount] -= orig_dt
            else:
                self.freeze_frame[freeze_amount] = 0
                delete_list.append(freeze_amount)

        for freeze in delete_list:
            del self.freeze_frame[freeze]

        self.timer += self.dt
        if self.dt > 0.05:
            print('lag spike', + self.timer)
            self.timer = 0

        self.dt = min(max(0.00001, self.dt), 0.1)
        self.frame_start = time.time()
        self.frame_history.append(self.ui_dt)
        self.frame_history = self.frame_history[-200:]

        self.screen.blit(pygame.transform.scale(self.display, self.scaled_resolution), (0, 0))
        self.display.fill(self.background_color)