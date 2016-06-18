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

class Farmer(GameEntity):

    def __init__(self, world, image_string):
        # Initializing the class
        GameEntity.__init__(self, world, "Farmer", "Entities/"+image_string)

        # Creating the states
        planting_state = Farmer_Planting(self)

        # Adding states to the brain
        self.brain.add_state(planting_state)

        self.max_speed = 80.0 * (1.0 / 60.0)
        self.speed = self.max_speed

        self.worldSize = world.world_size
        self.TileSize = self.world.tile_size

        # animation variables
        self.animation = Ani(6,10)
        self.pic = pygame.image.load("Images/Entities/map.png")
        self.img_func = ImageFuncs(18, 17,self.pic)
        self.sprites = self.img_func.get_images(6,0,0)
        self.hit = 0
        self.update()

    def update(self):
        # Updates image every 10 cycles and adds 1 to the 4 hit dig
        self.image = self.sprites[self.animation.get_frame()]
        self.image.set_colorkey((255,0,255))
        if self.animation.finished == True:
            self.hit += 1
            self.animation.finished = False


class Farmer_Planting(State):

    def __init__(self, Farmer):

        State.__init__(self, "Planting")
        self.farmer = Farmer

    def check_conditions(self):

        if self.farmer.location.get_distance_to(self.farmer.destination) < 15:
            self.farmer.destination = Vector2(self.farmer.location)
            self.farmer.update()

    def do_actions(self):

        if self.farmer.location == self.farmer.destination and self.farmer.hit >= 4 and TileFuncs.get_tile(
                self.farmer.world,self.farmer.location).plantable == 1:
            self.plant_seed()

        if self.farmer.location == self.farmer.destination and self.farmer.hit != 4 and TileFuncs.get_tile(
                self.farmer.world, self.farmer.location).plantable != 1:
            self.random_dest()

    def plant_seed(self):
        # Function for planting trees

        # Test to see if the tile the farmer is on is a tile that a tree can be planted on
        if TileFuncs.get_tile(self.farmer.world,self.farmer.location).plantable == 1:
            self.farmer.hit = 0
            self.farmer.update()
            old_tile = TileFuncs.get_tile(self.farmer.world,Vector2(self.farmer.location))

            darkness = pygame.Surface((32, 32))
            darkness.set_alpha(old_tile.darkness)

            new_tile = Tile.Baby_Tree(self.farmer.world, "GrassWithCenterTree")

            new_tile.darkness = old_tile.darkness

            new_tile.location = TileFuncs.get_tile_pos(self.farmer.world,self.farmer.destination)*32
            new_tile.rect.topleft = new_tile.location
            new_tile.color = old_tile.color

            self.farmer.world.tile_array[int(new_tile.location.y/32)][int(new_tile.location.x/32)] = new_tile
            self.farmer.world.world_surface.blit(new_tile.img, new_tile.location)
            self.farmer.world.world_surface.blit(darkness, new_tile.location)

        # Goes to a random destination no matter what
        self.farmer.hit = 0
        self.random_dest()

    def random_dest(self, recurse=False, r_num=0, r_max=5):
        # Function for going to a random destination
        if recurse:
            self.farmer.orientation += 20
        else:
            self.farmer.orientation += random.randint(-20, 20)
        angle = math.radians(self.farmer.orientation)
        distance = random.randint(50, 100)
        random_dest = Vector2(self.farmer.location.x + math.cos(angle) * distance, self.farmer.location.y + math.sin(angle) * distance)
         
         # If the destination will go off the map, it is NOT a valid move under any circumstances.
        bad_spot = False
        if (0 > random_dest.x > self.farmer.world.world_size[0] or \
            0 > random_dest.y > self.farmer.world.world_size[1]):
            bad_spot = True

        if ((not TileFuncs.get_tile(self.farmer.world, random_dest).walkable and r_num < r_max) or bad_spot):
            self.random_dest(True, r_num+1)
       
        self.farmer.destination = random_dest

    def entry_actions(self):
        self.random_dest()
