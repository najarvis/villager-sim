"""This class is going to be tasked with planting and harvesting crops. This
   class used to plant trees, however this has been moved to Arborist (which
   is the name of someone who takes care of trees you pleb)."""

import aitools.StateMachine
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

class Farmer(GameEntity):
    """The main class for Farmer. See above for the description"""

    def __init__(self, world, image_string):
        """Basic initialization"""

        # Initializing the class
        GameEntity.__init__(self, world, "Farmer", "Entities/"+image_string)

        # Creating the states
        tilling_state = Farmer_Tilling(self)

        # Adding states to the brain
        self.brain.add_state(tilling_state)

        self.max_speed = 80.0 * (1.0 / 60.0)
        self.speed = self.max_speed
        self.base_speed = self.speed

        self.worldSize = world.world_size
        self.TileSize = self.world.tile_size

class Farmer_Tilling(aitools.StateMachine.State):
    
    def __init__(self, farmer):
        aitools.StateMachine.State.__init__(self, "Tilling")
        self.farmer = farmer

    def entry_actions(self):
        BaseFunctions.random_dest(self.farmer)

    def do_actions(self):
        current_tile = TileFuncs.get_tile(self.farmer.world, self.farmer.location)
        if current_tile.tillable:
            darkness = pygame.Surface((self.farmer.TileSize, self.farmer.TileSize))
            darkness.set_alpha(current_tile.darkness)

            new_tile = Tile.SoilTile(self.farmer.world, "Soil2")
            new_tile.darkness = darkness

            new_tile.location = current_tile.location
            new_tile.rect.topleft = new_tile.location
            new_tile.color = current_tile.color # TODO: Figure out what this does.

            self.farmer.world.tile_array[int(new_tile.location.y / 32)][int(new_tile.location.x / 32)] = new_tile
            self.farmer.world.world_surface.blit(new_tile.img, new_tile.location)
            self.farmer.world.world_surface.blit(darkness, new_tile.location)
            # TODO: Update the minimap

            BaseFunctions.random_dest(self.farmer)

        elif self.farmer.location.get_distance_to(self.farmer.destination) < self.farmer.speed:
            BaseFunctions.random_dest(self.farmer)

    def check_conditions(self):
        pass

    def exit_actions(self):
        pass
