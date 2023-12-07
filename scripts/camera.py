import math
from .config import config

class Camera:
    def __init__(self, game):
        self.game = game
        self.true_pos = config['level_data'][self.game.state]['camera_starting_pos']
        self.target_pos = [0, 0]
        self.rate = 0.25
        self.track_entity = None
        self.restriction_point = None
        self.lock_distance = config['level_data'][self.game.state]['lock_distance']
        self.mode = None

    def focus(self):
        self.update()
        self.true_pos = self.target_pos.copy()

    def set_tracked_entity(self, entity):
        self.track_entity = entity

    def set_target(self, pos):
        self.target_pos = list(pos)

    def set_restriction(self, pos):
        self.restriction_point = list(pos)

    def update(self):
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
            
            self.true_pos[0] += x_direction * 1.5
            self.true_pos[1] += y_direction * 1.5
        else:
            if self.track_entity:
                if self.track_entity.type == 'player':
                    target_pos = self.track_entity.pos.copy()
                    if self.track_entity.weapon:
                        angle = math.radians(self.track_entity.weapon.rotation)
                        dis = math.sqrt((self.game.input.mouse_pos[1] - self.track_entity.center[1] + self.game.world.camera.render_offset[1]) ** 2 + (self.game.input.mouse_pos[0] - self.track_entity.center[0] + self.game.world.camera.render_offset[0]) ** 2)
                        target_pos[0] += math.cos(angle) * (dis / 8)
                        target_pos[1] += math.sin(angle) * (dis / 8)
                self.set_target((target_pos[0] - self.game.window.display.get_width() // 2, target_pos[1] - self.game.window.display.get_height() // 2))

            self.true_pos[0] += math.floor(self.target_pos[0] - self.true_pos[0]) / (self.rate / self.game.window.dt)
            self.true_pos[1] += math.floor(self.target_pos[1] - self.true_pos[1]) / (self.rate / self.game.window.dt)

        if self.restriction_point:
            if self.true_pos[0] + self.game.window.display.get_width() // 2 - self.restriction_point[0] > self.lock_distance[0]:
                self.true_pos[0] = self.restriction_point[0] - self.game.window.display.get_width() // 2 + self.lock_distance[0]
            if self.true_pos[0] + self.game.window.display.get_width() // 2 - self.restriction_point[0] < -self.lock_distance[0]:
                self.true_pos[0] = self.restriction_point[0] - self.game.window.display.get_width() // 2 - self.lock_distance[0]
            if self.true_pos[1] + self.game.window.display.get_height() // 2 - self.restriction_point[1] > self.lock_distance[1]:
                self.true_pos[1] = self.restriction_point[1] - self.game.window.display.get_height() // 2 + self.lock_distance[1]
            if self.true_pos[1] + self.game.window.display.get_height() // 2 - self.restriction_point[1] < -self.lock_distance[1]:
                self.true_pos[1] = self.restriction_point[1] - self.game.window.display.get_height() // 2 - self.lock_distance[1]

    @property
    def render_offset(self):
        return [self.true_pos[0] - self.game.window.offset[0], self.true_pos[1] - self.game.window.offset[1]]

    @property
    def pos(self):
        return (int(math.floor(self.true_pos[0])), int(math.floor(self.true_pos[1])))