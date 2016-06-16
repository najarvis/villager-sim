from GameEntity import GameEntity
from aitools.StateMachine import State
from Tile import *
from gametools.ImageFuncs import *

from random import randint
import random
import math
import pygame

NoTreeImg = pygame.image.load("Images/Tiles/MinecraftGrass.png")


class Lumberjack(GameEntity):
    def __init__(self, world, img):
        GameEntity.__init__(self, world, "Lumberjack", img)
        img_func = image_funcs(18, 17)

        self.speed = 100.
        self.view_range = 6

        self.searching_state = Searching(self)
        self.chopping_state = Chopping(self)
        self.delivering_state = Delivering(self)

        self.brain.add_state(self.searching_state)
        self.brain.add_state(self.chopping_state)
        self.brain.add_state(self.delivering_state)

        self.worldSize = world.size
        self.TileSize = self.world.TileSize

        self.row = 1
        self.times = 3
        self.pic = pygame.image.load("Images/Entities/map.png")
        self.cells = img_func.get_list(self.pic)
        self.ani = img_func.get_images(self.cells, self.times, 1, 1, 1, self.row, self.pic)
        self.start = img_func.get_image(self.cells, 1, 1, 0, self.row, self.pic)
        self.num = 0
        self.num_max = len(self.ani)-1
        self.ani_speed_init = 10
        self.ani_speed = self.ani_speed_init
        self.img = self.ani[0]
        self.update()
        self.hit = 0

    def update(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.image = self.ani[self.num]
            self.image.set_colorkey((255, 0, 255))
            self.ani_speed = self.ani_speed_init
            if self.num == self.num_max:
                self.num = 0
                self.hit += 1
            else:
                self.num += 1


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
            location_array = self.lumberjack.world.get_vnn_array((self.lumberjack.location), self.lumberjack.view_range)

            for location in location_array:
                test_tile = self.lumberjack.world.get_tile(location)
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
        if not self.lumberjack.world.get_tile(Vector2(*random_dest)).walkable:
            try:
                self.random_dest(True)
            except RuntimeError:
                pass
                #TODO: Fix this, it is trash
                #print "SOMEONE IS DROWNING!!"
                
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
                self.lumberjack.num = 0
                self.lumberjack.image = self.lumberjack.start
                self.lumberjack.ani_speed = self.lumberjack.ani_speed_init
                return "Searching"

            self.lumberjack.update()

            if self.lumberjack.hit == 4:
                self.lumberjack.destination = Vector2(self.lumberjack.location)
                self.lumberjack.image = self.lumberjack.start
                self.lumberjack.image.set_colorkey((255, 0, 255))

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
