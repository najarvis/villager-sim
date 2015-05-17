import pygame
from pygame.locals import *

class mapGen:

	def __init__(self):
		pass

	def genMap(self, num_octaves=8, size=(256,256)):
		surface = pygame.Surface(size)
		w,h=size
		totalMap = [[0 for i in xrange(2**num_octaves)] for i in xrange(2**num_octaves)]
		
