import pygame
from pygame.locals import *

from VoronoiMapGen import *

pygame.init()

screen_size = (256,256)
screen = pygame.display.set_mode(screen_size)

mapGenerator = mapGen()

def combine_images(*pics):
	num_pics = len(pics)
	w,h = pics[0].get_size()
	surface = pygame.Surface((w,h))
	total_map = [[0 for i in xrange(w)] for i in xrange(h)]
	for PIC in pics:
		for y in xrange(h):
			for x in xrange(w):
				total_map[x][y]+=PIC.get_at((x,y))[0]

	for y in xrange(h):
		for x in xrange(w):
			total_map[x][y]/=num_pics
			clr = total_map[x][y]
			surface.set_at((x,y), (clr, clr, clr))

	return surface

pic1 = mapGenerator.whole_new(25, c1=-1)
pic2 = mapGenerator.whole_new(25, c2=1)
pic3 = mapGenerator.whole_new(25, c3=1)
pic4 = mapGenerator.whole_new(25, c1=-1, c2=1)

pygame.image.save(combine_images(pic1,pic2,pic3,pic4), "CONGLOMERATEMESS.png")

pygame.quit()