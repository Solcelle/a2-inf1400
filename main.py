import random
import math
from turtle import distance
import pygame
pygame.init()

# Create screen
SCREEN_X = 1024
SCREEN_Y = 648
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)

GAME_TICK = 60
clock = pygame.time.Clock()

# Game coloure
BACKGROUND_COLOR = (20, 22, 30)
BOID_COLOR = (128, 56, 200)


'''Object'''
class Object():
	def __init__(self, x, y, radius, speed, color):
		self.x = x
		self.y = y
		self.radius = radius
		self.speed = speed
		self.color = color

'''Move object'''
class Move_object():
	def move(self):
		self.x += self.dir_horiz * self.speed * time_passed
		self.y += self.dir_verti * self.speed * time_passed

	def move_to_target(self, target_x, target_y):
		radians = math.atan2(target_y - self.y, target_x - self.x)
		self.dir_horiz = math.cos(radians)
		self.dir_verti = math.sin(radians)

'''Draw object'''
class Draw_object():
	def draw(self):
		self.box = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

'''Boid'''
class Boid(Object, Move_object, Draw_object, pygame.math.Vector2):
	def __init__(self, x, y, radius, speed, color):
		super().__init__(x, y, radius, speed, color)
		self.dir_horiz = 0
		self.dir_verti = 0
		self.Vector2 = tuple[self.x, self.y]
	
	def direction_to_object(self, other):
		radians = math.atan2(other.y - self.y, other.x - self.x)
		horizontal = math.cos(radians)
		vertical = math.sin(radians)
		return (horizontal, vertical)

	def distance_to_object(self, other):
		return pygame.math.Vector2.distance_to(self, other)
	
	def avoid_boids(self):
		for boid in boids:
			distance = self.distance_to_object(boid)
			if distance > 1 and distance < 10:
				horizontal, vertical = self.direction_to_object(boid)
				self.dir_horiz -= horizontal
				self.dir_verti -= vertical


# Create boids
boids = []
i = 0
while i < 10:
	boids.append(Boid(200 + 400 * random.random(), 200 + 400 * random.random(), 5, 200, BOID_COLOR))
	i += 1

boid_target = Boid(800, 300, 5, 600, (255, 0, 0))

# Game loop
while True:
	# Check for events
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()

	# Sets amount of updates per second
	time_passed = clock.tick(GAME_TICK) / 1000.0

	# Set background color
	screen.fill(BACKGROUND_COLOR)


	mouse_x, mouse_y = pygame.mouse.get_pos()
	boid_target.move_to_target(mouse_x, mouse_y)
	boid_target.move()
	boid_target.draw()


	# Update boids direction
	for boid in boids:
		if boid.distance_to_object(boid_target) < 200:
			boid.move_to_target(boid_target.x, boid_target.y)
		
		boid.avoid_boids()
		boid.direction_to_object(boid_target)
		boid.move()
		boid.draw()



	# Update display too show new frame
	pygame.display.update()
