import random
import time

from rich import print as rprint
from line_parser import Parser


class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.load_rules()
        self.grid = []
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                self.grid[y].append(Cell("Empty", x, y, self.rules["Empty"]))
                # self.grid[y].append(Cell("Sand", x, y, self.rules["Sand"]))
                # self.grid[y].append(Cell("Water", x, y, self.rules["Water"]))

    def update(self, area):
        for y in range(3):
            for x in range(3):
                if area.grid[y][x] == -1:
                    continue
                row = area.x - 1 + x
                col = area.y - 1 + y

                if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                    self.add_cell(area.grid[y][x].name, (row, col))

    def tick(self):
        areas = []
        for row in self.grid:
            for cell in row:
                if cell.id != 0:
                    area = Area(cell.x, cell.y, self.grid, self.rules)
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
                        areas[coll_idx] = Area(-2, -2, [[]], self.rules)
                self.update(areas[choosen])
            else:
                self.update(area)

    def add_cell(self, name, xy):
        x, y = xy
        if x > len(self.grid[0]) - 1 or x < 0 or y > len(self.grid) - 1 or y < 0:
            return
        self.grid[y][x] = Cell(name, x, y, self.rules[name])

    def load_rules(self):
        parser = Parser("cells.pixel")
        parser.load_file()
        parser.clear_lines()
        # rprint(parser.lines)
        parser.parse_lines()
        # rprint(parser.objects)
        self.rules = parser.objects


class Area:
    def __init__(self, x, y, sim_grid, rules):
        self.x = x
        self.y = y
        self.changed = False
        self.old_grid = [[-1] * 3 for _ in range(3)]
        self.grid = [[-1] * 3 for _ in range(3)]
        self.rules = rules

        # get neighbouring cells
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row = y + i
                new_col = x + j

                if 0 <= new_row < len(sim_grid) and 0 <= new_col < len(sim_grid[0]):
                    self.old_grid[i + 1][j + 1] = sim_grid[new_row][new_col]

    def id_at(self, xy):
        x, y = xy
        cell = self.old_grid[(y * -1) + 1][x + 1]
        if cell == -1:
            return -1
        return cell.id

    def name_at(self, x, y):
        cell = self.old_grid[(y * -1) + 1][x + 1]
        if cell == -1:
            return "None"
        return cell.name

    def place(self, xy, name):
        x, y = xy
        self.grid[(y * -1) + 1][x + 1] = Cell(
            name, self.x - x, self.y - y, self.rules[name]
        )
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
    def __init__(self, name, x, y, rules):
        self.name = name
        self.id = rules["id"]
        self.x = x
        self.y = y
        self.color = rules["color"]
        self.rules = rules["rules"]

    def __repr__(self):
        return str(self.id)

    def invert_rule(self, rule, axis):
        for i in range(len(rule)):
            if "cords" in rule[i]:
                match axis:
                    case "x":
                        rule[i]["cords"] = (
                            rule[i]["cords"][0] * -1,
                            rule[i]["cords"][1],
                        )
                    case "y":
                        rule[i]["cords"] = (
                            rule[i]["cords"][0],
                            rule[i]["cords"][1] * -1,
                        )
                    case _:
                        raise ValueError(f"Unknown axis '{axis}'")
        return rule

    def run_rule(self, rule, area):
        for command in rule:
            match command["type"]:
                case "ifidat":
                    if area.id_at(command["cords"]) != command["id"]:
                        return area, False
                case "change":
                    match command["id"]:
                        case 0:
                            name = "Empty"
                        case 1:
                            name = "Sand"
                        case 2:
                            name = "Water"
                        case 4:
                            name = "Lava"
                        case 5:
                            name = "Glass"
                        case 6:
                            name = "Ash"
                        case 7:
                            name = "Diamond"
                    area.place(command["cords"], name)
                case "symmetry":
                    if random.randint(0, 1):
                        inverted = self.invert_rule(rule[1:], command["axis"])
                        area, _ = self.run_rule(inverted, area)
                        return area, True
                case "done":
                    return area, True
                case _:
                    raise ValueError(f"Unknown command '{command['type']}'")

    def tick(self, area):
        done = False
        for rule in self.rules:
            if done:
                break
            area, done = self.run_rule(rule, area)
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
