from aitools import GoalMachine

"""This file will be the customized version of the goal machine for this world"""

class WorldGOAP(GameMachine.GameMachine):
    
    def __init__(self, world):
        GameMachine.GameMachine.__init__(self)
        self.world = world
        
        self.expand_goal = GoalMachine.Goal("expand", 1)
        self.wood_goal = GoalMachine.Goal("wood", .5)
        self.food_goal = GoalMachine.Goal("food", .5)
        self.shelter_goal = GoalMachine.Goal("shelter", .75)
        
        self.add_goal(self.expand_goal)
        self.add_goal(self.wood_goal)
        self.add_goal(self.food_goal)
        self.add_goal(self.shelter_goal)
        
        self.spawn_lumberjack_action = GoalMachine.Action("spawn lumberjack", {"wood":-1})
        self.spawn_farmer_action = GoalMachine.Action("spawn farmer", {"wood":-1})
        self.build_house_action = GoalMachine.Action("build house", {"shelter":-1})
        self.build_dock_action = GoalMachine.Action("build dock", {"food":-1})
        self.spawn_fishing_ship_action = GoalMachine.Action("spawn fishing ship", {"food"-1})
        
class SpawnLumberjack(GoalMachine.Action):
    
    def __init__(self, world):
        GoalMachine.Action.__init__("spawn lumberjack", {"wood":-1})
        self.world = world
        
    def execute(self):
        self.world.find_building("Town Center")
