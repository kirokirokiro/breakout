import pygame
import math

from entity import Entity
from player import Player
from ball import Ball
from block import Block

#Screen settings
#WIDTH = 800
#HEIGHT = 640
#DISPLAY = (WIDTH, HEIGHT)
'''base width is 800
base height is 640
'''

DEPTH = 32
FLAGS = 0

class Game():
	entities = None
	blocks = None
	player = None
		
	def __init__(self, WIDTH, HEIGHT):
		self.WIDTH = WIDTH
		self.HEIGHT = HEIGHT
		self.DISPLAY = (self.WIDTH, self.HEIGHT)	
		#Screen settings
		self.screen = pygame.display.set_mode(self.DISPLAY, FLAGS, DEPTH)
		pygame.display.set_caption("BREAKOUT ULTIMATE")
		
		#Background
		self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
		self.background.convert()
		self.background.fill(pygame.Color("#000000"))	
		
		#FONT
		pygame.font.init()
		font_path = "./font.ttf"
		font_size = 16
		self.fontObj = pygame.font.SysFont("courier", font_size)
		
		#Entities list (player, balls, blocks)
		self.entities = pygame.sprite.Group()
		self.blocks = pygame.sprite.Group()
		self.player = Player(self.WIDTH, self.HEIGHT)
		self.ball = Ball(self.WIDTH , self.HEIGHT)
		self.entities.add(self.player)
		self.entities.add(self.ball)
		
		#Calculating the space between each block, what could possibly go wrong?
		horizontal_spacing = 50 * (self.WIDTH * 1.0 / 800)
		vertical_spacing = 40 * (self.HEIGHT * 1.0 / 640)
		for column in range (0, 14):
			for row in range (0, 5):
				new_block = Block(column * horizontal_spacing + 60, row * vertical_spacing + 50, self.WIDTH, self.HEIGHT)
				self.entities.add(new_block)
				self.blocks.add(new_block)
				
		#Game states
		self.game_over = False
		
		
	def update_stuff(self):		
		#Keyboard and mouse events
		for e in pygame.event.get():
			#Clicking the cross to quit
			if e.type == pygame.QUIT:
				raise SystemExit, "QUIT"
			
			#Player input
			if (e.type == pygame.KEYDOWN or e.type == pygame.KEYUP):
				self.player.input(e.type, e.key)
				
			if e.type == pygame.KEYDOWN and e.key == pygame.K_v:
				if self.WIDTH == 1440:
					self.WIDTH = 800
					self.HEIGHT = 640
					self.DISPLAY = (self.WIDTH, self.HEIGHT)	
					#Screen settings
					self.screen = pygame.display.set_mode(self.DISPLAY, FLAGS, DEPTH)
					self.__init__(self.WIDTH, self.HEIGHT)
				elif self.WIDTH == 800:
					self.WIDTH = 1440
					self.HEIGHT = 900
					self.DISPLAY = (self.WIDTH, self.HEIGHT)	
					self.screen = pygame.display.set_mode(self.DISPLAY, FLAGS, DEPTH)
					self.__init__(self.WIDTH, self.HEIGHT)

			if self.game_over and e.type == pygame.KEYDOWN:
				self.__init__(self.WIDTH, self.HEIGHT)
				
		if self.game_over is False:

			#Entities update
			self.player.update()
			
			#If ball.update() returns 0 it means it has hit the bottom of the screen and the player has less than 0 lives left
			if self.ball.update(self.WIDTH, self.HEIGHT, self.player, self.blocks, self.entities) == 0:
				self.game_over = True

	
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
		
		#Draw game over message
		if self.game_over:
			game_over_text = self.fontObj.render("Game over :( Press any key to restart", 1, (255,255,255))
			self.screen.blit(game_over_text, (self.WIDTH/2 - game_over_text.get_rect().width/2, self.HEIGHT/2))

		pygame.display.flip()	

def main():
	#Initiating Pygame
	pygame.init()
	'''
	WIDTH = 1440
	HEIGHT = 900
	DISPLAY = (WIDTH, HEIGHT)	
	#Screen settings
	screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
	pygame.display.set_caption("BREAKOUT ULTIMATE")
'''
		
	#Starting the game's main timer
	timer = pygame.time.Clock()
	done = False
	game = Game(1440, 900)
	
	while not done:
		game.update_stuff()
		game.draw()
		timer.tick(60)
		
	pygame.quit()
			
if __name__ == "__main__":
	main()