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
import BaseFunctions

class Arborist(GameEntity):

    def __init__(self, world, image_string):
        # Initializing the class
        GameEntity.__init__(self, world, "Arborist", "Entities/"+image_string)

        # Creating the states
        planting_state = Arborist_Planting(self)

        # Adding states to the brain
        self.brain.add_state(planting_state)

        self.max_speed = 80.0 * (1.0 / 60.0)
        self.speed = self.max_speed
        self.base_speed = self.speed

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


class Arborist_Planting(State):

    def __init__(self, Arborist):

        State.__init__(self, "Planting")
        self.arborist = Arborist

    def check_conditions(self):

        if self.arborist.location.get_distance_to(self.arborist.destination) < 15:
            self.arborist.destination = Vector2(self.arborist.location)
            self.arborist.update()

    def do_actions(self):

        if self.arborist.location == self.arborist.destination and self.arborist.hit >= 4 and TileFuncs.get_tile(
                self.arborist.world,self.arborist.location).plantable == 1:
            self.plant_seed()

        if self.arborist.location == self.arborist.destination and self.arborist.hit != 4 and TileFuncs.get_tile(
                self.arborist.world, self.arborist.location).plantable != 1:
            BaseFunctions.random_dest(self.arborist)

    def plant_seed(self):
        # Function for planting trees

        # Test to see if the tile the arborist is on is a tile that a tree can be planted on
        if TileFuncs.get_tile(self.arborist.world,self.arborist.location).plantable == 1:
            self.arborist.hit = 0
            self.arborist.update()
            old_tile = TileFuncs.get_tile(self.arborist.world,Vector2(self.arborist.location))

            darkness = pygame.Surface((32, 32))
            darkness.set_alpha(old_tile.darkness)

            new_tile = Tile.Baby_Tree(self.arborist.world, "GrassWithCenterTree")

            new_tile.darkness = old_tile.darkness

            new_tile.location = TileFuncs.get_tile_pos(self.arborist.world,self.arborist.destination)*32
            new_tile.rect.topleft = new_tile.location
            new_tile.color = old_tile.color

            self.arborist.world.tile_array[int(new_tile.location.y/32)][int(new_tile.location.x/32)] = new_tile
            self.arborist.world.world_surface.blit(new_tile.img, new_tile.location)
            self.arborist.world.world_surface.blit(darkness, new_tile.location)

        # Goes to a random destination no matter what
        self.arborist.hit = 0
        BaseFunctions.random_dest(self.arborist)

    def entry_actions(self):
        BaseFunctions.random_dest(self.arborist)
