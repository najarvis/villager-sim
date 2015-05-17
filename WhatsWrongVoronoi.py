import pygame
from pygame.locals import *
pygame.init()

from VoronoiMapGen import mapGen, point
from random import seed

screen_size = (512,256)
w,h = screen_size

screen = pygame.display.set_mode(screen_size)

gen = mapGen()

seed(10)
image1 = gen.whole_new(25,c1=-1, name="image 1")
seed(10)
image2 = gen.whole_new(25,c2=-1, name="image 2")

if image1 == image2:
	pygame.display.set_caption("THEY MATCH")

done = False
while not done:

	pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == QUIT:
			done=True

	try:
		clr1 = image1.get_at(pos)[0]
		clr2 = image2.get_at(pos)[0]
		pygame.display.set_caption(str(clr1)+", "+str(clr2))
	except Exception:
		pass

	screen.blit(image1, (0,0))
	screen.blit(image2, (256,0))
	pygame.display.flip()

pygame.quit()