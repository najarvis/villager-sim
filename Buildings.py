from aitools.StateMachine import *
import GameEntity
from gametools.vector2 import Vector2
import glob

import ImageFuncs
import pygame


class Building(GameEntity.GameEntity):
    def __init(self, world, name, image_string="Inn"):
        GameEntity.__init__(self, world, name, "Buildings/"+image_string)

        self.image_funcs = ImageFuncs(32, 32, pygame.image.load("Images/Buildings/TotalImage.png"))
        self.tile_x, self.tile_y = pos
        self.cost = 100
        get_images(name)
        
        self.can_drop_food = False
        self.can_drop_wood = False


class LumberYard(Building):
    def __init__(self, world, image_string="LumberYard"):
        Building.__init__(self, world, "Lumber Yard", image_string)

        self.image = self.image_funcs.get_irregular_image(2, 2, 2, 2)
        self.Held = 0
        self.HeldMax = 50
        self.cost = 100

        self.world.MAXwood += self.HeldMax
        self.can_drop_wood = True


class Dock(Building):
    
    def __init__(self, world, image_string="Dock"):
        Building.__init__(self, world, "Dock", image_string)

        self.image = self.image_funcs.get_irregular_image(2, 2, 2, 0)

        self.Held = 0
        self.HeldMax = 25
        self.cost = 150
        
        self.can_drop_food = True

        self.world.MAXfood += self.HeldMax
        
class House(Building):
    def __init__(self, world, image_string="House"):
        Building.__init__(self, world, "House", image_string)

        self.supports = 5
        self.cost = 30

        self.world.MAXpopulation += self.supports


class Manor(Building):
    def __init__(self, world, image_string="Manor"):
        Building.__init__(self, world, "Manor", image_string)

        self.image = self.image_funcs.get_irregular_image(2, 2, 2, 4)

        self.supports = 15
        self.cost = 100

        self.world.MAXpopulation += self.supports
        
class TownCenter(Building):
    def __init__(self, world, image_string="Manor"):
        Building.__init__(self, world, "Town Center", image_string)
       
        self.image = self.image_funcs.get_irregular_image(2, 2, 2, 6)

        self.can_drop_food = True
        self.can_drop_wood = True
        
        self.supports = 15
        self.cost = 500
        
        self.world.MAXpopulation += self.supports
        self.world.MAXWood += 50
        self.world.MAXFood += 50


class UnderConstruction(Building):
    def __init__(self, world, image_string, will_be):
        Building.__init__(self, world, "Under Construction", image_string)
        self.will_be = will_be
        self.ttb = 30.0
        self.max_ttb = 30.0

    def create(self):
        self.world.add_built(self.will_be, self.location)
        self.world.remove_entity(self)


class StoreShed(Building):

    def __init__(self, world, image_string):
        Building.__init__(self, world, "Store Shed", image_string)
