class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = 0
        self.type = "None"
        self.active = False
        self.color = (255, 0, 0)

    def get_coordinates(self):
        return self.x, self.y

    def __repr__(self):
        return str(self.id)


class Nothing(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 1
        self.type = "Nothing"
        self.color = (0, 0, 0)


class Wall(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 2
        self.type = "Wall"
        self.color = (255, 255, 255)
