import pygame

from entity import Entity

class Player(Entity):
	def __init__(self, WIDTH, HEIGHT):
		Entity.__init__(self)
		self.image = pygame.Surface((128 * (WIDTH * 1.0 / 800), 15))
		self.image.convert()
		self.image.fill(pygame.Color("#FFFFFF"))
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH/2 - self.rect.width/2
		self.rect.y = HEIGHT - 50
		self.left = self.right = False
		
		self.speed = 7 * (WIDTH * 1.0 / 800)
		print "player speed =", self.speed
		self.score = 0
		self.lives = 0
			
	def update(self):
		if self.left:
			self.rect.x -= self.speed
		if self.right:
			self.rect.x += self.speed
			
	def input(self, type, key):
		if type == pygame.KEYDOWN and key == pygame.K_LEFT:
			self.left = True
		if type == pygame.KEYDOWN and key == pygame.K_RIGHT:
			self.right = True
			
		if type == pygame.KEYUP and key == pygame.K_LEFT:
			self.left = False
		if type == pygame.KEYUP and key == pygame.K_RIGHT:
			self.right = False
			
		if type == pygame.KEYDOWN and key == pygame.K_ESCAPE:
			raise SystemExit, "ESCAPE"
			
	def die(self, WIDTH, HEIGHT):
		self.rect.x = WIDTH/2 - self.rect.width/2
		self.rect.y = HEIGHT - 50
		self.lives -= 1