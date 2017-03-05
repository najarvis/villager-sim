from World import *
from aitools.StateMachine import *
from gametools.vector2 import *
import TileFuncs
import pygame
from pygame.locals import *

# TODO: Clean and add doctrings


class GameEntity(object):
    def __init__(self, world, name, image_string):

        self.world = world
        self.name = name

        self.image = pygame.image.load("Images/"+image_string+".png")
        self.orientation = 0
        
        try:
            self.image.set_colorkey((255, 0, 255))
        except AttributeError:
            pass
        self.location = Vector2(0, 0)
        self.world_location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.

        self.land_based = True
        self.base_speed = self.speed

        self.food = 70
        self.water = 70
        self.energy = 70
        self.active_info = False

        self.brain = StateMachine()

        self.id = 0

        self.tp = 1.0

    def render(self, surface):
        x, y = self.world_location
        w, h = self.image.get_size()
        pos = (x - (w / 2), y - (h / 2))
        surface.blit(self.image, pos)

    def check_speed(self):
        if TileFuncs.get_tile(self.world, self.location).name in ["AndrewSmoothStone", "MinecraftSnow"]:
            self.speed = 0.5 * self.base_speed
        else:
            self.speed = self.base_speed

    def process(self, time_passed):
        self.brain.think()
        self.world_location = self.location + self.world.world_position


        self.check_speed()

        if self.speed > 0. and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, self.speed)
            self.location += travel_distance * heading * self.speed
