import pygame
from pygame.locals import *
from VoronoiMapGen import mapGen
from random import randint
pygame.init()

screen_size = (512,512)
w,h = screen_size

screen = pygame.display.set_mode(screen_size)

generator = mapGen()

def new_cave(width,height,p=35, ds=None):
	p = int(max(width,height)/min(width,height)*2.5+25)
	map1 = generator.reallyCoolFull((width,height),num_p = p,ds=ds)
	blank_img = pygame.Surface((width,height))
	blank_img.fill((111,72,34))
	barWidth = 0
	for y in xrange(height):
		for x in xrange(width):
			barWidth+=1
			clr = map1.get_at((x,y))[0]
			if 150 >= clr >= 128:
				blank_img.set_at((x,y), (156,102,31))
			elif (height/2 < y < height/2+40) and randint(1,8)==1:
				blank_img.set_at((x,y), (20,20,20))	#Coal
			if (clr == 120 or clr == 121) and randint(1,4)==1:
				blank_img.set_at((x,y), (255,0,0))
			elif clr == 125 and y >= height-32:
				blank_img.set_at((x,y), (0,100,255))
			if clr >= height-3:
				blank_img.set_at((x,y), (100,100,100))

		barWidth=((y*width)/float(height*width))*512
		pygame.draw.rect(screen, (255,255,255), (0,50,barWidth,20))
		pygame.display.update()

	pygame.image.save(pygame.transform.scale(blank_img, (width*4, height*4)), "BLANK_IMG.png")
	return blank_img

img1 = new_cave(256,512, ds = screen)

done = False
while done==False:
	for event in pygame.event.get():
		if event.type == QUIT:
			done = True
		if event.type == KEYDOWN and event.key == K_SPACE:
			img1 = new_cave()

	screen.blit(pygame.transform.scale(img1, (256,512)), (128,0))

	pygame.display.flip()

pygame.quit()
