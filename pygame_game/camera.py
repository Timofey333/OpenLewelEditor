

class Camera:
    def __init__(self, map, x: int = 0, y: int = 0) -> None:
        self.x, self.y = x, y
        self.map = map

    @property
    def pos_x(self):
        return self.x

    @property
    def pos_y(self):
        return self.y
