import pygame
from pygame.locals import *

from VoronoiMapGen import point, mapGen

from random import seed, randint

screen_size = (512,512)
w,h = screen_size

screen = pygame.display.set_mode(screen_size)

Generator = mapGen()

seed_num = randint(0,10)

seed(seed_num)
large = Generator.whole_new(25, c1=-1, c2=1, name="large normal")
seed(seed_num)
large_thresh = Generator.threshold(Generator.whole_new(25, c1=-1, c2=1, name="large threshold"))
seed(seed_num)
large_comb = Generator.reallyCoolFull((256,256), name="large average")
seed(seed_num)
small1 = Generator.whole_new(25, (128,128), c1=1, c2=1, name="Small 1")
seed(seed_num)
small2 = Generator.whole_new(25, (128,128), c1=-1, name="Small 2")
seed(seed_num)
small3 = Generator.whole_new(25, (128,128), c2=1, name="Small 3")
seed(seed_num)
small4 = Generator.whole_new(25, (128,128), c3=1, name="Small 4")

pygame.display.set_caption("Voronoi Generation Tests!")

done = False
while not done:
	for event in pygame.event.get():
		if event.type == QUIT:
			done = True

	screen.blit(large, (0,0))
	screen.blit(large_thresh, (0,256))
	screen.blit(large_comb, (256,256))

	screen.blit(small1, (256,0))
	screen.blit(small2, (384,0))
	screen.blit(small3, (256,128))
	screen.blit(small4, (384,128))

	pygame.display.flip()

pygame.quit()