import vector
import settings
import random
import pygame
pygame.init()

screen = pygame.display.set_mode((settings.SCREEN_X, settings.SCREEN_Y), 0, 32)
clock = pygame.time.Clock()

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

'''Boid'''
class Boid(Object, Move_object, Draw_object):
	def __init__(self, x, y, radius, speed, color):
		super().__init__(x, y, radius, speed, color)
		self.vector_pos = vector.Vector2(self.x, self.y)
		self.vector_vel = vector.random_vector()
		self.return_speed = self.speed / 5000
	
	def update(self):
		average_vel = vector.Vector2(0, 0)
		center_pos = vector.Vector2(0, 0)

		# Gives boid random movement
		random_vector = vector.random_vector()
		self.vector_vel += random_vector / 4	

		# Updates boids position vector
		self.vector_pos.x = self.x
		self.vector_pos.y = self.y

		# Loops thru all boids and hoiks
		for other in boids:
			if self is not other:	# Excludes itself
				dist = vector.dist(self.vector_pos, other.vector_pos)	# Checks distance to other

				# Checks if other is within view	
				if dist < settings.view_dist:
					dir_pos = vector.direction_to(self.vector_pos, other.vector_pos)

					# If self is boid
					if not isinstance(self, Hoik):
						# If other is boid
						if isinstance(other, self.__class__):	
							# Checks direction to others positon and velocity
							dir_vel = vector.direction_to(self.vector_vel, other.vector_vel)
							self.avoid_boid(dir_pos, dist, settings.avoid_bias)	# Avoid boid
							# Updates boids velocity
							average_vel.x += dir_vel[0]
							average_vel.y += dir_vel[1]
							center_pos.x += dir_pos[0]
							center_pos.y += dir_pos[1]
						# If other is hoik
						else:
							print("here")
							self.avoid_hoik(dir_pos, settings.avoid_bias)

					# If self is hoik
					else:
						# If other is hoik
						if isinstance(other, Hoik):
							# Updates hoiks velocity
							
							self.avoid_hoik(dir_pos, settings.avoid_bias)
						# If other is boid
						else:
							# Updates 
							center_pos.x += dir_pos[0]
							center_pos.y += dir_pos[1]
							if dist < 4:
								boids.remove

		# Makes boids avoid obstacles
		for obst in obstacles:
			dist = vector.dist(self.vector_pos, obst.vector_pos)
			if dist < settings.view_dist:
				dir_pos = vector.direction_to(self.vector_pos, obst.vector_pos)
				self.avoid_hoik(dir_pos, settings.avoid_bias * 0.2)

		self.follow_object(average_vel, settings.follow_bias)		# Follow boids average direction
		self.follow_object(center_pos, settings.center_bias)		# Follow boids center position
		self.out_of_bounds()										# Return after out of screen
		self.move()
		self.draw()

	# Makes boid avoid direction
	def avoid_boid(self, dir, dist, bias):
		self.vector_vel.x -= (dir[0] / dist) * bias
		self.vector_vel.y -= (dir[1] / dist) * bias
		self.vector_vel = vector.normalize(self.vector_vel)

	# Makes boid avoid hoik
	def avoid_hoik(self, dir, bias):
		self.vector_vel.x -= dir[0] * bias
		self.vector_vel.y -= dir[1] * bias
		self.vector_vel = vector.normalize(self.vector_vel)
	
	# Makes boid follow direction
	def follow_object(self, dir, bias):
		dir = vector.normalize(dir)
		self.vector_vel.x += dir.x * bias
		self.vector_vel.y += dir.y * bias
		self.vector_vel = vector.normalize(self.vector_vel)

	# Makes boids return if they leave boundaries of screen
	def out_of_bounds(self):
		if self.x < 0:
			self.vector_vel.x += self.return_speed
		if self.x > settings.SCREEN_X:
			self.vector_vel.x -= self.return_speed
		if self.y < 0:
			self.vector_vel.y += self.return_speed
		if self.y > settings.SCREEN_Y:
			self.vector_vel.y -= self.return_speed
		self.vector_vel = vector.normalize(self.vector_vel)

'''Hoik'''
class Hoik(Boid):
	def __init__(self, x, y, radius, speed, color):
		super().__init__(x, y, radius, speed, color)
		
'''Obstacles'''
class Obstacle(Object, Draw_object):
	def __init__(self, x, y, radius, speed, color):
		super().__init__(x, y, radius, speed, color)
		self.vector_pos = vector.Vector2(self.x, self.y)

# Create boids
i = 0
boids, hoiks, obstacles = [], [], []
place_boid, place_hoik, place_obstacle = False, False, False
while i < settings.BOID_AMOUNT:
	boids.append(Boid(settings.SCREEN_X * random.random(), settings.SCREEN_Y * random.random(), settings.BOID_SIZE, settings.BOID_SPEED, settings.BOID_COLOR))
	i += 1

# Game loop
while True:
	# Check for events
	events = pygame.event.get()
	for event in events:
		# Quits game if window is closed
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			# Quit game with ESC
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			# Selects which object to spawn based on button pressed
			if event.key == pygame.K_b:
				place_boid, place_hoik, place_obstacle = True, False, False
			if event.key == pygame.K_h:
				place_boid, place_hoik, place_obstacle = False, True, False
			if event.key == pygame.K_o:
				place_boid, place_hoik, place_obstacle = False, False, True
				
		# Spawn object with mousepress
		if event.type == pygame.MOUSEBUTTONUP:
			mouse_pos = pygame.mouse.get_pos()
			# Spawn Boid
			if place_boid:
				boids.append(Boid(mouse_pos[0], mouse_pos[1], settings.BOID_SIZE, settings.BOID_SPEED, settings.BOID_COLOR))
			# Spawn Hoik
			if place_hoik:
				hoiks.append(Hoik(mouse_pos[0], mouse_pos[1], settings.HOIK_SIZE, settings.HOIK_SPEED, settings.HOIK_COLOR))
			# Spawn obstacle
			if place_obstacle:
				obstacles.append(Obstacle(mouse_pos[0], mouse_pos[1], settings.OBSTACLE_SIZE, 0, settings.OBSTACLE_COLOR))

	# Sets amount of updates per second
	time_passed = clock.tick(settings.GAME_TICK) / 1000.0

	# Set background colour
	screen.fill(settings.BACKGROUND_COLOR)

	# Update boids, hoiks and obstacles
	for boid in boids:
		boid.update()
	for hoik in hoiks:
		hoik.update()
	for obst in obstacles:
		obst.draw()

	# Update display too show new frame
	pygame.display.update()