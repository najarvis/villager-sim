import GameEntity
import aitools.StateMachine as StateMachine
import math, random
from gametools.vector2 import Vector2

class FishingShip(GameEntity.GameEntity):
    
    def __init__(self, world, img):
        GameEntity.GameEntity.__init__(self, world, "Fishing Ship", img)
        
        self.speed = 50.
        self.view_range = 5
        
        self.searching_state = Searching(self)
        
        self.brain.add_state(self.searching_state)
        
class Searching(StateMachine.State):
    """Looking for something to gather"""
    
    def __init__(self, fishing_ship):
        
        StateMachine.State.__init__(self, "Searching")
        self.fishing_ship = fishing_ship
        
    def check_conditions(self):
        if self.fishing_ship.location.get_distance_to(self.fishing_ship.destination) < 7:
            self.fishing_ship.location = self.fishing_ship.destination.copy()
            self.random_dest()
    
    def do_actions(self):
        pass
    
    def entry_actions(self):
        self.random_dest()
    
    def exit_actions(self):
        pass
    
    def random_dest(self, recurse=False):
        # Function for going to a random destination
        if recurse:
            self.fishing_ship.orientation += 20
        else:
            self.fishing_ship.orientation += random.randint(-20, 20)
        angle = math.radians(self.fishing_ship.orientation)
        distance = random.randint(25, 50)
        random_dest = (self.fishing_ship.location.x + math.cos(angle) * distance, self.fishing_ship.location.y + math.sin(angle) * distance)
        if self.fishing_ship.world.get_tile(Vector2(*random_dest)).walkable:
            try:
                self.random_dest(True)
            except RuntimeError:
                print "SOMEONE IS DROWNING!!"
                
        self.fishing_ship.destination = Vector2(*random_dest)
    
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
