import pygame
from pygame.locals import *

import math

from vector2 import Vector2

import Tile

from Building import *
from Builder import *

from Villager import *
from Lumberjack import *
from Farmer import *

from Clips import Clips

import GoalMachine

from random import randint, seed
from VoronoiMapGen import point, mapGen

lush_grass_img = pygame.image.load("Images/Tiles/MyGrass.png")
grass_img = pygame.image.load("Images/Tiles/MinecraftGrass.png")
water_img = pygame.image.load("Images/Tiles/AndrewWater2.png")
sand_img = pygame.image.load("Images/Tiles/Sand.png")
cobble_img = pygame.image.load("Images/Tiles/AndrewCobble2.png")
SStone_img = pygame.image.load("Images/Tiles/AndrewSmoothStone.png")
deepwater_img = pygame.image.load("Images/Tiles/AndrewWater.png")
snow_img = pygame.image.load("Images/Tiles/MinecraftSnow.png")
tree_img = pygame.image.load("Images/Tiles/GrassWithCenterTree.png")

lumber_yard_img = pygame.image.load("Images/Buildings/LumberYard.png")
house_img = pygame.image.load("Images/Buildings/House.png")
dock_img = pygame.image.load("Images/Buildings/Dock.png")
manor_img = pygame.image.load("Images/Buildings/Manor.png")
uc_img = pygame.image.load("Images/Buildings/UC.png")
ucw_img = pygame.image.load("Images/Buildings/UC_Dock.png")
uc_house_img = pygame.image.load("Images/Buildings/UC_House.png")

lumberjack_img = pygame.image.load("Images/Entities/Lumberjack.png")
farmer_img = pygame.image.load("Images/Entities/Farmer.png")
builder_img = pygame.image.load("Images/Entities/Builder.png")
fishingship_img = pygame.image.load("Images/Entities/fishingship.png")


class World(object):
    """This class holds and does everything basically."""

    def __init__(self, world_dimensions, font, rand_seed, screen_size):
        
        """Seed the map"""
        self.seed = rand_seed
        if self.seed is not None:
            seed(self.seed)
            
        """Set up dimensions"""
        self.TileSize = 32
        self.world_dimensions = world_dimensions
        self.size = self.world_dimensions[0] * self.TileSize, self.world_dimensions[1] * self.TileSize  # How big the map is
        
        self.w, self.h = self.size  # Certain functions entities need this.
        self.center = Vector2(self.w / 2, self.h / 2)
        self.background_pos = self.center.copy()

        """The clock that will handle all timing"""
        self.clock = pygame.time.Clock()

        """Set up the font the sidebar will use"""
        self.font = font
        self.font_size = self.font.size("A")[1]

        """Convert all those images"""
        self.convert_all()
        
        """Set up the goal machine"""
        self.goal_machine = GoalMachine.GoalMachine()
        
        self.expand_goal = GoalMachine.Goal("expand", 1)
        self.wood_goal = GoalMachine.Goal("wood", .5)
        self.food_goal = GoalMachine.Goal("food", .5)
        self.shelter_goal = GoalMachine.Goal("shelter", .75)
        
        self.goal_machine.add_goal(self.expand_goal)
        self.goal_machine.add_goal(self.wood_goal)
        self.goal_machine.add_goal(self.food_goal)
        self.goal_machine.add_goal(self.shelter_goal)
        
        self.spawn_lumberjack_action = GoalMachine.Action("spawn lumberjack", {"wood":-1})
        self.spawn_farmer_action = GoalMachine.Action("spawn farmer", {"wood":-1})
        self.build_house_action = GoalMachine.Action("build house", {"shelter":-1})
        self.build_dock_action = GoalMachine.Action("build dock", {"food":-1})
        self.spawn_fishing_ship_action = GoalMachine.Action("spawn fishing ship", {"food":-1})
        
        """Set up a new world"""
        self.new_world()
        self.cliper = Clips(self, screen_size)

    def new_world(self):
        try:
            del self.full_surface
        except AttributeError:
            pass
        
        self.mapGenerator = mapGen()
        vorMap = self.mapGenerator.negativeArray(self.mapGenerator.reallyCoolFull(self.world_dimensions,num_p=23))

        self.map_width = self.map_height = len(vorMap)

        self.minimap_img = pygame.Surface((self.map_width, self.map_height))

        self.TileArray = [[0 for i in xrange(self.map_width)] for a in xrange(self.map_height)]

        self.TreeID = 0
        self.TreeLocations = {}
        self.Baby_TreeID = 0
        self.baby_tree_locations = {}

        self.buildings = {"LumberYard": {},
                          "Dock": {},
                          "House": {},
                          "Manor": {},
                          "Town Center": {},
                          "UC": {}}

        self.building = {}
        self.entities = {}  # Stores all entities the game processes
        # Each entity is given a unique id so the program can find it
        self.entity_id = 0
        self.wood = 0  # Probably will add other resources
        self.MAXwood = 50
        self.food = 0
        self.MAXfood = 0
        self.population = 0
        self.MAXpopulation = 15
        self.background_pos = self.center.copy()
        
        self.shadowDown = 3.0 / ((self.size[0] / self.TileSize) / 128.0)

        self.full_surface = pygame.Surface(self.size, HWSURFACE)

        self.clock_degree = 0  # Used for the clock

        self.BuildingQueue = []

        for i in xrange(self.map_width):
            self.current_height = 0
            w_last = False
            for a in xrange(self.map_height):

                f_color = vorMap[i][a]
                color = f_color
                to_rotate = 1

                if color < 110:
                    colorb = 0
                    tile = Tile.WaterTile(self, self.water_img)

                    last_image = self.sand_img
                    last_color = 0
                    to_rotate = False

                elif color >= 110 and color < 120:
                    colorb = 110
                    tile = Tile.BeachTile(self, self.sand_img)
                    last_color = 110

                elif color >= 120 and color < 140:
                    colorb = 120
                    tile = Tile.GrassTile(self, self.grass_img)
                    last_color = 120

                elif color >= 140 and color < 160:
                    colorb = 140
                    tile = Tile.TreePlantedTile(self, self.grass_img)
                    last_color = 140

                elif color >= 160 and color < 170:
                    colorb = 160

                    tile = Tile.TreePlantedTile_w(self, self.tree_img)
                    tile.location = Vector2(i << 5, a << 5)
                    tile.rect.topleft = tile.location
                    tile.id = self.TreeID

                    self.TreeLocations[str(self.TreeID)] = tile.location
                    self.TreeID += 1

                    to_rotate = False

                    last_color = 160

                elif color >= 170 and color < 190:
                    colorb = 170
                    tile = Tile.TreePlantedTile(self, self.grass_img)
                    last_color = 170

                elif color >= 190 and color < 220:
                    colorb = 190
                    tile = Tile.SmoothStoneTile(self, self.SStone_img)
                    to_rotate = False
                    last_color = 190

                else:
                    colorb = 220
                    tile = Tile.SnowTile(self, self.snow_img)
                    last_color = 220

                # Shadows----
                fake_color = color
                if color < 110:
                    fake_color = 110
                if fake_color > self.current_height - self.shadowDown:

                    dark_surface = pygame.Surface((32, 32))
                    dark_surface.set_alpha(0)
                    if color >= 110:
                        self.current_height = fake_color

                    else:
                        self.current_height -= self.shadowDown

                else:
                    self.current_height -= self.shadowDown
                    dark_surface = pygame.Surface((32, 32))
                    dark_surface.set_alpha(128)
                # -----------

                tile.location = Vector2(i << 5, a << 5)
                tile.rect.topleft = tile.location
                tile.color = color

                if to_rotate:
                    tile.img = pygame.transform.rotate(tile.img, randint(0, 4) * 90)

                self.full_surface.blit(tile.img, tile.location)

                dark_surface2 = pygame.Surface((32, 32))

                alph = 220 - color
                if color >= 190 and color < 220:
                    alph = 330 - color

                dark_surface2.set_alpha(alph)

                tile.darkness = alph

                self.full_surface.blit(dark_surface, tile.location)
                self.full_surface.blit(dark_surface2, tile.location)

                # self.minimap_img.blit(combined_img.subsurface((0,0,1,1)), (i,a))
                self.minimap_img.blit(
                    tile.img.subsurface(
                        (0, 0, 1, 1)), (i, a))
                self.minimap_img.blit(
                    dark_surface.subsurface(
                        (0, 0, 1, 1)), (i, a))
                self.minimap_img.blit(
                    dark_surface2.subsurface(
                        (0, 0, 1, 1)), (i, a))

                self.TileArray[a][i] = tile

        self.populate()

    def populate(self):
        """This is the initial code that spawns the initial entities"""
        FARMER_COUNT = 5
        VILLAGER_COUNT = 5
        BUILDER_COUNT = 1

        # adds all the people and make sure they don't go all ape shit
        lumber1 = LumberYard(self, self.lumberyard_img)
        lumber1.location = Vector2(self.w / 2, self.h / 2)
        lumber1.tile_x, lumber1.tile_y = 4, 4
        self.add_entity(lumber1)

        for villager_num in xrange(VILLAGER_COUNT):  # Adds all Wood Cutters
            villager = Lumberjack(self, self.lumberjack_img)
            villager.location = lumber1.location.copy()
            villager.LastLumberYard = lumber1
            villager.brain.set_state("Searching")
            self.add_entity(villager)
            self.population += 1

        for builder_num in xrange(BUILDER_COUNT):
            builder = Builder(self, self.builder_img, lumber1)
            builder.location = lumber1.location.copy()
            builder.brain.set_state("Idle")
            self.add_entity(builder)
            self.population += 1

        for farmer_num in xrange(FARMER_COUNT):  # Adds all the farmers
            farmer = Farmer(self, self.farmer_img)
            farmer.location = lumber1.location.copy()
            farmer.brain.set_state("Planting")
            self.add_entity(farmer)
            self.population += 1

    def add_building(self, building, pos):

        buildable = self.test_buildable(building, 0, pos)

        if buildable:
            Build = buildable[1]
            Build.location = self.get_tile_pos(pos - self.background_pos) * 32
            self.add_entity(Build)
            self.buildings[building] = Build
            self.BuildingQueue.append(Build)
            return 1

    def add_built(self, building, pos):

        buildable = self.test_buildable(building, 1, pos)

        if buildable:
            Build = buildable[1]
            Build.location = pos
            self.add_entity(Build)
            self.buildings[building] = Build
            return 1

    def test_buildable(self, building, built, pos):

        if building == "LumberYard":
            if built:
                Build = LumberYard(self, self.lumberyard_img)
            else:
                Build = UnderConstruction(self, self.uc_img, "LumberYard")

        elif building == "House":
            if built:
                Build = House(self, self.house_img)
            else:
                Build = UnderConstruction(self, self.uc_house_img, "House")

        elif building == "Dock":
            if built:
                Build = Dock(self, self.dock_img)
            else:
                Build = UnderConstruction(self, self.ucw_img, "Dock")

        elif building == "Manor":
            if built:
                Build = Manor(self, self.manor_img)
            else:
                Build = UnderConstruction(self, self.uc_img, "Manor")

        buildable = 1
        land = 0
        water = 0

        Twidth, Theight = Build.image.get_size()
        for i in range(Twidth >> 5):
            for j in range(Theight >> 5):
                try:
                    if built:
                        test_tile = self.get_tile(
                            Vector2((pos.x - 32) + (i << 5), (pos.y - 32) + (j << 5)))
                        # print "A", test_tile, test_tile.location
                    else:
                        test_tile = self.get_tile(Vector2(((pos.x - 32) - self.background_pos.x) + (i << 5),
                                                          ((pos.y - 32) - self.background_pos.y) + (j >> 5)))
                        # print "B", test_tile, test_tile.location

                    if test_tile.buildable != 1 and building != "Dock":
                        buildable = 0
                        return False
                    
                    elif building == "Dock":
                        if test_tile.buildable_w:
                            water += 1
                        else:
                            land += 1
                            
                except IndexError:
                    return False
                
                except AttributeError:
                    return False

        if building == "Dock":
            if water >= 1 and land <= 2 and land > 0:
                buildable = 1
                return True, Build
            else:
                buildable = 0
                return False

        return True, Build

    def convert_all(self):
        self.lush_grass_img = lush_grass_img.convert()
        self.grass_img = grass_img.convert()
        self.water_img = water_img.convert()
        self.sand_img = sand_img.convert()
        self.cobble_img = cobble_img.convert()
        self.SStone_img = SStone_img.convert()
        self.deepwater_img = deepwater_img.convert()
        self.snow_img = snow_img.convert()
        self.tree_img = tree_img.convert()

        self.lumberyard_img = lumber_yard_img.convert()
        self.lumberyard_img.set_colorkey((255, 0, 255))

        self.house_img = house_img.convert()
        self.house_img.set_colorkey((255, 0, 255))

        self.dock_img = dock_img.convert()
        self.dock_img.set_colorkey((255, 0, 255))

        self.manor_img = manor_img.convert()
        self.manor_img.set_colorkey((255, 0, 255))

        self.uc_img = uc_img.convert_alpha()
        self.ucw_img = ucw_img.convert()
        self.ucw_img.set_colorkey((255, 0, 255))
        self.uc_house_img = uc_house_img.convert()
        self.uc_house_img.set_colorkey((255, 0, 255))

        self.lumberjack_img = lumberjack_img.convert()
        self.farmer_img = farmer_img.convert()
        self.builder_img = builder_img.convert()
        self.fishingship_img = fishingship_img.convert()
        self.fishingship_img.set_colorkey((255, 0, 255))

    def grow_trees(self, trees):
        for i in range(len(trees)):
            ran = randint(0, 100)
            if ran == 1 and len(trees) > 0:
                try:
                    a = trees.keys()
                    old_tile = self.get_tile(trees[a[i]])
                    darkness = pygame.Surface((32, 32))
                    darkness.set_alpha(old_tile.darkness)

                    new_tile = TreePlantedTile_w(self, tree_img)

                    new_tile.darkness = old_tile.darkness

                    new_tile.location = old_tile.location
                    new_tile.rect.topleft = new_tile.location
                    new_tile.color = old_tile.color

                    new_tile.id = self.TreeID
                    self.TreeID += 1

                    self.TileArray[int(new_tile.location.y / 32)][int(new_tile.location.x / 32)] = new_tile
                    self.full_surface.blit(new_tile.img, new_tile.location)
                    self.full_surface.blit(darkness, new_tile.location)

                    del self.baby_tree_locations[str(a[i])]
                except IndexError:
                    pass

    def add_entity(self, entity):  # Used to add entities to the world

        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):  # function for removing an entity
        del self.entities[entity.id]

    def remove_tree(self, tree_id):

        try:
            del self.TreeLocations[str(tree_id)]
            return 0
        except KeyError:
            return None

    def get(self, entity_id):  # Return an entity

        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def process(self, time_passed):  # Run the world through 1 cycle

        for entity in self.entities.values():
            entity.process(time_passed)

    def render(self, surface):
        surface.blit(self.full_surface, self.background_pos)

        for entity in self.entities.itervalues():
            entity.render(surface)

        #surface.blit(self.background_over, (0, 0))

    def render_all(self, surface, tp, mouse_pos):
        self.cliper.render(surface, tp, mouse_pos)

    def get_close_entity(self, name, location, range=100.):

        location = Vector2(*location)

        for entity in self.entities.itervalues():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if range == -1:
                    return entity
                if distance < range:
                    return entity

        return None

    def get_tile(self, location):
        tile = self.get_tile_pos(location)
        try:
            return self.TileArray[int(tile.y)][int(tile.x)]
        except IndexError:
            return Tile.NullTile(self, self.sand_img)

    def get_tile_pos(self, location):
        return Vector2(int(location.x) >> 5, int(location.y) >> 5)
    
    def get_vnn_array(self, location, r):
        """ Stands for Von Neumann Neighborhood. 
            Simply returns a neighborhood based on the initial location and range r"""
        return_array = []
        for row_number in range((2 * r) - 1):
            if row_number >= r:
                num_in_row = (2 * row_number) - (4 * (row_number - r + 1) - 1)
            else:
                num_in_row = (2 * row_number) + 1
        
            for cell in range(num_in_row):
                    
                new_location = (location.x + (cell - math.floor(num_in_row / 2.0)), location.y + (row_number - (r - 1)))
                return_array.append(Vector2(*new_location))
                
        return return_array
