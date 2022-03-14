import pygame

# Display
SCREEN_X = 1024
SCREEN_Y = 648
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)

# Tickrate
GAME_TICK = 60
clock = pygame.time.Clock()

# Boids rules
view_dist = 100
avoid_bias = 1.15
follow_bias = 0.1
center_bias = 0.3

# Coloure
BACKGROUND_COLOR = (20, 22, 30)
BOID_COLOR = (128, 56, 200)
HOIK_COLOR = (227, 72, 61)
OBSTACLE_COLOR = (86, 102, 130)

# Boid, Hoik and obstacle
BOID_AMOUNT = 80

BOID_SIZE = 5
HOIK_SIZE = 6
OBSTACLE_SIZE = 12

BOID_SPEED = 300
HOIK_SPEED = 250
