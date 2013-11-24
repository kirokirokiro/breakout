import pygame
import math

from entity import Entity
from player import Player
from ball import Ball
from block import Block
from item import Item
from sound import Sound

'''base width is 800
base height is 640
'''


DEPTH = 32
FLAGS = 0

class Game():
	entities = None
	blocks = None
	player = None
	items = None
	sound_factory = None
	
	def __init__(self, window_width, window_height):
		#Screen settings
		self.screen = pygame.display.set_mode((window_width, window_height), FLAGS, DEPTH)
		pygame.display.set_caption("BREAKOUT ULTIMATE")
		
		#Background
		self.background = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h))
		self.background.convert()
		self.background.fill(pygame.Color("#000000"))	
		
		#Font
		pygame.font.init()
		font_path = "./font.ttf"
		font_size = 16
		self.fontObj = pygame.font.SysFont("courier", font_size)
		
		#Entities list (player, balls, blocks)
		self.entities = pygame.sprite.Group()
		self.items = pygame.sprite.Group()
		self.blocks = pygame.sprite.Group()
		self.player = Player()
		self.ball = Ball()
		self.entities.add(self.player)
		self.entities.add(self.ball)
		
		self.sound_factory = Sound()
		
		#Calculating the space between each block
		horizontal_spacing = 50 * (pygame.display.Info().current_w * 1.0 / 800)
		vertical_spacing = 40 * (pygame.display.Info().current_h * 1.0 / 640)
		for column in range (0, 14):
			for row in range (0, 5):
				new_block = Block(column * horizontal_spacing + 60, row * vertical_spacing + 50, pygame.display.Info().current_w, pygame.display.Info().current_h)
				self.entities.add(new_block)
				self.blocks.add(new_block)
				
		#Game states
		self.game_over = False
		self.menu = True
		self.pause = True
		
		
	def update_stuff(self):	
		#Keyboard and mouse events
		for e in pygame.event.get():
			#Clicking the cross to quit
			if e.type == pygame.QUIT:
				raise SystemExit, "QUIT"
			
			#All the input is sent to the Player object
			if (e.type == pygame.KEYDOWN or e.type == pygame.KEYUP):
				self.player.input(e.type, e.key)
			
			#Pressing V switch between 2 resolution. We could add a menu to choose the resolution later
			if e.type == pygame.KEYDOWN and e.key == pygame.K_v:
				if pygame.display.Info().current_w == 1200:	
					self.__init__(800, 640)
					
				elif pygame.display.Info().current_w == 800:
					self.__init__(1200, 960)

			#pressing B mute the sound
			if e.type == pygame.KEYDOWN and e.key == pygame.K_n:
				self.ball.change_volume()
				
			#If player has no life left, he can press SPACE to restart
			if self.game_over and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
				self.__init__(pygame.display.Info().current_w, pygame.display.Info().current_h)
			
			#If game is paused, player can press SPACE to unpause
			if self.pause and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
				self.pause = False
				
			elif not self.pause and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
				self.pause = True
				
		if not self.game_over and not self.pause:
			#Entities update
			self.player.update(self.items, self.sound_factory)
			self.items.update()
			
			#If ball.update() returns 1 it means the player has died
			if self.ball.update(self.player, self.blocks, self.entities, self.items, self.sound_factory) == 1:
					self.player.die()
					self.ball.die()
					if self.player.lives < 0:
						self.game_over = True
					else:
						self.pause = True
						print "pause = ", self.pause

	def draw(self):
		#Graphics drawing
		self.screen.blit(self.background, (0, 0))
		self.entities.draw(self.screen)
		
		#Draw the score
		score_text = self.fontObj.render(str(self.player.score) + " points", 1, (255,255,255))
		self.screen.blit(score_text, (10, 5))
		
		#Draw lives
		lives_text = self.fontObj.render(str(self.player.lives) + " lives", 1, (255,255,255))
		self.screen.blit(lives_text, (10, 25))
		
		#Draw game over and pause message
		if self.game_over:
			game_over_text = self.fontObj.render("Game over :( Press space to restart", 1, (255,255,255))
			self.screen.blit(game_over_text, (pygame.display.Info().current_w/2 - game_over_text.get_rect().width/2, pygame.display.Info().current_h/2))
		
		if self.pause:
			game_over_text = self.fontObj.render("Press space to start", 1, (255,255,255))
			self.screen.blit(game_over_text, (pygame.display.Info().current_w/2 - game_over_text.get_rect().width/2, pygame.display.Info().current_h/2))

		pygame.display.flip()	

def main():
	#Initiating Pygame
	pygame.init()
		
	#Starting the game's main timer
	timer = pygame.time.Clock()
	done = False
	game = Game(1200, 960)
	
	while not done:
		game.update_stuff()
		game.draw()
		timer.tick(60)
		
	pygame.quit()
			
if __name__ == "__main__":
	main()