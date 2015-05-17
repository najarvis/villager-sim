import pygame
from pygame.locals import *

class Tile:

    def __init__(self, img):
        self.img = img
        self.size = img.get_size


screen_size = 320,320
screen = pygame.display.set_mode(screen_size)

grass_img = pygame.image.load("MyGrass.png").convert()
water_img = pygame.image.load("Water.png").convert()

tilex, tiley = 10,10

Array = [[0 for i in xrange(tilex)] for a in xrange(tiley)]

filename = "TransitionTest.txt"

def get_surrounding(array, pos):
    start = [[0 for i in xrange(3)] for a in xrange(3)]
    start[1][1] = "SELF"
    for i in range(3):
        for a in range(3):
            
