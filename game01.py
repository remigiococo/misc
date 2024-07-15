import sys
import pygame
from pygame import gfxdraw as gfx
import os
import math
import random

BLOCK_SIZE=80
NUM_ROWS=4
NUM_COLS=4
PIGRECO=3.1415926535897932384626433832795

def load_image(image_name):
	try:
		surface = pygame.image.load(os.path.join(main_dir, "images", image_name))
		return surface
	except pygame.error as message:
		print('Cannot load image:', image_name)
		raise SystemExit(message)

def is_in_sector(dx,dy,min_r,max_r,min_ang,max_ang):
	if dx == 0 and dy == 0:
		return False
	d = math.sqrt(dx*dx + dy*dy)
	if (d < min_r) or (d > max_r):
		return False
	if dx == 0:
		if dy > 0:
			a = PIGRECO*0.5
		else:
			a = PIGRECO*1.5
	elif dy == 0:
		if dx > 0:
			a = 0
		else:
			a = PIGRECO
	else:		
		a = math.atan2(dy, dx)
		if a < 0:
			a = a + PIGRECO*2
	if (a <= min_ang) or (a > max_ang):
		return False
	return True

def drawArc(surface, center, radii, angles, color):
	rs = surface.get_rect()
	for x in range(rs.width):
		for y in range(rs.height):
			if is_in_sector(x-center[0], y-center[1], radii[0], radii[1], angles[0], angles[1]):
				surface.set_at((x, y), color)
	
class GameObject:

	def __init__(self, surface, x, y, image_name=None):
		self.surface = surface
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
		if image_name != None and len(image_name) > 0:
			self.image = utils.load_image(image_name)
			self.image = pygame.transform.smoothscale(self.image, [BLOCK_SIZE, BLOCK_SIZE])

	def get_row(self):
		return self.y // BLOCK_SIZE

	def get_col(self):
		return self.x // BLOCK_SIZE

	def set_row(self, r):
		self.y = r*BLOCK_SIZE

	def set_col(self, c):
		self.x = c*BLOCK_SIZE

class Button(GameObject):
	
	def __init__(self, surface, x, y, text=None):
		super().__init__(surface, x, y, image_name=None)
		self.text=text
		self.font = "Arial"
		self.fontsize = 12
		self.pressed = False

	def draw(self):
		GAP=2
		rect2 = pygame.Rect(self.rect.x+GAP, self.rect.y+GAP, self.rect.width-2*GAP, self.rect.height-2*GAP)
		pygame.draw.rect(self.surface, (128,128,128), self.rect) # background
		pygame.draw.rect(self.surface, (250,250,250), rect2, border_radius=6)
		button_text = pygame.font.SysFont(self.font, self.fontsize).render(self.text, True, (0,0,0))
		button_rect = button_text.get_rect(center=self.rect.center)
		self.surface.blit(button_text, button_rect)
	
	def down(self, x, y):
		#print(x, y, self.rect) # debug
		#xx = x - self.rect[0]
		#yy = y - self.rect[1]
		prev = self.pressed
		self.pressed = False
		if self.rect.collidepoint(x, y) and pygame.mouse.get_pressed()[0] == 1:
			self.pressed = True
		if self.pressed == True and prev == False:
			return True
		return False
		
class Disc(GameObject):
	
	def __init__(self, surface, x, y, image_name=None):
		super().__init__(surface, x, y, image_name)
		self.angle = 0
		self.surf_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
		r = self.rect.width // 2
		drawArc(self.surf_img, (r, r), (1,r), (0, PIGRECO*0.5), (200, 10, 10))
		drawArc(self.surf_img, (r, r), (1,r), (PIGRECO*0.5, PIGRECO), (10, 200, 10))
		drawArc(self.surf_img, (r, r), (1,r), (PIGRECO, PIGRECO*1.5), (10, 10, 200))
		drawArc(self.surf_img, (r, r), (1,r), (PIGRECO*1.5, PIGRECO*2), (255, 255, 255))
		
	def incr_angle(self, a):
		# angolo in gradi
		self.angle = self.angle + a
		if( self.angle >= 360 ):
			self.angle = self.angle - 360
			
	def draw(self):
		#print(self.rect)
		#rect2 = pygame.Rect(self.rect.left, self.rect.top, self.rect.width*2, self.rect.height*2)
		zoom = 1
		rect2 = pygame.Rect(0, 0, self.rect.width*zoom, self.rect.height*zoom)
		surf2 = pygame.Surface((rect2.width, rect2.height))
		modo = 5
		if modo == 1:
			rr = rect2
			for w in range(10*zoom):
				pygame.draw.arc(surf2, (200, 10, 10), rr, 0, PIGRECO*0.5, width=4)
				pygame.draw.arc(surf2, ( 10,200, 10), rr, PIGRECO*0.5, PIGRECO, width=4)
				pygame.draw.arc(surf2, ( 10, 10,200), rr, PIGRECO, PIGRECO*1.5, width=4)
				pygame.draw.arc(surf2, (255,255,255), rr, PIGRECO*1.5, PIGRECO*2, width=4)
				rr.left = rr.left+1
				rr.top = rr.top+1
				rr.width = rr.width-2
				rr.height = rr.height-2
		if modo == 2:		
			pygame.draw.arc(surf2, (200, 10, 10), rect2, 0, PIGRECO*0.5, width=10*zoom)
			pygame.draw.arc(surf2, ( 10,200, 10), rect2, PIGRECO*0.5, PIGRECO, width=10*zoom)
			pygame.draw.arc(surf2, ( 10, 10,200), rect2, PIGRECO, PIGRECO*1.5, width=10*zoom)
			pygame.draw.arc(surf2, (255,255,255), rect2, PIGRECO*1.5, PIGRECO*2, width=10*zoom)
		if modo == 3:
			r = rect2.width//2
			xx = rect2.x + r
			yy = rect2.y + r
			for w in range(15*zoom):
				gfx.arc(surf2, xx, yy, r, 0, 90, (200,10,10))
				gfx.arc(surf2, xx, yy, r, 90, 180, (10,200,10))
				gfx.arc(surf2, xx, yy, r, 180, 270, (10,10,200))
				gfx.arc(surf2, xx, yy, r, 270, 360, (255,255,255))
				r = r - 1
		if modo == 4:
			r = rect2.width//2
			xx = rect2.x + r
			yy = rect2.y + r
			rr = (1,r) #(r*3//4, r)
			drawArc(surf2, (xx, yy), rr, (self.angle, self.angle + PIGRECO*0.5), (200, 10, 10))
			drawArc(surf2, (xx, yy), rr, (self.angle + PIGRECO*0.5, self.angle + PIGRECO), (10, 200, 10))
			drawArc(surf2, (xx, yy), rr, (self.angle + PIGRECO, self.angle + PIGRECO*1.5), (10, 10, 200))
			drawArc(surf2, (xx, yy), rr, (self.angle + PIGRECO*1.5, self.angle + PIGRECO*2), (255,255,255))
		if modo == 5:
			surf3 = pygame.transform.rotate(self.surf_img, self.angle)
			rect3 = surf3.get_rect()
			#print(rect2)
			surf2.blit(surf3, rect2, area=pygame.Rect((rect3.width-self.rect.width)//2,(rect3.height-self.rect.height)//2, self.rect.width, self.rect.height))
		surf2 = pygame.transform.smoothscale(surf2, (self.rect.width, self.rect.height))		
		self.surface.blit(surf2, self.rect)
		#
		# test di animazione
		#
		#self.angle = self.angle + 1
		#if self.angle > 360:
		#	self.angle = self.angle - 360
		#print(self.angle)	
		return
		
class MainGame:

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Test")
		self.screen_w = pygame.display.Info().current_w
		self.screen_h = pygame.display.Info().current_h
		print(self.screen_w, self.screen_h)
		self.clk = pygame.time.Clock()
		self.screen = None
		self.width = 0
		self.height = 0
		self.rows = NUM_ROWS
		self.cols = NUM_COLS
		self.moves = 0


	def initialization(self):
		self.width = BLOCK_SIZE * (self.cols+1)
		self.height = BLOCK_SIZE * (self.rows+1)
		os.environ["SDL_VIDEO_WINDOW_POS"] = ("" + str(self.screen_w // 2 - self.width // 2)
																					+ ", " + str(self.screen_h // 2 - self.height // 2))
		self.screen = pygame.display.set_mode([self.width, self.height])
		self.rect = self.screen.get_rect()
		self.d = [ [ None for r in range(self.cols+1) ] for c in range(self.rows+1) ]
		for r in range(1,self.rows+1):
			for c in range(1,self.cols+1):
				self.d[r][c] = Disc(self.screen, c*BLOCK_SIZE, r*BLOCK_SIZE)
		self.b_cols = [ Button(self.screen, 0, r*BLOCK_SIZE, "Rotate") for	r in range(0, self.rows+1) ]
		self.b_rows = [ Button(self.screen, c*BLOCK_SIZE, 0, "Rotate") for	c in range(0, self.cols+1) ]
		self.animation = False
		self.r_ani = 0
		self.c_ani = 0
		self.font = "Arial"
		self.fontsize = 24
		#
		for n in range(100):
			rc = random.randint(0,1)
			if rc == 0:
				r = random.randint(1,4)
				self.rotate_row(r)
			else:
				c = random.randint(1,4)
				self.rotate_col(c)

	def rotate_row(self, r):
		for c in range(1, self.cols+1):
			self.d[r][c].incr_angle(90)

	def rotate_col(self, c):
		for r in range(1, self.rows+1):
			self.d[r][c].incr_angle(90)

	def completed(self):
		for r in range(1, self.rows+1):
			for c in range(1, self.cols+1):
				if self.d[r][c].angle != 0:
					return False
		return True
		
	def main(self):
		self.initialization()
		while True:
			self.screen.fill((128,128,128))	
			if self.completed():
				txt = "Finished in " + str(self.moves) + " moves"
				#print(txt) # debug
				fin_text = pygame.font.SysFont(self.font, self.fontsize).render(txt, True, (0,0,0))
				fin_rect = fin_text.get_rect(center=self.rect.center)
				self.screen.blit(fin_text, fin_rect)
			else:	
				for r in range(1,self.rows+1):
					for c in range(1,self.cols+1):
						self.d[r][c].draw()
				for r in range(1,self.rows+1):
					self.b_cols[r].draw()
				for c in range(1,self.cols+1):
					self.b_rows[c].draw()
			event = pygame.event.poll() #pygame.event.wait()
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_r:
					self.initialization()
			if self.animation:
				if self.r_ani != 0:
					for c in range(1, self.cols+1):
						self.d[self.r_ani][c].incr_angle( 3 )
						if (self.d[self.r_ani][c].angle % 90) == 0:
							self.animation = False
				if self.c_ani != 0:
					for r in range(1, self.rows+1):
						self.d[r][self.c_ani].incr_angle( 3 )
						if (self.d[r][self.c_ani].angle % 90) == 0:
							self.animation = False
			else:	
				mouse_x = pygame.mouse.get_pos()[0]
				mouse_y = pygame.mouse.get_pos()[1]
				for r in range(1, self.rows+1):
					if self.b_cols[r].down(mouse_x,mouse_y):
						# print("pressed", r) # debug
						#self.rotate_row(r)
						self.animation = True
						self.r_ani = r
						self.c_ani = 0
						self.moves += 1
				for c in range(1, self.cols+1):
					if self.b_rows[c].down(mouse_x,mouse_y):
						# print("pressed", c) # debug
						#self.rotate_col(c)
						self.animation = True
						self.r_ani = 0
						self.c_ani = c
						self.moves += 1
			self.clk.tick(100)
			pygame.display.flip()

if __name__ == "__main__":
	game = MainGame()
	game.main()
