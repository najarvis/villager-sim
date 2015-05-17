import pygame
from pygame.locals import *
pygame.init()

screen_size = 640,480

screen = pygame.display.set_mode(screen_size)

done = False
while done == False:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
            
    pygame.display.flip()
            
pygame.quit()