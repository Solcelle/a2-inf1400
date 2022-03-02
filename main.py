import pygame
pygame.init

# Create screen
SCREEN_RES = (1280, 720)
screen = pygame.display.set_mode((SCREEN_RES), 0, 32)

GAME_TICK = 60
CLOCK = pygame.time.Clock()

# Game coloure
BACKGROUND_COLOR = (20, 22, 30)

# Game loop
while True:
	events = pygame.event.get()

	# Sets amount of updates per second
	time_passed = CLOCK.tick(GAME_TICK) / 1000.0

	# Set background color
	screen.fill(BACKGROUND_COLOR)

	# Update display too show new frame
	pygame.display.update()
