import pygame, random
from entity import Entity

class Item(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		item_width = 18 * (pygame.display.Info().current_w *  1.0 / 800)
		item_height = 18 * (pygame.display.Info().current_h *  1.0 / 640)
		self.image = pygame.Surface((item_width, item_height))
		self.image.convert()
		self.image.fill(pygame.Color("#FF00FF"))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.speed = 3 * (pygame.display.Info().current_h * 1.0 / 800)
		
	def update(self):
		self.rect.y += self.speed