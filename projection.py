import pygame
import numpy as np
from math import sin, cos

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Screen setup
WIDTH, HEIGHT = 800, 600
pygame.init()
pygame.display.set_caption("3D Projection in Pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Cube setup
scale = 100
circle_pos = [WIDTH // 2, HEIGHT // 2]  # Center of screen
angle = 0

# Cube vertices
points = [
    np.matrix([-1, -1,  1]),
    np.matrix([ 1, -1,  1]),
    np.matrix([ 1,  1,  1]),
    np.matrix([-1,  1,  1]),
    np.matrix([-1, -1, -1]),
    np.matrix([ 1, -1, -1]),
    np.matrix([ 1,  1, -1]),
    np.matrix([-1,  1, -1])
]

# Simple orthographic projection matrix
projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

projected_points = [[0, 0] for _ in range(len(points))]

def connect_points(i, j, points):
    pygame.draw.line(screen, BLACK, (int(points[i][0]), int(points[i][1])), (int(points[j][0]), int(points[j][1])))

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Rotation matrices
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle),  cos(angle), 0],
        [0, 0, 1]
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle),  cos(angle)]
    ])

    # Apply transformations
    for i, point in enumerate(points):
        rotated = rotation_z @ point.reshape((3, 1))
        rotated = rotation_y @ rotated
        rotated = rotation_x @ rotated

        projected2d = projection_matrix @ rotated

        x = int(projected2d[0, 0] * scale + circle_pos[0])
        y = int(projected2d[1, 0] * scale + circle_pos[1])

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, RED, (x, y), 5)

    # Connect cube edges
    for i in range(4):
        connect_points(i, (i + 1) % 4, projected_points)
        connect_points(i + 4, ((i + 1) % 4) + 4, projected_points)
        connect_points(i, i + 4, projected_points)

    pygame.display.update()
    angle += 0.01

pygame.quit()
