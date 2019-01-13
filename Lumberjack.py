from aitools.StateMachine import *
from Entities import *
from GameEntity import *
from gametools.vector2 import Vector2
from gametools.ImageFuncs import *
from gametools.ani import *
import Tile
import math
import pygame
import random
import TileFuncs
from World import *
import BaseFunctions

NoTreeImg = pygame.image.load("Images/Tiles/MinecraftGrass.png")

class Lumberjack(GameEntity):

    def __init__(self, world, image_string):
        # Initializing the class
        GameEntity.__init__(self, world, "Lumberjack", "Entities/"+image_string)

        self.speed = 100.0 * (1.0 / 60.0)
        self.base_speed = self.speed
        self.view_range = 6

        # Creating the states
        self.searching_state = Searching(self)
        self.chopping_state = Chopping(self)
        self.delivering_state = Delivering(self)

        # Adding states to the brain
        self.brain.add_state(self.searching_state)
        self.brain.add_state(self.chopping_state)
        self.brain.add_state(self.delivering_state)

        self.worldSize = world.world_size
        self.TileSize = self.world.tile_size

        # animation variables
        self.animation = Ani(5,10)
        self.pic = pygame.image.load("Images/Entities/map.png")
        self.img_func = ImageFuncs(18, 17,self.pic)
        self.sprites = self.img_func.get_images(5,0,1)
        self.hit = 0
        self.update()

    def update(self):
        # Updates image every 10 cycles and adds 1 to the 4 hit dig
        self.image = self.sprites[self.animation.get_frame()]
        self.image.set_colorkey((255,0,255))
        if self.animation.finished == True:
            self.hit += 1
            self.animation.finished = False


class Searching(State):
    """This state will be used to have the Lumberjack looking for
       trees to cut, It needs to be fast enough to have AT LEAST 20 Lumberjacks
       with little to no framerate loss.
       
       Perhaps it could be used to find a clump of trees. and then the Lumberjack
       wouldn't just wander around aimlessly searching for trees even though it
       saw some when it was just at another tree"""

    def __init__(self, Lumberjack):
        State.__init__(self, "Searching")
        self.lumberjack = Lumberjack

    def entry_actions(self):
        BaseFunctions.random_dest(self.lumberjack)

    def do_actions(self):
        pass

    def check_conditions(self):
        if self.lumberjack.location.get_distance_to(self.lumberjack.destination) < 15:
            location_array = TileFuncs.get_vnn_array(self.lumberjack.world,(self.lumberjack.location), self.lumberjack.view_range)

            for location in location_array:
                test_tile = TileFuncs.get_tile(self.lumberjack.world,location)
                if test_tile.name == "GrassWithCenterTree":
                    self.lumberjack.Tree_tile = test_tile
                    self.lumberjack.tree_id = test_tile.id

                    self.lumberjack.destination = location.copy()
                    return "Chopping"

            BaseFunctions.random_dest(self.lumberjack)

    def exit_actions(self):
        pass


class Chopping(State):
    def __init__(self, Lumberjack):
        State.__init__(self, "Chopping")
        self.lumberjack = Lumberjack

    def entry_actions(self):
        pass

    def do_actions(self):
        pass

    def check_conditions(self):
        check = TileFuncs.get_tile(self.lumberjack.world,Vector2(self.lumberjack.location))
        if self.lumberjack.location.get_distance_to(self.lumberjack.destination) < 15:
            self.lumberjack.destination = Vector2(self.lumberjack.location)

            if check.name != "GrassWithCenterTree":
                self.lumberjack.hit = 0
                self.lumberjack.update()
                return "Searching"

            self.lumberjack.update()

            if self.lumberjack.hit >= 4:
                self.lumberjack.destination = Vector2(self.lumberjack.location)
                self.lumberjack.update()

                old_tile = TileFuncs.get_tile(self.lumberjack.world,Vector2(self.lumberjack.location))

                darkness = pygame.Surface((32, 32))
                darkness.set_alpha(old_tile.darkness)

                new_tile = Tile.TreePlantedTile(self.lumberjack.world, "MinecraftGrass")

                new_tile.darkness = old_tile.darkness

                new_tile.location = TileFuncs.get_tile_pos(self.lumberjack.world,self.lumberjack.destination)*32
                new_tile.rect.topleft = new_tile.location
                new_tile.color = old_tile.color

                self.lumberjack.world.tile_array[int(new_tile.location.y/32)][int(new_tile.location.x/32)] = new_tile
                self.lumberjack.world.world_surface.blit(new_tile.img, new_tile.location)
                self.lumberjack.world.world_surface.blit(darkness, new_tile.location)

                self.lumberjack.hit = 0

                # del self.lumberjack.world.TreeLocations[str(self.lumberjack.tree_id)]
                return "Delivering"

    def exit_actions(self):
        pass


class Delivering(State):
    """This state will be used solely to deliver wood from wherever the Lumberjack
       got the wood to the closest Lumber yard. maybe all the lumber yards could
       be stored in a dictionary similar to trees, that would be much faster"""

    def __init__(self, Lumberjack):
        State.__init__(self, "Delivering")
        self.lumberjack = Lumberjack

    def entry_actions(self):
        self.lumberjack.destination = Vector2(self.lumberjack.world.w/2,self.lumberjack.world.h/2)

    def do_actions(self):
        pass

    def check_conditions(self):

        # if self.lumberjack.world.wood >= self.lumberjack.world.MAXwood:
        #    return "IDLE"

        if self.lumberjack.location.get_distance_to(self.lumberjack.destination) < 15:
            self.lumberjack.world.wood += 5
            return "Searching"

    def exit_actions(self):
        pass


class IDLE(State):
    def __init__(self, Lumberjack):
        State.__init__(self, "Delivering")
        self.lumberjack = Lumberjack

    def entry_actions(self):
        pass

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def exit_actions(self):
        pass
