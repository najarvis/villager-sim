from StateMachine import *
from World import *

from GameEntity import *
from gametools.vector2 import Vector2
from Entities import *

from Tile import *

from random import *

blank_grass_img = pygame.image.load("Images/Tiles/MinecraftGrass.png")


class Villager(GameEntity):
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "Villager", image)
        exploring_state = Villager_Exploring(self)
        delivering_state = Villager_Delivering(self)
        chopping_state = Villager_Chopping(self)
        sleeping_state = Villager_sleeping(self)

        self.brain.add_state(exploring_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(chopping_state)
        self.brain.add_state(sleeping_state)

        self.speed = 100
        self.carrying = None


class Villager_sleeping(State):
    def __init__(self, Villager):
        State.__init__(self, "sleeping")
        self.Villager = Villager

    def check_conditions(self):
        if (self.Villager.world.clock_degree < 190 or self.Villager.world.clock_degree > 250) and (
            self.Villager.world.wood < self.Villager.world.MAXwood):
            return "exploring"

    def entry_actions(self):
        self.Villager.speed = 100.
        self.Villager.destination = self.Villager.LastLumberYard.location.copy()


class Villager_Exploring(State):
    def __init__(self, Villager):

        State.__init__(self, "exploring")
        self.Villager = Villager

    def random_dest(self):

        w, h = self.Villager.world.size
        self.Villager.destination = Vector2(randint(0, w/12), randint(0, h/12))

    def do_actions(self):
        if self.Villager.location.get_distance_to(
                self.Villager.destination) < 2.0:  # This is because it will always be < 1 away, but never get it exactly
            self.random_dest()

    def check_conditions(self):

        if (self.Villager.world.clock_degree < 250. and self.Villager.world.clock_degree > 190.) or (
            self.Villager.world.wood >= self.Villager.world.MAXwood):
            return "sleeping"

        for TREE_pos in self.Villager.world.TreeLocations.itervalues():
            if TREE_pos.get_distance_to(self.Villager.location) < 200:
                self.Villager.destination = TREE_pos.copy()

                pos = self.Villager.world.get_tile_pos(self.Villager.destination)
                tile = self.Villager.world.TileArray[int(pos.x)][int(pos.y)]

                return "chopping"

    def entry_actions(self):
        self.random_dest()
        self.Villager.speed = 100.


class Villager_Chopping(State):
    def __init__(self, Villager):

        State.__init__(self, "chopping")
        self.Villager = Villager
        self.Tree_id = None

    def check_conditions(self):

        pos = self.Villager.world.get_tile_pos(self.Villager.destination)
        if self.Villager.world.TileArray[int(pos.x)][int(pos.y)].name != "TreePlantedTile_W":
            return "exploring"

        if self.Villager.world.wood >= self.Villager.world.MAXwood:
            return "sleeping"

        if self.Villager.location.get_distance_to(self.Villager.destination) < 5.0:
            # Creates a new blank tile, then replaces the tree tile with it
            new_tile = TreePlantedTile_w(self.Villager.world, blank_grass_img)
            new_tile.location = self.Villager.world.get_tile_pos(self.Villager.destination)*32
            new_tile.rect.topleft = new_tile.location

            self.Villager.world.background.blit(new_tile.img, new_tile.location)
            self.Villager.Tile = self.Villager.world.TileArray[int(new_tile.location.x/32)][int(new_tile.location.y/32)]

            # Removes the old tree from the world.
            if self.Villager.world.remove_tree(self.Villager.Tile.id) == None:
                return "exploring"

            if self.Villager.Tile.name == "TreePlantedTile_W":
                self.Villager.carrying = "tree"
            else:
                print "ERROR:", self.Villager.Tile.name
                self.Villager.carrying = "sapling"
            return "delivering"

    def entry_actions(self):
        pos = self.Villager.world.get_tile_pos(self.Villager.destination)
        tile = self.Villager.world.TileArray[int(pos.x)][int(pos.y)]
        if tile.name != "TreePlantedTile_W":
            return "exploring"


class Villager_Delivering(State):
    def __init__(self, Villager):

        State.__init__(self, "delivering")
        self.Villager = Villager

    def check_conditions(self):

        if self.Villager.world.wood >= self.Villager.world.MAXwood:
            return "sleeping"

        if self.Villager.location.get_distance_to(self.Villager.destination) < 5.0:
            if self.Villager.carrying == "tree":
                self.Villager.world.wood += 5
            else:
                self.Villager.world.wood += 1
            return "exploring"

    def entry_actions(self):

        self.Villager.speed = 85.
        des = self.Villager.world.get_close_entity("LumberYard", self.Villager.location, 100)
        if des == None:
            des = self.Villager.world.get_close_entity("LumberYard", self.Villager.location, 300)
            if des == None:
                des = self.Villager.LastLumberYard

        self.Villager.destination = des.location
