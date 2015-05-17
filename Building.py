from StateMachine import *
from World import *
from GameEntity import *
from vector2 import *
import glob
from random import *

import pygame

class Building(GameEntity):
    
    def __init(self, world, name, img):
        GameEntity.__init__(self,world, name, img)
        
        self.tile_x, self.tile_y = pos
        self.cost = 100
        get_images(name)
        
    def get_images(self, name):
        self.images = []
        try:
            if name!="UC":
                self.basic_img = pygame.image.load(glob.glob("Images/Buildings/%s.png"%name))
                self.images.append(self.basic_img)
                self.red_img = pygame.image.load(glob.glob("Images/Buildings/RED_%s.png"%name))
                self.images.append(self.red_img)
                self.dark_img = pygame.image.load(glob.glob("Images/Buildings/DARK_%s.png"%name))
                self.images.append(self.dark_img)
                self.selected_img = pygame.image.load(glob.glob("Images/Buildings/SELECTED_%s_Icon"%name))
                self.images.append(self.selected_img)
                self.icon_img = pygame.image.load(glob.glob("%s_Icon.png"%name))
                self.images.append(self.selected_img)
            else:
                self.house_img = pygame.image.load("Images/Buildings/UC_House.png")
                self.dock_img = pygame.image.load("Images/Buildings/UC_Dock.png")
                self.manor_img = pygame.image.load("UC.png")
                self.lumber_img = pygame.image.load("UC.png")
                
                self.images.append(self.house_img)
                self.images.append(self.dock_img)
                self.images.append(self.manor_img)
                self.images.append(self.lumber_img)
        except Exception:
            pass
        for i in self.images:
            i.set_colorkey((255,0,255))
            
    def convert_all(self):
        for i in self.images:
            i.convert()
            
class LumberYard(Building):
    def __init__(self, world, img):
        name = "LumberYard"
        Building.__init__(self, world, name, img)
        
        self.Held = 0
        self.HeldMax = 50
        self.cost = 100

        self.world.MAXwood+=self.HeldMax
        
class Dock(Building):
    
    def __init__(self, world, img):
        
        name = "Dock"
        Building.__init__(self, world, name, img)
        
        self.Held = 0
        self.HeldMax = 25
        self.cost = 150

        self.world.MAXfood+=self.HeldMax
        
class House(Building):
    
    def __init__(self, world, img):
        name = "House"
        Building.__init__(self, world, name, img)
        
        self.supports = 5
        self.cost = 30
        
        self.world.MAXpopulation+=self.supports
        
class Manor(Building):
    
    def __init__(self, world, img):
        name = "Manor"
        Building.__init__(self, world, name, img)
        
        self.supports = 15
        self.cost = 100
        
        self.world.MAXpopulation+=self.supports
        
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