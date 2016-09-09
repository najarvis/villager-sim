import pygame

from gametools.vector2 import Vector2


class Tile(object):
    def __init__(self, world, tile_name="NULL"):
        self.world = world
        self.name = tile_name
        self.img = pygame.image.load("Images/Tiles/"+tile_name+".png").convert()
        self.location = Vector2(0, 0)
        self.walkable = False
        self.fishable = False
        self.plantable = False
        self.buildable = False
        self.buildable_w = False
        self.darkness = 0

        self.id = 0
        self.rect = pygame.Rect((0, 0), self.img.get_size())

    def render(self, screen):
        screen.blit(self.img, self.location)


class GrassTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = True
        self.buildable = True
        self.plantable = True

class WaterTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.buildable_w = True
        self.fishable = True

class DeepWaterTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.buildable_w = True

class SmoothStoneTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = True
        self.buildable = True

class CobblestoneTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = True
        self.buildable = True

class DirtTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = True
        self.buildable = True

class BeachTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = True
        self.buildable = True

class Baby_Tree(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = True

class TreePlantedTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = True
        self.Taken = False

class SnowTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)


class BuildingTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = True
