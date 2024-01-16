import pygame, time
from .config import config
from .mgl import MGL

class Window:
    def __init__(self, game):
        self.game = game

        pygame.init()

        # config ------------------------------------------------------------------------- #
        self.scaled_resolution = config['window']['scaled_resolution']
        self.base_resolution = config['window']['base_resolution']
        self.offset = [0, 0]
        self.background_color = config['window']['background_color']
        self.title = config['window']['title']

        # screen ------------------------------------------------------------------------- #
        self.screen = pygame.display.set_mode(self.scaled_resolution, pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface(self.base_resolution, pygame.SRCALPHA)
        self.light_surf = self.display.copy()
        self.ui_surf = self.display.copy()
        self.mgl = MGL()

        self.screen_ratio = self.scaled_resolution[0] // self.base_resolution[0]
        
        # icon and caption --------------------------------------------------------------- #
        self.icon = pygame.image.load('data/graphics/icon/icon.png')
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(self.title)

        # time and dt -------------------------------------------------------------------- #
        self.freeze_frame = {}

        self.dt = 0.1
        self.frame_history = [0.01]
        self.frame_start = time.time()
        self.show_fps = True
        self.timer = 0

        # cursor -------------------------------------------------------------------------- #
        pygame.mouse.set_visible(False)
        self.cursor_id = 'normal'
        self.cursor = None

    def fps(self):
        avg_dt = sum(self.frame_history) / len(self.frame_history)
        avg_fps = 1 / avg_dt
        return avg_fps

    def add_freeze(self, rate, duration):
        self.freeze_frame[rate] = duration

    def render_frame(self):
        # render the cursor
        if not self.cursor:
            self.cursor = self.game.assets.cursor[self.cursor_id]
        self.ui_surf.blit(self.cursor, (self.game.input.mouse_pos[0] - self.offset[0] - self.game.assets.cursor[self.cursor_id].get_width() // 2, self.game.input.mouse_pos[1] - self.offset[1] - self.game.assets.cursor[self.cursor_id].get_height() // 2))

        # converting the screen surfaces into mgl textures
        self.display.blit(self.light_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        self.mgl.pg2tx(self.display, 'base_display')
        self.mgl.pg2tx(self.light_surf, 'light_surf')
        self.mgl.pg2tx(self.ui_surf, 'ui_surf')

        # passing in uniforms to the shaders
        world = self.game.world
        self.mgl.render(world.world_timer, self.base_resolution, world.player.i_frames)

        # get dt
        self.dt = time.time() - self.frame_start
        self.ui_dt = self.dt

        delete_list = []

        orig_dt = self.dt

        # screen freezes
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

        # used for debugging frame spikes
        self.timer += self.dt
        if self.dt > 0.05:
            print('lag spike', + self.timer)
            self.timer = 0

        self.dt = min(max(0.00001, self.dt), 0.1)
        self.frame_start = time.time()
        self.frame_history.append(self.ui_dt)
        self.frame_history = self.frame_history[-200:]

        self.display.fill(self.background_color)
        self.light_surf.fill((25, 25, 25, 0))
        self.ui_surf.fill((0, 0, 0, 0))