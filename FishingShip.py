import GameEntity
import aitools.StateMachine as StateMachine
import math, random
from gametools.vector2 import Vector2
import BaseFunctions


class FishingShip(GameEntity.GameEntity):
    
    def __init__(self, world, img):
        GameEntity.GameEntity.__init__(self, world, "Fishing Ship", img)
        
        self.speed = 50.0 * (1.0 / 60.0)
        self.view_range = 5
        
        self.searching_state = Searching(self)
        
        self.brain.add_state(self.searching_state)
        
class Searching(StateMachine.State):
    """Looking for something to gather"""
    
    def __init__(self, fishing_ship):
        
        StateMachine.State.__init__(self, "Searching")
        self.fishing_ship = fishing_ship
        
    def check_conditions(self):
        if self.fishing_ship.location.get_distance_to(self.fishing_ship.destination) < self.fishing_ship.speed:
            BaseFunctions.random_dest(self.fishing_ship)
    
    def do_actions(self):
        pass
    
    def entry_actions(self):
        BaseFunctions.random_dest()
    
    def exit_actions(self):
        pass
    
class Gathering(StateMachine.State):
    """In the state of gathering"""
    
    def __init__(self, fishing_ship):
        
        StateMachine.State.__init__(self, "Gathering")
        self.fishing_ship = fishing_ship
        
    def check_conditions(self):
        pass
    
    def do_actions(self):
        pass
    
    def entry_actions(self):
        pass
    
    def exit_actions(self):
        pass
    
class Returning(StateMachine.State):
    """Returning what is gathered to the dock"""
    
    def __init__(self, fishing_ship):
        StateMachine.State.__init__(self, "Returning")
        self.fishing_ship = fishing_ship
        
    def check_conditions(self):
        pass
    
    def do_actions(self):
        pass
    
    def entry_actions(self):
        pass
    
    def exit_actions(self):
        pass
