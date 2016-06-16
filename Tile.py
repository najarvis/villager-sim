import pygame

from gametools.vector2 import Vector2


class Tile(object):
    def __init__(self, world, tile_name="NULL"):
        self.world = world
        self.name = tile_name
        self.img = pygame.image.load("Images/Tiles/"+tile_name+".png").convert()
        self.location = Vector2(0, 0)
        self.walkable = 0
        self.plantable = 0
        self.buildable = 0
        self.buildable_w = 0

        self.id = 0
        self.rect = pygame.Rect((0, 0), self.img.get_size())

    def render(self, screen):
        screen.blit(self.img, self.location)


class GrassTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = 1
        self.buildable = 1
        self.plantable = 1

class WaterTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.buildable_w = 1

class DeepWaterTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.buildable_w = 1

class SmoothStoneTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = 1
        self.buildable = 1

class CobblestoneTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = 1
        self.buildable = 1

class DirtTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = 1
        self.buildable = 1

class BeachTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = 1
        self.buildable = 1

class Baby_Tree(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = 1

class TreePlantedTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)
        self.walkable = 1
        self.Taken = 0

class SnowTile(Tile):
    def __init__(self, world, tile_name):
        Tile.__init__(self, world, tile_name)

