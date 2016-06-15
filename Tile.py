import pygame

from vector2 import Vector2


class Tile:
    def __init__(self, world, img):
        self.world = world
        self.name = "BASETILE"
        self.img = img
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
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.walkable = 1
        self.buildable = 1
        self.name = "GrassTile"


class WaterTile(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.buildable_w = 1
        self.name = "WaterTile"


class DeepWaterTile(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.name = "DeepWaterTile"
        self.buildable_w = 1


class SmoothStoneTile(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.walkable = 1
        self.buildable = 1
        self.name = "SmoothStoneTile"


class CobblestoneTile(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.walkable = 1
        self.buildable = 1
        self.name = "CobblestoneTile"


class DirtTile(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.walkable = 1
        self.buildable = 1
        self.name = "DirtTile"


class BeachTile(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.walkable = 1
        self.buildable = 1
        self.name = "SandTile"


class TreePlantedTile(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.name = "TreePlantedTile"
        self.walkable = 1
        self.buildable = 1
        self.plantable = 1


class Baby_Tree(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.name = "Baby_Tree"
        self.walkable = 1


class TreePlantedTile_w(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.name = "TreePlantedTile_W"
        self.walkable = 1
        self.Taken = 0


class SnowTile(Tile):
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.name = "SnowTile"
        
        
class NullTile(Tile):
    
    def __init__(self, world, img):
        Tile.__init__(self, world, img)
        self.name = "NULL"