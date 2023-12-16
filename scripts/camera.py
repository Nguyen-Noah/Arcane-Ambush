import math, random
from .config import config
from .core_funcs import clamp_between

class Camera:
    def __init__(self, game):
        self.game = game
        self.camera_offset = config['level_data'][self.game.state]['camera_starting_pos']
        self.true_pos = self.camera_offset.copy()
        self.target_pos = [0, 0]
        self.rate = 0.25
        self.track_entity = None
        self.restriction_point = None
        self.lock_distance = config['level_data'][self.game.state]['lock_distance']
        self.mode = None
        self.screen_shake = 0

    def focus(self):
        self.update()
        self.true_pos = self.target_pos.copy()

    def set_tracked_entity(self, entity):
        self.track_entity = entity

    def set_target(self, pos):
        self.target_pos = list(pos)

    def set_restriction(self, pos):
        self.restriction_point = list(pos)

    def add_screen_shake(self, amt):
        self.screen_shake = amt

    def update(self):
        self.true_pos = self.camera_offset.copy()

        if self.screen_shake:
            self.true_pos[0] += random.randint(0, 8) - 4
            self.true_pos[1] += random.randint(0, 8) - 4
            self.screen_shake -= 1

        if self.game.world.builder_mode:
            self.rate = .0005
        else:
            self.rate = 0.25

        if self.mode == 'freeroam':
            x_direction = 0
            y_direction = 0
            if self.game.input.states['pan_left']:
                x_direction = -1
            elif self.game.input.states['pan_right']:
                x_direction = 1
            if self.game.input.states['pan_up']:
                y_direction = -1
            elif self.game.input.states['pan_down']:
                y_direction = 1
            
            self.camera_offset[0] += x_direction * 1.5
            self.camera_offset[1] += y_direction * 1.5
        else:
            # Weapon Lead --------------------------------------- #
            if self.track_entity:
                if self.track_entity.type == 'player':
                    target_pos = self.track_entity.pos.copy()
                    if self.track_entity.weapon:
                        angle = math.radians(self.track_entity.weapon.rotation)
                        dis = math.sqrt((self.game.input.mouse_pos[1] - self.track_entity.center[1] + self.game.world.camera.render_offset[1]) ** 2 + (self.game.input.mouse_pos[0] - self.track_entity.center[0] + self.game.world.camera.render_offset[0]) ** 2)
                        target_pos[0] += math.cos(angle) * (dis / 8)
                        target_pos[1] += math.sin(angle) * (dis / 8)
                self.set_target((target_pos[0] - self.game.window.display.get_width() // 2, target_pos[1] - self.game.window.display.get_height() // 2))

            # Core Camera Functionality -------------------------- #
            self.camera_offset[0] += math.floor(self.target_pos[0] - self.camera_offset[0]) / (self.rate / self.game.window.dt)
            self.camera_offset[1] += math.floor(self.target_pos[1] - self.camera_offset[1]) / (self.rate / self.game.window.dt)

        # clamp the camera so that the camera will not show anything outside of the map
        # use 4 pixel padding to compensate for screenshake
        self.camera_offset = clamp_between(self.camera_offset, min_offset=(4, 4), max_offset=(self.game.world.floor.get_width() - self.game.window.base_resolution[0] - 4, self.game.world.floor.get_height() - self.game.window.base_resolution[1] - 4))

        if self.restriction_point:
            if self.camera_offset[0] + self.game.window.display.get_width() // 2 - self.restriction_point[0] > self.lock_distance[0]:
                self.camera_offset[0] = self.restriction_point[0] - self.game.window.display.get_width() // 2 + self.lock_distance[0]
            if self.camera_offset[0] + self.game.window.display.get_width() // 2 - self.restriction_point[0] < -self.lock_distance[0]:
                self.camera_offset[0] = self.restriction_point[0] - self.game.window.display.get_width() // 2 - self.lock_distance[0]
            if self.camera_offset[1] + self.game.window.display.get_height() // 2 - self.restriction_point[1] > self.lock_distance[1]:
                self.camera_offset[1] = self.restriction_point[1] - self.game.window.display.get_height() // 2 + self.lock_distance[1]
            if self.camera_offset[1] + self.game.window.display.get_height() // 2 - self.restriction_point[1] < -self.lock_distance[1]:
                self.camera_offset[1] = self.restriction_point[1] - self.game.window.display.get_height() // 2 - self.lock_distance[1]

    @property
    def render_offset(self):
        return [self.camera_offset[0] - self.game.window.offset[0], self.camera_offset[1] - self.game.window.offset[1]]

    @property
    def pos(self):
        return (int(math.floor(self.camera_offset[0])), int(math.floor(self.camera_offset[1])))