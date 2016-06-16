from GameEntity import GameEntity
from aitools.StateMachine import State
from Tile import *
import TileFuncs
from gametools.ImageFuncs import *
from gametools.ani import *
from random import randint
import random
import math
import pygame

NoTreeImg = pygame.image.load("Images/Tiles/MinecraftGrass.png")


class Lumberjack(GameEntity):
    def __init__(self, world, img):
        GameEntity.__init__(self, world, "Lumberjack", img)

        self.speed = 100.
        self.view_range = 6

        self.searching_state = Searching(self)
        self.chopping_state = Chopping(self)
        self.delivering_state = Delivering(self)

        self.brain.add_state(self.searching_state)
        self.brain.add_state(self.chopping_state)
        self.brain.add_state(self.delivering_state)

        self.worldSize = world.world_size
        self.TileSize = self.world.tile_size

        self.animation = Ani(5,10)
        self.pic = pygame.image.load("Images/Entities/map.png")
        self.img_func = ImageFuncs(18, 17,self.pic)
        self.sprites = self.img_func.get_images(5,0,1)
        self.hit = 0
        self.update()

    def update(self):
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
        self.random_dest()

    def do_actions(self):
        pass

    def check_conditions(self):
        if self.lumberjack.location.get_distance_to(self.lumberjack.destination) < 15:
            location_array = TileFuncs.get_vnn_array(self.lumberjack.world,(self.lumberjack.location), self.lumberjack.view_range)

            for location in location_array:
                test_tile = TileFuncs.get_tile(self.lumberjack.world,location)
                if test_tile.name == "TreePlantedTile_W":
                    self.lumberjack.Tree_tile = test_tile
                    self.lumberjack.tree_id = test_tile.id

                    self.lumberjack.destination = location.copy()
                    return "Chopping"

            self.random_dest()

    def exit_actions(self):
        pass

    def random_dest(self, recurse=False):
        # Function for going to a random destination
        if recurse:
            self.lumberjack.orientation += 20
        else:
            self.lumberjack.orientation += random.randint(-20, 20)
        angle = math.radians(self.lumberjack.orientation)
        distance = random.randint(25, 50)
        random_dest = (self.lumberjack.location.x + math.cos(angle) * distance, self.lumberjack.location.y + math.sin(angle) * distance)
        # if not TileFuncs.get_tile(self.lumberjack.world,Vector2(*random_dest)).walkable:
        #     try:
        #         self.random_dest(True)
        #     except RuntimeError:
        #         pass
        #         #TODO: Fix this, it is trash
        #         #print "SOMEONE IS DROWNING!!"
                
        self.lumberjack.destination = Vector2(*random_dest)


class Chopping(State):
    def __init__(self, Lumberjack):
        State.__init__(self, "Chopping")
        self.lumberjack = Lumberjack

    def entry_actions(self):
        pass

    def do_actions(self):
        pass

    def check_conditions(self):
        check = self.lumberjack.world.get_tile(Vector2(self.lumberjack.location))
        if self.lumberjack.location.get_distance_to(self.lumberjack.destination) < 15:
            self.lumberjack.destination = Vector2(self.lumberjack.location)

            if check.name != "TreePlantedTile_W":
                self.lumberjack.hit = 0
                self.lumberjack.update()
                return "Searching"

            self.lumberjack.update()

            if self.lumberjack.hit >= 4:
                self.lumberjack.destination = Vector2(self.lumberjack.location)
                self.lumberjack.update()

                old_tile = self.lumberjack.world.get_tile(Vector2(self.lumberjack.location))

                darkness = pygame.Surface((32, 32))
                darkness.set_alpha(old_tile.darkness)

                new_tile = TreePlantedTile(self.lumberjack.world, NoTreeImg)

                new_tile.darkness = old_tile.darkness

                new_tile.location = self.lumberjack.world.get_tile_pos(self.lumberjack.destination)*32
                new_tile.rect.topleft = new_tile.location
                new_tile.color = old_tile.color

                self.lumberjack.world.TileArray[int(new_tile.location.y/32)][int(new_tile.location.x/32)] = new_tile
                self.lumberjack.world.full_surface.blit(new_tile.img, new_tile.location)
                self.lumberjack.world.full_surface.blit(darkness, new_tile.location)

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

        des = self.lumberjack.world.get_close_entity("LumberYard", self.lumberjack.location, 100)
        if des == None:
            des = self.lumberjack.world.get_close_entity("LumberYard", self.lumberjack.location, 300)
            if des == None:
                des = self.lumberjack.LastLumberYard

        self.lumberjack.LastLumberYard = des

        self.lumberjack.destination = des.location.copy()

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
