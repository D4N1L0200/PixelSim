from rich import print as rprint


class Parser:
    def __init__(self, file) -> None:
        self.file = file

    def load_file(self) -> None:
        with open(self.file) as file:
            self.lines = file.readlines()

    def clear_lines(self) -> None:
        out = []
        for line in self.lines:
            line = line[:-1]
            if line.startswith("#") or not line:
                continue
            else:
                out.append(line.strip())
        self.lines = out

    def parse_lines(self) -> None:
        self.objects = {}
        rule = []
        in_rule = False
        indent = 0
        for line in self.lines:
            if "element" in line:
                _, current_element, id, _ = line.split()
                self.objects[current_element] = {}
                self.objects[current_element]["id"] = int(id)
                self.objects[current_element]["rules"] = []
                indent += 1
            elif "color" in line:
                _, R, G, B = line.split()
                self.objects[current_element]["color"] = (int(R), int(G), int(B))
            elif "rule" in line:
                if any(i in "xy" for i in line.split()):
                    symmetry = line.split()[1]
                    rule.append({"type": "symmetry", "axis": symmetry})
                in_rule = True
                indent += 1
            elif "}" == line:
                if in_rule:
                    self.objects[current_element]["rules"].append(rule)
                    rule = []
                    in_rule = False
                indent -= 1
            elif in_rule:
                command, cell, x, y = line.split()
                rule.append(
                    {"type": command, "id": int(cell), "cords": (int(x), int(y))}
                )
            else:
                rprint(f"Unknown line: '{line}'")
        # print("Finishing indent:", indent)


if __name__ == "__main__":
    parser = Parser("cells.pixel")
    parser.load_file()
    # rprint(parser.lines)
    parser.clear_lines()
    # rprint(parser.lines)
    parser.parse_lines()
    rprint(parser.objects)


# def tick(self, area):
#     if area.id_at(0, 0) == 1:  # Sand
#         # Down
#         if area.id_at(0, -1) == 0:
#             area.place(0, 0, 0)
#             area.place(0, -1, 1)
#         if area.id_at(0, -1) == 1:
#             if random.randint(0, 1):  # Left Priority
#                 # Diagonal Down Left
#                 if area.id_at(-1, -1) == 0:
#                     area.place(0, 0, 0)
#                     area.place(-1, -1, 1)
#                 # Diagonal Down Right
#                 elif area.id_at(1, -1) == 0:
#                     area.place(0, 0, 0)
#                     area.place(1, -1, 1)
#             else:  # Right Priority
#                 # Diagonal Down Right
#                 if area.id_at(1, -1) == 0:
#                     area.place(0, 0, 0)
#                     area.place(1, -1, 1)
#                 # Diagonal Down Left
#                 elif area.id_at(-1, -1) == 0:
#                     area.place(0, 0, 0)
#                     area.place(-1, -1, 1)
#         # Down Water
#         if area.id_at(0, -1) == 2:
#             area.place(0, 0, 2)
#             area.place(0, -1, 1)
#         # Diagonal Down Left Water
#         elif area.id_at(-1, -1) == 2:
#             area.place(0, 0, 2)
#             area.place(-1, -1, 1)
#         # Diagonal Down Right Water
#         elif area.id_at(1, -1) == 2:
#             area.place(0, 0, 2)
#             area.place(1, -1, 1)
#     if area.id_at(0, 0) == 2:  # Water
#         # Down
#         if area.id_at(0, -1) == 0:
#             area.place(0, 0, 0)
#             area.place(0, -1, 2)
#         elif random.randint(0, 1):  # Left Priority
#             #  Left
#             if area.id_at(-1, 0) == 0:
#                 area.place(0, 0, 0)
#                 area.place(-1, 0, 2)
#             #  Right
#             elif area.id_at(1, 0) == 0:
#                 area.place(0, 0, 0)
#                 area.place(1, 0, 2)
#         else:  # Right Priority
#             #  Right
#             if area.id_at(1, 0) == 0:
#                 area.place(0, 0, 0)
#                 area.place(1, 0, 2)
#             #  Left
#             elif area.id_at(-1, 0) == 0:
#                 area.place(0, 0, 0)
#                 area.place(-1, 0, 2)
#     # if area.id_at(0, 0) == 3:  # Left Water
#     #     if area.id_at(0, -1) == 0:  # Down
#     #         area.place(0, 0, 0)
#     #         area.place(0, -1, 3)
#     #     elif area.id_at(-1, 0) == 0:  #  Left Empty
#     #         area.place(0, 0, 0)
#     #         area.place(-1, 0, 3)
#     #     elif area.id_at(-1, 0) == -1:  #  Left Wall
#     #         area.place(0, 0, 4)
#     #     elif area.id_at(-1, 0) == 4:  #  Left Water
#     #         area.place(0, 0, 4)
#     #         area.place(-1, 0, 3)
#     # if area.id_at(0, 0) == 4:  # Right Water
#     #     if area.id_at(0, -1) == 0:  # Down
#     #         area.place(0, 0, 0)
#     #         area.place(0, -1, 4)
#     #     elif area.id_at(1, 0) == 0:  #  Right Empty
#     #         area.place(0, 0, 0)
#     #         area.place(1, 0, 4)
#     #     elif area.id_at(1, 0) == -1:  #  Right Wall
#     #         area.place(0, 0, 3)
#     return area
