import pygame

from entity import Entity

class Player(Entity):
	def __init__(self):
		Entity.__init__(self)
		player_width =  128 * (pygame.display.Info().current_w * 1.0 / 800)
		player_height = 15 * (pygame.display.Info().current_h * 1.0 / 640) 
		self.image = pygame.Surface((player_width, player_height))
		self.image.convert()
		self.image.fill(pygame.Color("#FFFFFF"))
		self.rect = self.image.get_rect()
		self.rect.x = pygame.display.Info().current_w/2 - self.rect.width/2
		self.rect.y = pygame.display.Info().current_h - 50
		self.left = self.right = False
		
		self.speed = 5 * (pygame.display.Info().current_w * 1.0 / 800)
		self.score = 0
		self.lives = 2
			
	def update(self):
		if self.left and self.rect.left > 0:
			self.rect.x -= self.speed
		if self.right and self.rect.right < pygame.display.Info().current_w:
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
			
	def die(self):
		self.rect.x = pygame.display.Info().current_w/2 - self.rect.width/2
		self.rect.y = pygame.display.Info().current_h - 50
		self.lives -= 1