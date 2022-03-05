from tkinter import S
from unicodedata import is_normalized
import vector
import random
import math
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
	def __init__(self, x: float, y: float, radius, speed, color):
		self.x = x
		self.y = y
		self.radius = radius
		self.speed = speed
		self.color = color

'''Move object'''
class Move_object():
	def move(self):
		self.x += self.vector_vel.x * self.speed * time_passed
		self.y += self.vector_vel.y * self.speed * time_passed

'''Draw object'''
class Draw_object():
	def draw(self):
		self.box = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

view_dist = 100
avoid_bias = 1
follow_bias = 0.02
center_bias = 0.02


'''Boid'''
class Boid(Object, Move_object, Draw_object):
	def __init__(self, x, y, radius, speed, color):
		super().__init__(x, y, radius, speed, color)
		self.vector_pos = vector.Vector2(self.x, self.y)
		self.vector_vel = vector.random_vector()
		self.return_speed = self.speed / 8000
	
	def update_boid(self):
		random_vector = vector.random_vector()
		self.vector_vel += random_vector / 4
		self.vector_pos.x = self.x
		self.vector_pos.y = self.y
		
		center_pos = vector.Vector2(0, 0)
		average_vel = vector.Vector2(0, 0)
		for boid in boids:
			if self is not boid:
				dist = vector.dist(self.vector_pos, boid.vector_pos)
				if dist < view_dist:
					angle_pos = vector.direction_to(self.vector_pos, boid.vector_pos)
					angle_vel = vector.direction_to(self.vector_vel, boid.vector_vel)

					self.avoid_boid(angle_pos, dist)
					average_vel.x += angle_vel[0]
					average_vel.y += angle_vel[1]
					center_pos.x += angle_pos[0]
					center_pos.y += angle_pos[1]

		self.follow_boid(average_vel)
		self.center_boid(center_pos)
			
		self.move()
		self.draw()
		self.out_of_bounds()

	# Makes boid avoid nearby boid
	def avoid_boid(self, angle, dist):
		self.vector_vel.x -= (angle[0] / dist) * avoid_bias
		self.vector_vel.y -= (angle[1] / dist) * avoid_bias
		self.vector_vel = vector.normalize(self.vector_vel)
	
	# Makes boid follow nearby boid
	def follow_boid(self, average_val):
		self.vector_vel.x += average_val.x * follow_bias
		self.vector_vel.y += average_val.y * follow_bias
		self.vector_vel = vector.normalize(self.vector_vel)
	
	def center_boid(self, center_pos):
		self.vector_vel.x += center_pos.x * center_bias
		self.vector_vel.y += center_pos.y * center_bias
		self.vector_vel = vector.normalize(self.vector_vel)
	

	# Makes boids return if they leave boundaries of screen
	def out_of_bounds(self):
		if self.x < 0:
			self.vector_vel.x += self.return_speed
		if self.x > SCREEN_X:
			self.vector_vel.x -= self.return_speed
		if self.y < 0:
			self.vector_vel.y += self.return_speed
		if self.y > SCREEN_Y:
			self.vector_vel.y -= self.return_speed
		self.vector_vel = vector.normalize(self.vector_vel)

# Create boids
boids = []
i = 0
while i < 100:
	boids.append(Boid(SCREEN_X * random.random(), SCREEN_Y * random.random(), 5, 300, BOID_COLOR))
	i += 1

#boids.append(Boid(SCREEN_X * random.random(), SCREEN_Y * random.random(), 50, 300, [255, 0, 0]))

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

	# Update boids direction
	for self in boids:
		self.update_boid()

	# Update display too show new frame
	pygame.display.update()
