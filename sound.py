import pygame, time

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

class Sound():
	def __init__(self):
		self.sound_volume = 0.2
		self.last_bip = 0
		self.bip = pygame.mixer.Sound("bip.wav")
		self.bip.set_volume(self.sound_volume)	
		self.player_size_increase = pygame.mixer.Sound("increase_size.wav")
		self.player_size_increase.set_volume(self.sound_volume)	
		
		self.player_size_decrease = pygame.mixer.Sound("decrease_size.wav")
		self.player_size_decrease.set_volume(self.sound_volume)	
		self.mute = False
		
	def play_bip(self):
		if time.time() - self.last_bip > 1:
			self.last_bip = time.time()
			self.bip.play()
	
	def play_player_size_increase(self):
		self.player_size_increase.play()
		
	def play_player_size_decrease(self):
		self.player_size_decrease.play()
		
	def change_volume(self):
		if self.mute:
			self.bip.set_volume(0.15)
			self.mute = False
		else:
			self.bip.set_volume(0)
			self.mute = True