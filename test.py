from rich import print as rprint


# # def blockify(lines) -> list:
# #     blocks = []
# #     indent = 0
# #     for line in lines:
# #         if "{" in line:
# #             indent += 1
# #             blocks.append(line)
# #         if "}" in line:
# #             indent -= 1
# #             # blocks.append(line)
# #     print(indent)
# #     return blocks


# # lines = [
# #     "element Empty 0 {",
# #     "color 16 16 16",
# #     "}",
# #     "element Sand 1 {",
# #     "color 255 204 0",
# #     "rule {",
# #     "@ => _",
# #     "_    @",
# #     "}",
# #     "rule x {",
# #     "@  => _",
# #     "#_    #@",
# #     "}",
# #     "}",
# # ]

# # rprint(lines)
# # blocks = blockify(lines)
# # rprint(blocks)

# # [
# #     'element Empty 0 {',
# #     'color 16 16 16',
# #     '}',
# #     'element Sand 1 {',
# #     'color 255 204 0',
# #     'rule {',
# #     '@ => _',
# #     '_    @',
# #     '}',
# #     'rule x {',
# #     '@  => _',
# #     '#_    #@',
# #     '}',
# #     '}'
# # ]

# # [
# #     "element Empty 0 {",
# #     ["color 16 16 16"],
# #     "element Sand 1 {",
# #     [
# #         "color 255 204 0",
# #         "rule {",
# #         [
# #             "@ => _",
# #             "_    @",
# #         ],
# #         "rule x {",
# #         [
# #             "@  => _",
# #             "#_    #@",
# #         ],
# #     ],
# # ]


# # {
# #     "Empty": {"id": 0, "rules": [], "color": (16, 16, 16)},
# #     "Sand": {"id": 1, "rules": [], "color": (255, 204, 0)},
# # }


def parse_element_data(file_path):
    elements = {}

    with open(file_path, "r") as file:
        lines = file.readlines()

        current_element = None
        current_rule = None

        for line_idx, line in enumerate(lines):
            # Remove leading and trailing whitespaces
            line = line.strip()

            # Ignore empty lines and comment lines
            if not line or line.startswith("#"):
                continue

            if line == "}":
                if current_rule is not None:
                    # End of rule, reset current_rule
                    current_rule = None
                else:
                    # End of element definition, reset current_element
                    current_element = None
                continue

            if line.startswith("element "):
                # Extract element information
                _, name, id, _ = line.split(" ")
                # current_element = {"name": name, "id": int(id), "rules": []}
                current_element = {"id": int(id), "rules": []}
                elements[name] = current_element

            elif line.startswith("color "):
                # Extract element color information
                _, r, g, b = line.split(" ")
                current_element["color"] = (int(r), int(g), int(b))

            # elif line.startswith("rule"):
            #     # Create a new rule dictionary for the element
            #     rule_name = line.split(" ")[1] if " " in line else "default"
            #     current_rule = {"name": rule_name, "pattern": [], "replacement": []}
            #     current_element["rules"].append(current_rule)

            # elif line:
            #     # Extract pattern and replacement for the current rule
            #     pattern, _, replacement = line.partition("=>")
            #     current_rule["pattern"].append(pattern.strip())
            #     current_rule["replacement"].append(replacement.strip())

            elif line.startswith("rule"):
                # Create a new rule dictionary for the element
                # rule_name = line.split(" ")[1] if " " in line else "default"
                current_rule = {
                    # "name": rule_name,
                    "pattern": [["", "", ""], ["", "", ""], ["", "", ""]],
                    "replacement": [["", "", ""], ["", "", ""], ["", "", ""]],
                }
                current_element["rules"].append(current_rule)


            elif line:
                # Extract pattern and replacement for the current rule
                # pattern, _, replacement = line.partition("=>")
                # pattern_lines = pattern.split("\n")
                # replacement_lines = replacement.split("\n")

                # for i in range(3):
                #     for j in range(3):
                #         current_rule["pattern"][i][j] = (
                #             pattern_lines[i][j]
                #             if i < len(pattern_lines) and j < len(pattern_lines[i])
                #             else ""
                #         )
                #         current_rule["replacement"][i][j] = (
                #             replacement_lines[i][j]
                #             if i < len(replacement_lines)
                #             and j < len(replacement_lines[i])
                #             else ""
                #         )

    return elements


# Usage example:
file_path = "cells.pixel"
elements_data = parse_element_data(file_path)
rprint(elements_data)

# # Now you can access the data for each element easily:
# for element_name, element_info in elements_data.items():
#     print(f"Element: {element_name}")
#     print(f"ID: {element_info['id']}")
#     print(f"Color: {element_info['color']}")
#     for rule in element_info["rules"]:
#         print(f"Rule: {rule['name']}")
#         print(f"Pattern: {rule['pattern']}")
#         print(f"Replacement: {rule['replacement']}")

pattern = [["", "", ""], ["", "@", ""], ["", "_", ""]]
replacement = [["", "", ""], ["", "_", ""], ["", "@", ""]]