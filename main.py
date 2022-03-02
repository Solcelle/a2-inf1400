from asyncio.windows_events import NULL
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
	def __init__(self):
		self.x = 0
		self.y = 0
		self.height = 0
		self.width = 0
		self.color = (0, 0, 0)
		self.polygon = [(100,100), (300,100), (150,300)]

'''Move object'''
class Move_object():
	def __init__(self):
		self.speed = 0
		
	def move(self, left, right):
		self.x += -left * time_passed
		self.x += right * time_passed

'''Draw object'''
class Draw_object():
	def draw(self):
		self.box = pygame.draw.polygon(screen, self.color, self.polygon)

'''Boid'''
class Boid(Object, Move_object, Draw_object):
	def __init__(self):
		super().__init__()
		self.color = BOID_COLOR

boid1 = Boid()


# Game loop
while True:
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
	boid1.draw()

	# Update display too show new frame
	pygame.display.update()
