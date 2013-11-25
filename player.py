import pygame

from entity import Entity

class Player(Entity):
	def __init__(self):
		Entity.__init__(self)
		player_width =  128 * (pygame.display.Info().current_w * 1.0 / 800)
		player_height = 15 * (pygame.display.Info().current_h * 1.0 / 640) 
		self.set_size(player_width, player_height, pygame.display.Info().current_w/2 - player_width/2, pygame.display.Info().current_h - 50)

		self.left = self.right = False
		self.speed = 5 * (pygame.display.Info().current_w * 1.0 / 800)
		self.score = 0
		self.lives = 2
		
		#This is the list of possible sizes
		self.sizes_w = [112, 128, 156]
		
		#This is the current size of the player, this is the index of self.sizes_w[]
		#so if self.size = 1, then the width of the player will be sizes_w[1]
		self.size = 1
		
	def set_size(self, w, h, x, y):
		#used when creating the player or resizing him
		self.image = pygame.Surface((w, h))
		self.image.convert()
		self.image.fill(pygame.Color("#FFFFFF"))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
	def update(self, items, sound_factory):
		#input left and right
		if self.left and self.rect.left > 0:
			self.rect.x -= self.speed
		if self.right and self.rect.right < pygame.display.Info().current_w:
			self.rect.x += self.speed
			
		items_collisions = pygame.sprite.spritecollide(self, items, True)
		for i in items_collisions:
			#item type 1 increases the player's size
			if i.type == 1:
				self.score += 50
				if self.size != 2:
					player_width =  self.sizes_w[self.size + 1] * (pygame.display.Info().current_w * 1.0 / 800)
					player_height = 15 * (pygame.display.Info().current_h * 1.0 / 640) 
					self.rect.x -= ((player_width - self.rect.width) / 2)
					self.set_size(player_width, player_height, self.rect.x, self.rect.y)
					self.size += 1
					sound_factory.play_player_size_increase()
			#item type 2 reduces the size
			elif i.type == 2:
				self.score -= 50
				if self.size != 0:
					player_width =  self.sizes_w[self.size - 1] * (pygame.display.Info().current_w * 1.0 / 800)
					player_height = 15 * (pygame.display.Info().current_h * 1.0 / 640) 
					self.rect.x -= ((player_width - self.rect.width) / 2)
					self.set_size(player_width, player_height, self.rect.x, self.rect.y)
					self.size -= 1
					sound_factory.play_player_size_decrease()
			
	def input(self, type, key):
		#input received from breakout.py
		if type == pygame.KEYDOWN and key == pygame.K_LEFT:
			self.left = True
		if type == pygame.KEYDOWN and key == pygame.K_RIGHT:
			self.right = True
			
		if type == pygame.KEYUP and key == pygame.K_LEFT:
			self.left = False
		if type == pygame.KEYUP and key == pygame.K_RIGHT:
			self.right = False
			

			
	def die(self):
		self.rect.x = pygame.display.Info().current_w/2 - self.rect.width/2
		self.rect.y = pygame.display.Info().current_h - 50
		self.lives -= 1