import vector
import settings
import random
import pygame

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
		self.box = pygame.draw.circle(settings.screen, self.color, (self.x, self.y), self.radius)

'''Boid'''
class Boid(Object, Move_object, Draw_object):
	def __init__(self, x, y, radius, speed, color):
		super().__init__(x, y, radius, speed, color)
		self.vector_pos = vector.Vector2(self.x, self.y)
		self.vector_vel = vector.random_vector()
		self.return_speed = self.speed / 4000
	
	def update(self):
		average_vel = vector.Vector2(0, 0)
		center_pos = vector.Vector2(0, 0)

		# Gives boid random movement
		random_vector = vector.random_vector()
		self.vector_vel += random_vector / 4	

		# Updates boids position vector
		self.vector_pos.x = self.x
		self.vector_pos.y = self.y

		# Loops through boids
		for other in boids:
			if self is not other:	# Excludes itself
				dist = vector.dist(self.vector_pos, other.vector_pos)	# Checks distance to other

				# Checks if boid is within view	
				if dist < settings.view_dist:
					# Checks direction to boids positon and velocity
					dir_pos = vector.direction_to(self.vector_pos, other.vector_pos)
					dir_vel = vector.direction_to(self.vector_vel, other.vector_vel)

					# Avoid boid
					self.avoid_boid(dir_pos, dist, settings.avoid_bias)

					# Adds together boids average direction 
					average_vel.x += dir_vel[0]
					average_vel.y += dir_vel[1]

					# Adds together boids average position
					center_pos.x += dir_pos[0]
					center_pos.y += dir_pos[1]

		# Loops through hoiks
		for hoik in hoiks:
			# Checks distance between boid and hoik
			dist = vector.dist(self.vector_pos, hoik.vector_pos)

			# Check if boid is within view
			if dist < settings.view_dist * 2:
				# Check direction between boid and hoik
				dir_pos = vector.direction_to(self.vector_pos, hoik.vector_pos)

				# Makes hoik follow boid
				boid_pos = vector.Vector2(0, 0)
				boid_pos.x -= dir_pos[0]
				boid_pos.y -= dir_pos[1]
				hoik.follow_direction(boid_pos, settings.follow_bias)

				# Check if hoik is within view
				if dist < settings.view_dist:
					# Make boid avoid hoik
					self.avoid_hoik(dir_pos, settings.avoid_bias)

					# Removes boid if caught by hoik
					if dist < 10:
						boids.remove(self)
			
		# Loops thru obstacles
		for obst in obstacles:
			# Checks distance between boid and obstacle
			dist = vector.dist(self.vector_pos, obst.vector_pos)
			# Avoid obstacle if within view
			if dist < settings.view_dist:
				dir_pos = vector.direction_to(self.vector_pos, obst.vector_pos)
				self.avoid_hoik(dir_pos, settings.avoid_bias * 0.2)

		self.follow_direction(average_vel, settings.follow_bias)	# Follow boids average direction
		self.follow_direction(center_pos, settings.center_bias)		# Follow boids center position
		self.out_of_bounds()										# Return boid after out of screen
		self.move()													# Update boids position
		self.draw()													# Draw boid

	# Makes boid avoid other boid
	def avoid_boid(self, dir, dist, bias):
		self.vector_vel.x -= (dir[0] / dist) * bias				# Updates selfs velocity
		self.vector_vel.y -= (dir[1] / dist) * bias
		self.vector_vel = vector.normalize(self.vector_vel)		# Normalizes velocity vector

	# Makes boid avoid hoik
	def avoid_hoik(self, dir, bias):
		self.vector_vel.x -= dir[0] * bias						# Updates selfs velocity
		self.vector_vel.y -= dir[1] * bias
		self.vector_vel = vector.normalize(self.vector_vel)		# Normalizes velocity vector
	
	# Makes boid follow a direction
	def follow_direction(self, dir, bias):
		dir = vector.normalize(dir)								# Normalizes direction vector
		self.vector_vel.x += dir.x * bias						# Updates selfs velocity
		self.vector_vel.y += dir.y * bias
		self.vector_vel = vector.normalize(self.vector_vel)		# Normalizes velocity vector

	# Makes boid return if they leave boundaries of screen
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

	def update(self):
		# Gives hoik random movement
		random_vector = vector.random_vector()
		self.vector_vel += random_vector / 4	

		# Updates position vector
		self.vector_pos.x = self.x
		self.vector_pos.y = self.y

		self.out_of_bounds()	# Retruns hoik if outside of screen
		self.move()				# Update Hoiks position
		self.draw()				# Draw hoik on screen
		
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
			# Selects which object to be spawn based on button pressed
			if event.key == pygame.K_b:		# Select boid with b
				place_boid, place_hoik, place_obstacle = True, False, False
			if event.key == pygame.K_h:		# Select hoik with h
				place_boid, place_hoik, place_obstacle = False, True, False
			if event.key == pygame.K_o:		# Select obstacle with o
				place_boid, place_hoik, place_obstacle = False, False, True
				
		# Spawn object on mousepress
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
	time_passed = settings.clock.tick(settings.GAME_TICK) / 1000.0

	# Set background colour
	settings.screen.fill(settings.BACKGROUND_COLOR)

	# Update boids, hoiks and obstacles
	for boid in boids:
		boid.update()
	for hoik in hoiks:
		hoik.update()
	for obst in obstacles:
		obst.draw()

	# Update display too show new frame
	pygame.display.update()