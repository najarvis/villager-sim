from StateMachine import *
from World import *
from GameEntity import *
from gametools.vector2 import Vector2
import glob
import FishingShip

from random import *

import pygame


class Building(GameEntity):
    def __init(self, world, name, img):
        GameEntity.__init__(self, world, name, img)

        self.tile_x, self.tile_y = pos
        self.cost = 100
        get_images(name)
        
        self.can_drop_food = False
        self.can_drop_wood = False


class LumberYard(Building):
    def __init__(self, world, img):
        name = "LumberYard"
        Building.__init__(self, world, name, img)

        self.Held = 0
        self.HeldMax = 50
        self.cost = 100

        self.world.MAXwood += self.HeldMax
        self.can_drop_wood = True


class Dock(Building):
    
    def __init__(self, world, img):
        name = "Dock"
        Building.__init__(self, world, name, img)

        self.Held = 0
        self.HeldMax = 25
        self.cost = 150
        
        self.can_drop_food = True

        self.world.MAXfood += self.HeldMax
        
        new_ship = FishingShip.FishingShip(self.world, self.world.fishingship_img)
        new_ship.location = self.location.copy()
        new_ship.brain.set_state("Searching")
        self.world.add_entity(new_ship)
        self.world.population += 1


class House(Building):
    def __init__(self, world, img):
        name = "House"
        Building.__init__(self, world, name, img)

        self.supports = 5
        self.cost = 30

        self.world.MAXpopulation += self.supports


class Manor(Building):
    def __init__(self, world, img):
        name = "Manor"
        Building.__init__(self, world, name, img)

        self.supports = 15
        self.cost = 100

        self.world.MAXpopulation += self.supports
        
class TownCenter(Building):
    def __init__(self, world, img):
        Building.__init__(self, world, "Town Center", img)
        
        self.can_drop_food = True
        self.can_drop_wood = True
        
        self.supports = 15
        self.cost = 500
        
        self.world.MAXpopulation += self.supports
        self.world.MAXWood += 50
        self.world.MAXFood += 50


class UnderConstruction(Building):
    def __init__(self, world, img, will_be):
        name = "UC"
        Building.__init__(self, world, name, img)
        self.will_be = will_be
        self.ttb = 30.0
        self.max_ttb = 30.0

    def create(self):
        self.world.add_built(self.will_be, self.location)
        self.world.remove_entity(self)
