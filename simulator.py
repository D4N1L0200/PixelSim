import random
import time

from rich import print as rprint


class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                self.grid[y].append(Cell(0, x, y))

    def update(self, area):
        for y in range(3):
            for x in range(3):
                if area.grid[y][x] == -1:
                    continue
                row = area.x - 1 + x
                col = area.y - 1 + y

                if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                    self.add_cell(area.grid[y][x].id, (row, col))

    def tick(self):
        areas = []
        for row in self.grid:
            for cell in row:
                if cell.id != 0:
                    area = Area(cell.x, cell.y, self.grid)
                    updated_area = cell.tick(area)
                    if updated_area.changed:
                        areas.append(updated_area)

        areas.reverse()

        for idx, area in enumerate(areas):
            collision_idxs = area.collides(areas[:idx] + areas[idx + 1 :])
            if len(collision_idxs):
                collision_idxs.insert(0, idx)
                choosen = random.choice(collision_idxs)
                for coll_idx in collision_idxs:
                    if coll_idx != choosen:
                        areas[coll_idx] = Area(-2, -2, [[]])
                self.update(areas[choosen])
            else:
                self.update(area)

    def add_cell(self, id, xy):
        x, y = xy
        if x > len(self.grid[0]) - 1 or x < 0 or y > len(self.grid) - 1 or y < 0:
            return
        self.grid[y][x] = Cell(id, x, y)


class Area:
    def __init__(self, x, y, sim_grid):
        self.x = x
        self.y = y
        self.changed = False
        self.old_grid = [[-1] * 3 for _ in range(3)]
        self.grid = [[-1] * 3 for _ in range(3)]

        # get neighbouring cells
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row = y + i
                new_col = x + j

                if 0 <= new_row < len(sim_grid) and 0 <= new_col < len(sim_grid[0]):
                    self.old_grid[i + 1][j + 1] = sim_grid[new_row][new_col]

    def id_at(self, x, y):
        cell = self.old_grid[(y * -1) + 1][x + 1]
        if cell == -1:
            cell = Cell(-1, 0, 0)
        return cell.id

    def place(self, x, y, id):
        self.grid[(y * -1) + 1][x + 1] = Cell(id, self.x - x, self.y - y)
        self.changed = True

    def valid_points(self):
        points = []

        for iidx, i in enumerate(range(self.y - 1, self.y + 2)):
            for jidx, j in enumerate(range(self.x - 1, self.x + 2)):
                if self.grid[iidx][jidx] != -1:
                    points.append((j, i))

        return points

    def collides(self, areas):
        valid_points = self.valid_points()
        idxs = []
        for idx, area in enumerate(areas):
            if abs(self.x - area.x) <= 2 and abs(self.y - area.y) <= 2:
                other_valid_points = area.valid_points()
                for item in valid_points:
                    if item in other_valid_points:
                        idxs.append(idx + 1)
        return idxs


class Cell:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self.id)

    def tick(self, area):
        if area.id_at(0, 0) == 1:  # Sand
            # Down
            if area.id_at(0, -1) == 0:
                area.place(0, 0, 0)
                area.place(0, -1, 1)
            if area.id_at(0, -1) == 1:
                if random.randint(0, 1):  # Left Priority
                    # Diagonal Down Left
                    if area.id_at(-1, -1) == 0:
                        area.place(0, 0, 0)
                        area.place(-1, -1, 1)
                    # Diagonal Down Right
                    elif area.id_at(1, -1) == 0:
                        area.place(0, 0, 0)
                        area.place(1, -1, 1)
                else:  # Right Priority
                    # Diagonal Down Right
                    if area.id_at(1, -1) == 0:
                        area.place(0, 0, 0)
                        area.place(1, -1, 1)
                    # Diagonal Down Left
                    elif area.id_at(-1, -1) == 0:
                        area.place(0, 0, 0)
                        area.place(-1, -1, 1)
            # Down Water
            if area.id_at(0, -1) == 2:
                area.place(0, 0, 2)
                area.place(0, -1, 1)
            # Diagonal Down Left Water
            elif area.id_at(-1, -1) == 2:
                area.place(0, 0, 2)
                area.place(-1, -1, 1)
            # Diagonal Down Right Water
            elif area.id_at(1, -1) == 2:
                area.place(0, 0, 2)
                area.place(1, -1, 1)
        if area.id_at(0, 0) == 2:  # Water
            # Down
            if area.id_at(0, -1) == 0:
                area.place(0, 0, 0)
                area.place(0, -1, 2)
            elif random.randint(0, 1):  # Left Priority
                #  Left
                if area.id_at(-1, 0) == 0:
                    area.place(0, 0, 0)
                    area.place(-1, 0, 2)
                #  Right
                elif area.id_at(1, 0) == 0:
                    area.place(0, 0, 0)
                    area.place(1, 0, 2)
            else:  # Right Priority
                #  Right
                if area.id_at(1, 0) == 0:
                    area.place(0, 0, 0)
                    area.place(1, 0, 2)
                #  Left
                elif area.id_at(-1, 0) == 0:
                    area.place(0, 0, 0)
                    area.place(-1, 0, 2)
        # if area.id_at(0, 0) == 3:  # Left Water
        #     if area.id_at(0, -1) == 0:  # Down
        #         area.place(0, 0, 0)
        #         area.place(0, -1, 3)
        #     elif area.id_at(-1, 0) == 0:  #  Left Empty
        #         area.place(0, 0, 0)
        #         area.place(-1, 0, 3)
        #     elif area.id_at(-1, 0) == -1:  #  Left Wall
        #         area.place(0, 0, 4)
        #     elif area.id_at(-1, 0) == 4:  #  Left Water
        #         area.place(0, 0, 4)
        #         area.place(-1, 0, 3)
        # if area.id_at(0, 0) == 4:  # Right Water
        #     if area.id_at(0, -1) == 0:  # Down
        #         area.place(0, 0, 0)
        #         area.place(0, -1, 4)
        #     elif area.id_at(1, 0) == 0:  #  Right Empty
        #         area.place(0, 0, 0)
        #         area.place(1, 0, 4)
        #     elif area.id_at(1, 0) == -1:  #  Right Wall
        #         area.place(0, 0, 3)
        return area


if __name__ == "__main__":
    sim = Simulation(10, 10)
    sim.add_cell(1, (2, 2))
    sim.add_cell(1, (3, 3))
    sim.add_cell(1, (2, 5))
    sim.add_cell(1, (2, 4))
    sim.add_cell(1, (3, 0))
    running = True
    while running:
        rprint(sim.grid)
        time.sleep(0.5)
        sim.tick()
