import pygame, math, time

from entity import Entity

class Ball(Entity):
	def __init__(self, WIDTH, HEIGHT):
		Entity.__init__(self)
		self.size_width = self.size_height = 18 * (WIDTH * 1.0 / 800)
		#self.size_height = 18 * (HEIGHT * 1.0 / 640)
		self.image = pygame.Surface((self.size_width, self.size_height ))
		self.image.convert()
		self.image.fill(pygame.Color("#FFFFFF"))
		self.rect = self.image.get_rect()
		self.x = WIDTH/2 - self.rect.width/2
		self.y = HEIGHT - 80
		self.rect.x = self.nextX = self.x
		self.rect.y = self.nextY = self.y
		self.speed = ((WIDTH * HEIGHT) / 512000) * 7.0
		print (WIDTH * HEIGHT)
		#direction is an angle. In this code 90 is to the right, 270 is to the left, 180 is up and 360 is down
		self.direction = 180
		self.time_last_collide_up_down = 0
		self.time_last_collide_left_right = 0
		
	def update(self, WIDTH, HEIGHT, player, blocks, entities):
		#first it converts the direction angle to radian
		rad = self.direction * math.pi/180
		
		#then is calculates the next Y and X coordinates that the ball will reach with this angle
		self.nextX += self.speed * math.sin(rad)
		self.nextY += self.speed * math.cos(rad)
		
		#here is gets complicated, fasten your seatbelt, I got a headache trying to figure this out. I couldn't find a code on the internet that is that precise and "realistic"
		#It loops on all the blocks...
		for block in blocks:
			#and look for one that will contain nextX and nextY AND all the corners of the ball
			#ie we look for a block that will collide with the ball (it will "contain" at least one corner of the ball)
			if block.rect.collidepoint(self.nextX, self.nextY) or block.rect.collidepoint(self.nextX + self.rect.width, self.nextY)  or block.rect.collidepoint(self.nextX + self.rect.width, self.nextY + self.rect.height)  or block.rect.collidepoint(self.nextX, self.nextY + self.rect.height):
				print self.rect.top >= block.rect.bottom
				#once we found a colliding block, we try to find out if it will collide from which side it will collide
				#if RIGHT NOW the ball is over it or under it, then it means it will collide from these sides
				#because it will collide in 1/60th of a second it's precise 
				if self.rect.top >= block.rect.bottom or self.rect.bottom <= block.rect.top:
					self.collide_up_down()

				#else if the ball is on the left or on the right, it will collide from these directions
				else:
					self.collide_left_right()
				#we simply use the methods that will calculate the angles after the collision
				
				#the block is removed from the 2 lists
				blocks.remove(block)
				entities.remove(block)
				player.score += 100
				print "Score =", player.score

		#now we calculate the X and Y coordinates again after the collision with the blocks
		#if it didn't collide then it does the exact same calculation
		rad = self.direction * math.pi/180		
		self.x += self.speed * math.sin(rad)
		self.y += self.speed * math.cos(rad)

		#we have to calculate x and y of the object (self.x and self.y) and only then we can change the x and y of the rectangle (self.rect)
		#because the rectangle's coordinates are rounded
		self.rect.y = self.y
		self.rect.x = self.x
		
		#we change the nextX and nextY values too because we will use it in the next frame to do the calculations again
		self.nextX = self.x
		self.nextY = self.y
		
		#if the ball is outside of the screen, bounce it
		if self.rect.right >= WIDTH or self.rect.left <= 0:
			self.collide_left_right()
		if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
			self.collide_up_down()
			
		#when the ball hit the bottom of the screen the player loses a life
		if self.rect.bottom >= HEIGHT:
			player.die(WIDTH, HEIGHT)
			self.die(WIDTH, HEIGHT)
			
			#if Ball returns 0, it means the game is over! (in breakout.py)
			if player.lives < 0:
				return 0
		
		#if it collides with the player, bounce it too...
		if pygame.sprite.collide_rect(self, player):
			self.collide_player(player)

		#if we don't do this we get crazy angle values like -9000 after a while
		if self.direction > 360:
			self.direction -= 360
		

	
	def die(self, WIDTH, HEIGHT):
		self.rect.x = self.nextX = self.x = WIDTH/2
		self.rect.y = self.nextY = self.y = HEIGHT - 100
		self.speed = 5
		self.direction = 180
		
	def collide_up_down(self):
		#we check if there's at least 0.005 seconds between each collisions or else it can collides the ball twice
		#when it hits 2 blocks at the same time and the direction change is cancelled (it goes from 180 to 360 to 180 again)
		if time.time() - self.time_last_collide_up_down > 0.005:
			self.time_last_collide_up_down = time.time()
			self.direction = 360 - (self.direction - 180)
		
	def collide_left_right(self):
		if time.time() - self.time_last_collide_left_right > 0.005:
			self.time_last_collide_left_right = time.time()
			self.direction = 360 - self.direction
		
	def collide_player(self, player):
	#calculate the angle of the ball, the closer it is to the borders of the racket the higher the angle is
		print "Position on the racket:", ((self.rect.x + self.rect.width/2 - player.rect.x) * 1.0 / player.rect.width) * 100
		
		percentage_on_racket = ((self.rect.x + self.rect.width/2 - player.rect.x) * 1.0 / player.rect.width) * 100
		self.direction = (-1.2 * percentage_on_racket) + 240