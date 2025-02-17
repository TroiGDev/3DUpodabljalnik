import pygame
import sys
import polyRasterizer as ras
import numpy as np

pygame.init()
screen = pygame.display.set_mode((640, 480))
pixels = pygame.PixelArray(screen)

# Define triangle vertices
v1 = (200, 100, 200)
v2 = (100, 400, 200)
v3 = (400, 400, 200)

v4 = (250, 100, 100)
v5 = (150, 400, 200)
v6 = (450, 400, 300)

z_buffer = np.full((screen.get_width(), screen.get_height()), np.finfo(np.float32).max)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen and buffer
    screen.fill((255, 255, 255))
    z_buffer.fill(np.finfo(np.float32).max)
        
    # Draw triangle (like pygame.draw.polygon)
    ras.rasterize_triangle(pixels, z_buffer, v1, v2, v3, (255, 0, 0))

    ras.rasterize_triangle(pixels, z_buffer, v4, v5, v6, (0, 0, 255))
        
    pygame.display.flip()

del pixels
pygame.quit()