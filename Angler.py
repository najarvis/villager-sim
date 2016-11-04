from aitools.StateMachine import *
from Entities import *
from GameEntity import *
from gametools.vector2 import Vector2
from gametools.ImageFuncs import *
from gametools.ani import *
import BaseFunctions
import math
import pygame
import random
import TileFuncs
from World import *
#TODO: Clean up imports and add docstrings

class Angler(GameEntity):

    def __init__(self, world, image_string):
        # Initializing the class
        GameEntity.__init__(self, world, "Angler", "Entities/"+image_string)

        # Creating the states
        fishing_state = Fishing(self)
        exploring_state = Searching(self)
        delivering_state = Delivering(self)

        # Adding states to the brain
        self.brain.add_state(fishing_state)
        self.brain.add_state(exploring_state)
        self.brain.add_state(delivering_state)

        self.max_speed = 80.0 * (1.0 / 60.0)
        self.speed = self.max_speed
        self.base_speed = self.speed
        self.view_range = 2
        self.fish = 0

        self.worldSize = world.world_size
        self.TileSize = self.world.tile_size

        # animation variables
        self.animation = Ani(9, 10)
        self.pic = pygame.image.load("Images/Entities/map.png")
        self.img_func = ImageFuncs(18, 17,self.pic)
        self.sprites = self.img_func.get_images(9,0,2)
        self.hit = 0
        self.update()

    def update(self):
        self.image = self.sprites[self.animation.get_frame()]
        self.image.set_colorkey((255,0,255))
        if self.animation.finished:
            self.hit += 1
            self.animation.finished = False


class Fishing(State):

    def __init__(self, angler):

        State.__init__(self, "Fishing")
        self.angler = angler

    def check_conditions(self):

        if self.angler.location.get_distance_to(self.angler.destination) <= self.angler.max_speed:
            self.angler.destination = Vector2(self.angler.location)
            self.angler.update()

        if self.angler.fish == 1:
            return "Delivering"

    def do_actions(self):
        if self.angler.location == self.angler.destination and self.angler.hit >= 4:
            # TODO: Why is this checking if the tile is fishable if it has been fishing there?
            
            for tile_location in TileFuncs.get_vnn_array(self.angler.world, self.angler.location, 2):
                if TileFuncs.get_tile(self.angler.world, tile_location).fishable:
                    self.angler.hit = 0
                    self.angler.fish = 1

    def entry_actions(self):
        BaseFunctions.random_dest(self.angler)


class Searching(State):

    def __init__(self, angler):
        State.__init__(self, "Searching")
        self.angler = angler

    def entry_actions(self):
        BaseFunctions.random_dest(self.angler)

    def do_actions(self):
        pass

    def check_conditions(self):
        if self.angler.location.get_distance_to(self.angler.destination) < self.angler.max_speed:
            location_array = TileFuncs.get_vnn_array(self.angler.world,(self.angler.location), self.angler.view_range)

            for location in location_array:
                # TODO: This will make the angler go into the water, change this to go to the nearest walkable tile.
                test_tile = TileFuncs.get_tile(self.angler.world, location)
                if test_tile.__class__.__name__ == "WaterTile":

                    self.angler.destination = location.copy()
                    return "Fishing"

            BaseFunctions.random_dest(self.angler)

    def exit_actions(self):
        pass

class Delivering(State):

    def __init__(self, angler):
        State.__init__(self, "Delivering")
        self.angler = angler

    def entry_actions(self):
        #TODO: Make dropoff point dynamic (e.g. it's own building)

        self.angler.destination = Vector2(self.angler.world.w/2, self.angler.world.h/2)

    def do_actions(self):
        pass

    def check_conditions(self):

        if self.angler.location.get_distance_to(self.angler.destination) < 15:
            self.angler.world.fish += self.angler.fish
            self.angler.fish = 0
            return "Searching"

    def exit_actions(self):
        pass
