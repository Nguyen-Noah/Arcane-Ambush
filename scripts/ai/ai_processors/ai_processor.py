class AIProcessor:
    def __init__(self, parent_entity):
        self.parent = parent_entity
        self.ai = parent_entity.controller
        self.game = parent_entity.game