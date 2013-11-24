import pygame, math

from entity import Entity

class Block(Entity):
	def __init__(self, x, y, WIDTH, HEIGHT):
		Entity.__init__(self)
		self.image = pygame.Surface((36 * (WIDTH * 1.0 / 800), 18 * (HEIGHT * 1.0 / 640)))
		self.image.convert()
		self.image.fill(pygame.Color("#00FF00"))
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
	