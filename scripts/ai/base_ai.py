class BaseAI:
    def __init__(self, parent):
        self.parent = parent
        self.game = parent.game
        self.init()

    def init(self):
        pass