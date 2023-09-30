import time

import pygame

from simulator import Simulation

testing = False
if testing:
    width = 20
    height = 20
    cell_size = 25
    padding = 0
else:
    # width = 100
    # height = 100
    # cell_size = 5
    # padding = 0
    width = 50
    height = 50
    cell_size = 10
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
        sim.add_cell("Lava", get_mouse_pos())
    if pygame.mouse.get_pressed()[2]:  # Right Click
        sim.add_cell("Diamond", get_mouse_pos())

    window.fill(0)
    for iy, rowOfCells in enumerate(sim.grid):
        for ix, cell in enumerate(rowOfCells):
            pygame.draw.rect(
                window,
                cell.color,
                (
                    ix * (cell_size + padding) + padding,
                    iy * (cell_size + padding) + padding,
                    cell_size,
                    cell_size,
                ),
            )
    pygame.display.flip()
    pygame.display.set_caption(f"PixelSim - FPS: {round(clock.get_fps(), 2)}")
    clock.tick(60)
    if testing:
        time.sleep(0.2)
    sim.tick()

pygame.quit()
exit()
