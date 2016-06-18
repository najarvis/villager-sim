from aitools.StateMachine import *
from Entities import *
from GameEntity import *
from gametools.vector2 import Vector2
from gametools.ImageFuncs import *
from gametools.ani import *
import math
import pygame
import random
import TileFuncs
from World import *

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
        self.view_range = 1
        self.fish = 0

        self.worldSize = world.world_size
        self.TileSize = self.world.tile_size

        # animation variables
        self.animation = Ani(9,10)
        self.pic = pygame.image.load("Images/Entities/map.png")
        self.img_func = ImageFuncs(18, 17,self.pic)
        self.sprites = self.img_func.get_images(9,0,2)
        self.hit = 0
        self.update()

    def update(self):
        self.image = self.sprites[self.animation.get_frame()]
        self.image.set_colorkey((255,0,255))
        if self.animation.finished == True:
            self.hit += 1
            self.animation.finished = False


class Fishing(State):

    def __init__(self, angler):

        State.__init__(self, "Fishing")
        self.angler = angler

    def check_conditions(self):

        if self.angler.location.get_distance_to(self.angler.destination) < 15:
            self.angler.destination = Vector2(self.angler.location)
            self.angler.update()

        if self.angler.fish == 1:
            return "Delivering"

    def do_actions(self):

        if self.angler.location == self.angler.destination and self.angler.hit >= 4 and TileFuncs.get_tile(
                self.angler.world,self.angler.location).fishable == 1:
            self.angler.hit = 0
            self.angler.fish = 1


    def random_dest(self, recurse=False, r_num=0, r_max=5):
        # Function for going to a random destination
        if recurse:
            self.angler.orientation += 20
        else:
            self.angler.orientation += random.randint(-20, 20)
        angle = math.radians(self.angler.orientation)
        distance = random.randint(50, 100)
        random_dest = Vector2(self.angler.location.x + math.cos(angle) * distance, self.angler.location.y + math.sin(angle) * distance)        
        
        # If the destination will go off the map, it is NOT a valid move under any circumstances.
        bad_spot = False
        if (0 > random_dest.x > self.angler.world.world_size[0] or \
            0 > random_dest.y > self.angler.world.world_size[1]):
            bad_spot = True

        if ((not TileFuncs.get_tile(self.angler.world, random_dest).walkable and r_num < r_max) or bad_spot):
            self.random_dest(True, r_num+1)
        
        self.angler.destination = random_dest

    def entry_actions(self):
        self.random_dest()


class Searching(State):

    def __init__(self, angler):
        State.__init__(self, "Searching")
        self.angler = angler

    def entry_actions(self):
        self.random_dest()

    def do_actions(self):
        pass

    def check_conditions(self):
        if self.angler.location.get_distance_to(self.angler.destination) < 15:
            location_array = TileFuncs.get_vnn_array(self.angler.world,(self.angler.location), self.angler.view_range)

            for location in location_array:
                test_tile = TileFuncs.get_tile(self.angler.world,location)
                if test_tile.name == "AndrewWater":

                    self.angler.destination = location.copy()
                    return "Fishing"

            self.random_dest()

    def exit_actions(self):
        pass

    def random_dest(self, recurse=False, r_num=0, r_max=5):
        # Function for going to a random destination
        if recurse:
            self.angler.orientation += 20
        else:
            self.angler.orientation += random.randint(-20, 20)
        angle = math.radians(self.angler.orientation)
        distance = random.randint(50, 100)
        random_dest = Vector2(self.angler.location.x + math.cos(angle) * distance, self.angler.location.y + math.sin(angle) * distance)        
        
        # If the destination will go off the map, it is NOT a valid move under any circumstances.
        bad_spot = False
        if (0 > random_dest.x > self.angler.world.world_size[0] or \
            0 > random_dest.y > self.angler.world.world_size[1]):
            bad_spot = True

        if ((not TileFuncs.get_tile(self.angler.world, random_dest).walkable and r_num < r_max) or bad_spot):
            self.random_dest(True, r_num+1, r_max)
        
        self.angler.destination = random_dest


class Delivering(State):

    def __init__(self, angler):
        State.__init__(self, "Delivering")
        self.angler = angler

    def entry_actions(self):

        self.angler.destination = Vector2(self.angler.world.w/2,self.angler.world.h/2)

    def do_actions(self):
        pass

    def check_conditions(self):

        # if self.angler.world.wood >= self.angler.world.MAXwood:
        #    return "IDLE"

        if self.angler.location.get_distance_to(self.angler.destination) < 15:
            self.angler.world.fish += self.angler.fish
            self.angler.fish = 0
            return "Searching"

    def exit_actions(self):
        pass
