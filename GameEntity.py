from World import *
from StateMachine import *
from gametools.vector2 import *

import pygame
from pygame.locals import *


class GameEntity(object):
    def __init__(self, world, name, image):

        self.world = world
        self.name = name

        self.image = image
        self.orientation = 0
        
        try:
            self.image.set_colorkey((255, 0, 255))
        except AttributeError:
            pass
        self.location = Vector2(0, 0)
        self.world_location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.

        self.brain = StateMachine()

        self.id = 0

        self.tp = 1.0

    def render(self, surface):
        x, y = self.world_location
        w, h = self.image.get_size()
        pos = (x-w/2, y-h/2)
        surface.blit(self.image, pos)

    def process(self, time_passed):
        self.brain.think()
        self.tp = time_passed
        self.world_location = self.location+self.world.background_pos

        if self.speed > 0. and self.location != self.destination:
            vec_to_destination = self.destination-self.location
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed*self.speed)
            self.location += travel_distance*heading*time_passed*self.speed
