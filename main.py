from rich import print as rprint
import cellTypes as cellT


class CellGrid:
    def __init__(self, width, height, built=True, walled=True):
        self.width = width
        self.height = height
        self.walled = walled
        self.grid = []
        # Option to have the grid empty
        if built:
            self.build_grid()

    def build_grid(self):
        # Build the grid, with walls or nothing
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                if not self.walled:
                    self.grid[y].append(cellT.Nothing(x, y))
                else:
                    if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                        self.grid[y].append(cellT.Wall(x, y))
                    else:
                        self.grid[y].append(cellT.Nothing(x, y))

    def get_cell(self, x, y):
        return self.grid[y][x]


class Simulation:
    def __init__(self):
        self.cellGrid = CellGrid(10, 10)
        self.running = False
        # self.updateBuffer = []  # Update list

    def test(self):
        rprint(self.cellGrid.grid)
        rprint(self.cellGrid.get_cell(4, 7))


if __name__ == "__main__":
    sim = Simulation()
    sim.test()
    # sim.run()
