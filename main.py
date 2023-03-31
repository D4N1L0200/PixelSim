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

    def push_cell(self, new_cell):
        self.grid[new_cell.y][new_cell.x] = new_cell

    def push_cells(self, cell_list, new_cell):
        pass
        # TODO

    def get_neighbours(self, cell, diagonal=True):
        neighbours = []
        if diagonal:
            # left to right, top to bottom
            for x in range(cell.x - 1, cell.x + 2):
                for y in range(cell.y - 1, cell.y + 2):
                    if x != cell.x or y != cell.y:
                        neighbours.append(self.get_cell(x, y))
        else:
            # left, right, top, bottom
            for x in range(cell.x - 1, cell.x + 2):
                if x != cell.x:
                    neighbours.append(self.get_cell(x, cell.y))
            for y in range(cell.y - 1, cell.y + 2):
                if y != cell.y:
                    neighbours.append(self.get_cell(cell.x, y))
        return neighbours


class Simulation:
    def __init__(self):
        self.cellGrid = CellGrid(10, 10)
        self.running = False

    def tick(self):
        # Update the grid
        for row in self.cellGrid.grid:
            for cell in row:
                if cell.active:
                    cell.tick(self.cellGrid)

    def test(self):
        # rprint(self.cellGrid.grid)
        self.cellGrid.push_cell(cellT.Expandable(5, 5))
        rprint(self.cellGrid.grid)
        self.tick()
        rprint(self.cellGrid.grid)


if __name__ == "__main__":
    sim = Simulation()
    sim.test()
    # sim.run()
