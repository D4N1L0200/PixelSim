import time

import pygame

from simulator import Simulation

testing = True
if testing:
    width = 10
    height = 10
    cell_size = 50
    padding = 0
else:
    width = 100
    height = 100
    cell_size = 5
    padding = 0
sim = Simulation(width, height)

pygame.init()
window = pygame.display.set_mode(
    (
        width * (cell_size + padding) + padding,
        height * (cell_size + padding) + padding,
    )
)
clock = pygame.time.Clock()


def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    if ((x % (padding + cell_size)) - padding < 0) or (
        (y % (padding + cell_size)) - padding < 0
    ):
        return -1, -1
    row = y // (padding + cell_size)
    col = x // (padding + cell_size)
    return col, row


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:  # Left Click
        sim.add_cell(1, get_mouse_pos())
    if pygame.mouse.get_pressed()[2]:  # Right Click
        sim.add_cell(2, get_mouse_pos())

    window.fill(0)
    for iy, rowOfCells in enumerate(sim.grid):
        for ix, cell in enumerate(rowOfCells):
            if cell.id == 0:
                color = (16, 16, 16)
            elif cell.id == 1:
                color = (255, 255, 255)
            elif cell.id == 2:
                color = (0, 0, 255)
            else:
                color = (255, 0, 0)
            pygame.draw.rect(
                window,
                color,
                (
                    ix * (cell_size + padding) + padding,
                    iy * (cell_size + padding) + padding,
                    cell_size,
                    cell_size,
                ),
            )
    pygame.display.flip()
    clock.tick(240)
    if testing:
        time.sleep(0.2)
    sim.tick()

pygame.quit()
exit()
