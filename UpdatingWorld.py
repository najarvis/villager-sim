import pygame
from gametools import vector2, VoronoiMapGen
import Tile
import Clips
import Farmer
import Lumberjack

class World(object):
    """This class holds everything in the game. It also
    updates and renders it all each frame."""

    def __init__(self, tile_dimensions, screen_size):
        """Basic initialization.
        
        Args:
            tile_dimensions: The dimensions of the world in terms
                of tiles. default is 128x128 tiles.
                
            screen_size: The size of the window, this is used for scaling
                (mostly of the minimap).
                
        Returns:
            None
        """

        self.tile_size = 32
        self.w, self.h = self.world_size = tile_dimensions[0] * self.tile_size, \
                                            tile_dimensions[1] * self.tile_size
        self.world_position = vector2.Vector2(-self.w / 2, -self.h / 2)

        self.clock = pygame.time.Clock()

        # Entities
        self.entities = {}
        self.entity_id = 0

        self.new_world(tile_dimensions)
        self.clipper = Clips.Clips(self, screen_size)

    def new_world(self, array_size):
        """Creates a new world (including all of the entities)
        
        Args:
            array_size: The size of the tile array, same as tile_dimensions
                in __init__.
                
        Returns:
            None
        """

        map_width, map_height = array_size
        map_generator = VoronoiMapGen.mapGen()
        vor_map = map_generator.negative(map_generator.reallyCoolFull(array_size,
                                                                                num_p=23))
        self.minimap_img = pygame.Surface((map_width, map_height))
        self.tile_array = [[0 for tile_x in xrange(map_width)] for tile_y in xrange(map_height)]
        self.world_surface = pygame.Surface(self.world_size, pygame.HWSURFACE)
        
        for tile_x in xrange(map_width):

            for tile_y in xrange(map_height):

                color = vor_map[tile_x][tile_y]

                if color < 110:
                    # Water tile
                    new_tile = Tile.WaterTile(self, "AndrewWater")

                elif 120 > color >= 110:
                    # Sand / Beach tile
                    new_tile = Tile.BeachTile(self, "Sand")

                # TODO: Implement a humidity / temperature system
                elif 160 > color >= 120:
                    # Grass
                    new_tile = Tile.GrassTile(self, "MinecraftGrass")

                elif 170 > color >= 160:
                    # Tree
                    new_tile = Tile.TreePlantedTile(self, "GrassWithCenterTree")

                elif 190 > color >= 170:
                    # Grass (again)
                    new_tile = Tile.GrassTile(self, "MinecraftGrass")

                elif 220 > color >= 190:
                    # Rock
                    new_tile = Tile.SmoothStoneTile(self, "AndrewSmoothStone")

                else:
                    # Snow
                    new_tile = Tile.SnowTile(self, "MinecraftSnow")

                new_tile.location = vector2.Vector2(tile_x * self.tile_size, tile_y * self.tile_size)

                new_tile.rect.topleft = new_tile.location
                new_tile.color = color

                alph = 220 - color
                if 220 > color >= 190:
                    alph = 330 - color

                subtle_shadow = pygame.Surface((self.tile_size, self.tile_size))
                subtle_shadow.set_alpha(alph)

                self.world_surface.blit(new_tile.img, new_tile.location)
                self.world_surface.blit(subtle_shadow, new_tile.location)
                
                self.minimap_img.blit(
                        new_tile.img.subsurface(
                            (0, 0, 1, 1)), (tile_x, tile_y))


                self.minimap_img.blit(
                        subtle_shadow.subsurface(
                            (0, 0, 1, 1)), (tile_x, tile_y))

                self.tile_array[tile_x][tile_y] = new_tile

        self.populate()

    def populate(self):
        
        for lumberjack_num in xrange(5):
            lumberjack = Lumberjack.Lumberjack(self, pygame.Surface((32, 32)))
            lumberjack.location = vector2.Vector2(self.w/2, self.h/2)
            lumberjack.brain.set_state("Searching")
            self.add_entity(lumberjack)
            
        for farmer_num in xrange(5):
            farmer = Farmer.Farmer(self, pygame.Surface((32, 32)))
            farmer.location = vector2.Vector2(self.w/2, self.h/2)
            farmer.brain.set_state("Planting")
            self.add_entity(farmer)

    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def process(self, delta):
        for entity in self.entities.values():
            entity.process(delta)

    def render(self, surface):
        surface.blit(self.world_surface, self.world_position)

        for entity in self.entities.itervalues():
            entity.render(surface)

    def render_all(self, surface, delta, mouse_pos):
        self.clipper.render(surface, delta, mouse_pos)
        #self.render(surface)

