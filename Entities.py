from aitools.StateMachine import *
from World import *
from GameEntity import *
from gametools.vector2 import *

from random import *


class Tree(GameEntity):
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "Tree", image)


class Sapling(GameEntity):
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "Sapling", image)
        growing_state = Growing(self)
        self.brain.add_state(growing_state)
        self.ttg = 30.0


class Growing(State):
    def __init__(self, Sapling):
        State.__init__(self, "Growing")
        self.Sapling = Sapling

    def check_conditions(self):
        if self.Sapling.ttg <= 0:
            new_tree = Tree(self.Sapling.world, tree_image)
            new_tree.location = self.Sapling.location.copy()
            self.Sapling.world.add_entity(new_tree)
            self.Sapling.world.remove_entity(self.Sapling)

    def do_actions(self):
        self.Sapling.ttg -= self.Sapling.tp
        # print self.Sapling.ttg
