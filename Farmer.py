from StateMachine import *
from World import *
from GameEntity import *

from gametools.vector2 import Vector2
from Entities import *
from Image_funcs import *

import random
import math

import pygame

Tile_image = pygame.image.load("Images/Tiles/baby_tree.png")


class Farmer(GameEntity):
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "Farmer", image)
        img_func = image_funcs(18, 17)

        planting_state = Farmer_Planting(self)
        #         exploring_state = Farmer_Exploring(self)

        self.brain.add_state(planting_state)
        #         self.brain.add_state(exploring_state)


        self.speed = 80
        self.max_speed = self.speed

        self.planted = 0

        self.worldSize = world.size
        self.TileSize = self.world.TileSize

        self.row = 0
        self.times = 6
        self.pic = pygame.image.load("Images/Entities/map.png")
        self.cells = img_func.get_list(self.pic)
        self.ani = img_func.get_images(self.cells, self.times, 1, 1, 1, self.row, self.pic)
        self.start = img_func.get_image(self.cells, 1, 1, 0, self.row, self.pic)
        self.num = 0
        self.img = self.ani[0]
        self.num_max = len(self.ani)-1
        self.ani_speed_init = 10
        self.ani_speed = self.ani_speed_init
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


class Farmer_Planting(State):
    def __init__(self, Farmer):

        State.__init__(self, "Planting")
        self.farmer = Farmer

    def check_conditions(self):
        if self.farmer.location.get_distance_to(self.farmer.destination) < 15:
            self.farmer.destination = Vector2(self.farmer.location)
            self.farmer.update()

    def do_actions(self):
        if self.farmer.location == self.farmer.destination and self.farmer.hit == 4 and self.farmer.world.get_tile(
                self.farmer.location).plantable == 1:
            self.plant_seed()
        if self.farmer.location == self.farmer.destination and self.farmer.hit != 4 and self.farmer.world.get_tile(
                self.farmer.location).plantable != 1:
            self.random_dest()

    def plant_seed(self):
        # Function for planting trees

        # Test to see if the tile the farmer is on is a tile that a tree can be planted on
        if self.farmer.world.get_tile(self.farmer.location).plantable == 1:
            self.farmer.hit = 0
            self.farmer.image = self.farmer.start
            self.farmer.image.set_colorkey((255, 0, 255))

            old_tile = self.farmer.world.get_tile(Vector2(self.farmer.location))

            darkness = pygame.Surface((32, 32))
            darkness.set_alpha(old_tile.darkness)

            new_tile = Baby_Tree(self.farmer.world, Tile_image)

            new_tile.darkness = old_tile.darkness

            new_tile.location = self.farmer.world.get_tile_pos(self.farmer.destination)*32
            new_tile.rect.topleft = new_tile.location
            new_tile.color = old_tile.color

            # Give it an ID so it can be found
            new_tile.id = self.farmer.world.Baby_TreeID
            self.farmer.world.Baby_TreeID += 1

            self.farmer.world.TileArray[int(new_tile.location.y/32)][int(new_tile.location.x/32)] = new_tile
            self.farmer.world.full_surface.blit(new_tile.img, new_tile.location)
            self.farmer.world.full_surface.blit(darkness, new_tile.location)

            # Add the location to a dictionary so villagers can see how far they are from it.
            self.farmer.world.baby_tree_locations[str(self.farmer.world.Baby_TreeID)] = new_tile.location

        # Goes to a random destination no matter what
        self.farmer.hit = 0
        self.random_dest()

    def random_dest(self, recurse=False):
        # Function for going to a random destination
        if recurse:
            self.farmer.orientation += 20
        else:
            self.farmer.orientation += random.randint(-20, 20)
        angle = math.radians(self.farmer.orientation)
        distance = random.randint(50, 100)
        random_dest = (self.farmer.location.x + math.cos(angle) * distance, self.farmer.location.y + math.sin(angle) * distance)
        if not self.farmer.world.get_tile(Vector2(*random_dest)).walkable:
            try:
                self.random_dest(True)
            except RuntimeError:
                print "SOMEONE IS DROWNING!!"
        self.farmer.destination = Vector2(*random_dest)

    def entry_actions(self):
        self.random_dest()
