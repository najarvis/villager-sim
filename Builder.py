from StateMachine import *
from World import *
from GameEntity import *
from vector2 import *

from Building import *

from random import *

import pygame


class Builder(GameEntity):
    
    def __init__(self, world, image, rest):
        GameEntity.__init__(self,world,"Builder",image)
        
        self.current_build = None
        
        self.speed = 100.0
        
        self.building_state = Builder_Building(self)
        self.Idle_state = Builder_Idle(self)
        self.Finding_state = Builder_Finding(self)
        
        self.brain.add_state(self.building_state)
        self.brain.add_state(self.Idle_state)
        self.brain.add_state(self.Finding_state)
        
        
        self.IdleLocation = rest.location.copy()
        
        
class Builder_Building(State):
    
    def __init__(self, Builder):
        State.__init__(self, "Building")
        self.Builder = Builder
        
    def check_conditions(self):
        if self.building_complete>=5.0:
            
            self.Builder.target.create()
            
            self.Builder.world.BuildingQueue.remove(self.Builder.target)
            return "Finding"
    
    def do_actions(self):
        self.building_complete+=self.Builder.tp
    
    def entry_actions(self):
        
        self.Builder.destination = self.Builder.location.copy()
        self.building_complete = 0.0
        
class Builder_Finding(State):   #Finding a suitable place to build.
    """If:
    Lumber Yard - In the woods not near anything else
    Docks - Edge of the water, decently distanced from others
    House - Somewhere in the town area
    Manor - near top of the map or maybe replaces a house.
    """
    
    def __init__(self, Builder):
        State.__init__(self, "Finding")
        self.Builder = Builder
        
    def check_conditions(self):
        if len(self.Builder.world.BuildingQueue) == 0:
            return "Idle" 
        
        if self.Builder.location.get_distance_to(self.Builder.destination) < 2:
            return "Building"
          
    def do_actions(self):
        pass
    
    def entry_actions(self):
        try:
            self.Builder.destination = self.Builder.world.BuildingQueue[0].location.copy()
            self.Builder.target = self.Builder.world.BuildingQueue[0]
              
        except IndexError:
            pass
            
class Builder_Idle(State):
    
    def __init__(self, Builder):
        State.__init__(self, "Idle")
        self.Builder = Builder
    
    def entry_actions(self):
        
        self.Builder.destination = self.Builder.IdleLocation
        
    def check_conditions(self):
        if len(self.Builder.world.BuildingQueue) >= 1:
            return "Finding"
    