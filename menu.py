import pygame

class Menu():
	def __init__(self):
		#Menu font
		#pygame.font.init()
		font_size = 16
		self.fontObj = pygame.font.SysFont("courier", font_size)
		
		#Menu settings
		self.menu_items_x_position = []
		self.menu_items_y_position = []
		self.rect_items_menu = []
		self.menu_main_text = self.menu_items_text = ["Play", "Options", "Quit"]
		self.menu_options_text = ["800x640", "1280x800", "1360x768", "1440x900", "Back"]
		self.menu_items = []
		
		self.menu_name = "Main"
		self.create_menu()
		
		#self.menu_mouse_pos = [False, False, False, False, False, False]
		

	def update(self, menu, game):
		
		for i in range (len(self.menu_items_text)):
			if self.rect_items_menu[i].collidepoint(pygame.mouse.get_pos()):
				self.menu_items[i] = self.fontObj.render(self.menu_items_text[i], 1, (255,000,000))
				self.menu_mouse_pos[i] = True
			else:
				self.menu_items[i] = self.fontObj.render(self.menu_items_text[i], 1, (255,255,255))
				self.menu_mouse_pos[i] = False
			
		for e in pygame.event.get():
			if e.type == pygame.MOUSEBUTTONDOWN:
				if self.menu_name == "Main":
					if self.menu_mouse_pos[0] == True:
						return "Play"
					elif self.menu_mouse_pos[1] == True:
						self.menu_name = "Options"
						self.menu_items_text = self.menu_options_text
						self.create_menu()
					elif self.menu_mouse_pos[2] == True:
						raise SystemExit, "Quit"	
						
				elif self.menu_name == "Options":
					if self.menu_mouse_pos[0] == True:
						game.__init__(800, 600)
					elif self.menu_mouse_pos[1] == True:
						game.__init__(1280, 800)
					elif self.menu_mouse_pos[2] == True:
						game.__init__(1360, 768)
					elif self.menu_mouse_pos[3] == True:
						game.__init__(1440, 900)
					elif self.menu_mouse_pos[4] == True:
						self.menu_name = "Main"
						self.menu_items_text = self.menu_main_text
						self.create_menu()	
			
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				print "bop"
				raise SystemExit, "ESCAPE"
					
	def draw(self, screen):
		for i in range(len(self.menu_items_text)):
			screen.blit(self.menu_items[i], (self.menu_items_x_position[i], self.menu_items_y_position[i]))
			
	def create_menu(self):
		#create menu from items list
		self.menu_items_x_position[:] = self.menu_items_y_position[:] = self.menu_items[:] = self.rect_items_menu[:] = []
		self.menu_mouse_pos = [False, False, False, False, False, False]
		
		for i in range(len(self.menu_items_text)):
			rendered_menu_text = self.fontObj.render(self.menu_items_text[i], 1, (255,255,255))
			self.menu_items.append(rendered_menu_text)
			
			self.menu_items_x_position.append(pygame.display.Info().current_w/2  - self.menu_items[i].get_rect().width/2)
			self.menu_items_y_position.append(pygame.display.Info().current_h/2 - 50 + 30 * i)
						
			menu_items_rect = pygame.Rect(self.menu_items_x_position[i], self.menu_items_y_position[i], self.menu_items[i].get_rect().width, self.menu_items[i].get_rect().height)
			self.rect_items_menu.append(menu_items_rect)
