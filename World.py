import sys
import pygame
from gametools import vector2, VoronoiMapGen, MidpointDisplacement, PertTools
import math
import Tile
import Clips
import Farmer
import Lumberjack
import Angler
import Explorer
import Arborist

# TODO: Fog Of War - Make the world image covered in black, and the ai slowly reveals it.
#     the tiles should have a 'hidden' attribute. Would be cool because the person watching
#     the simulation wouldn't know what the final image looked like either.

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
        self.w, self.h = self.world_size = (tile_dimensions[0] * self.tile_size, tile_dimensions[1] * self.tile_size)
        self.world_position = vector2.Vector2(-self.w / 2, -self.h / 2)

        self.clock = pygame.time.Clock()

        # Unused variables
        self.wood = 0
        self.fish = 0

        # Entities
        self.entities = {}
        self.buildings = {}
        self.entity_id = 0
        self.building_id = 0

        self.new_world(tile_dimensions)
        self.clipper = Clips.Clips(self, screen_size)

        # TODO (wazzup771@gmail.com | Nick Wayne): Not sure if these belong here either
        self.info_bar = pygame.image.load("Images/Entities/info_bar.png").convert()
        self.info_bar.set_colorkey((255, 0, 255))
        self.f_high = (50, 200, 50)
        self.f_low = (255, 0, 0)
        self.w_high = (0, 0, 255)
        self.w_low = (76, 70, 50)
        self.e_high = (0, 255, 0)
        self.e_low = (50, 50, 0)

    def new_world(self, array_size):
        """Creates a new world (including all of the entities)

        Args:
            array_size: The size of the tile array, same as tile_dimensions
                in the constructor.

        Returns:
            None
        """

        map_width, map_height = array_size
        map_generator = VoronoiMapGen.mapGen()

        # midpoint_generator = MidpointDisplacement.MidpointDisplacement()
        # mid_map = PertTools.scale_array(midpoint_generator.normalize(midpoint_generator.NewMidDis(int(math.log(map_width, 2)))), 255)
        #vor_map = map_generator.whole_new_updated(size=array_size, ppr=2, c1=-1, c2=1, c3=0)

        #combined_map = PertTools.combine_arrays(vor_map, mid_map, 0.33, 0.66)

        # pert_map = PertTools.scale_array(midpoint_generator.normalize(midpoint_generator.NewMidDis(int(math.log(map_width, 2)))), 255)
        # vor_map = map_generator.radial_drop(PertTools.pertubate(combined_map, pert_map), 1.5, 0.0)
        # vor_map = map_generator.radial_drop(mid_map, 1.5, 0.0)


        vor_map = map_generator.radial_drop(map_generator.negative(map_generator.reallyCoolFull(array_size, num_p=23)), max_scalar=1.5, min_scalar=0.0)


        # All grass map for testing
        # vor_map = [[150 for x in xrange(128)] for y in xrange(128) ]

        # Method without radial drop
        # vor_map = map_generator.negative(map_generator.reallyCoolFull(array_size, num_p=23))

        self.minimap_img = pygame.Surface((map_width, map_height))
        self.tile_array = [[0 for tile_x in xrange(map_width)] for tile_y in xrange(map_height)]
        self.world_surface = pygame.Surface(self.world_size, pygame.HWSURFACE)
        
        if len(sys.argv) >= 4:
            do_hard_shadow = bool(int(sys.argv[3]))
        else:
            do_hard_shadow = False
        if do_hard_shadow:
            shadow_drop = 2.5 / (map_width / 128.0)
            shaded = False

        for tile_x in xrange(map_width):
            shadow_height = 0

            for tile_y in xrange(map_height):

                color = vor_map[tile_x][tile_y]

                if do_hard_shadow:
                    shaded = False
                    if color < shadow_height and not shadow_height < 110:
                        shaded = True
                        shadow_height -= shadow_drop

                    elif color >= 110 and color > shadow_height:
                        shadow_height = color
                        shadow_height -= shadow_drop

                    else:
                        shadow_height -= shadow_drop

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
                new_tile.darkness = alph
                
                subtle_shadow = pygame.Surface((self.tile_size, self.tile_size))
                subtle_shadow.set_alpha(alph)
                
                if do_hard_shadow:
                    hard_shadow = pygame.Surface((self.tile_size, self.tile_size))
                    hard_shadow.set_alpha(128)
                    if shaded:
                        new_tile.img.blit(hard_shadow, (0, 0))

                self.world_surface.blit(new_tile.img, new_tile.location)
                self.world_surface.blit(subtle_shadow, new_tile.location)

                self.minimap_img.blit(
                    new_tile.img.subsurface(
                        (0, 0, 1, 1)), (tile_x, tile_y))

                self.minimap_img.blit(
                    subtle_shadow.subsurface(
                        (0, 0, 1, 1)), (tile_x, tile_y))

                self.tile_array[tile_y][tile_x] = new_tile
        
        self.populate()

    def populate(self):
        """Populates the world with entities.

        Currently just does a hard-coded a specific number of 
        lumberjacks and farmers in the same position.

        Args:
            None

        Returns:
            None"""

        start = {"Lumberjack": {"count": 2,
                                "state": "Searching",
                                "class": Lumberjack.Lumberjack},

                 "Angler": {"count": 2,
                            "state": "Searching",
                            "class": Angler.Angler},

                 "Arborist": {"count": 1,
                              "state": "Planting",
                              "class": Arborist.Arborist},

                 "Farmer": {"count": 0,
                            "state": "Tilling",
                            "class": Farmer.Farmer},

                 "Explorer": {"count": 1,
                              "state": "Exploring",
                              "class": Explorer.Explorer}
                 }

        for key in start.keys():
            for count in xrange(start[key]["count"]):
                new_ent = start[key]["class"](self, key)
                new_ent.location = vector2.Vector2(self.w / 2, self.h / 2)
                new_ent.brain.set_state(start[key]["state"])
                self.add_entity(new_ent)

    def add_entity(self, entity):
        """Maps the input entity to the entity hash table (dictionary)
        using the entity_id variable, then incriments entity_id.

        Args:
            entity: A GameEntity that will be added to the world

        Returns:
            None
        """

        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def add_building(self, building):
        self.buildings[self.building_id] = building
        building.id = self.building_id
        self.building_id += 1

        for tile_x in xrange(building.image.get_width()):
            for tile_y in xrange(building.image.get_height()):
                self.tile_array[building.location.y + tile_y][building.location.x + tile_x] = Tile.BuildingTile(self, "MinecraftGrass")
        self.world_surface.blit(building.image, building.location * self.tile_size)

    def process(self, delta):
        """Runs through each entity and runs their process function.

        Args:
            delta: Time passed since the last frame (in seconds)

        Returns:
            None
        """

        for entity in self.entities.values():
            entity.process(delta)

    def render(self, surface):
        """Blits the world_surface and all entities onto surface.

        Args:
            surface: The surface on which to blit everything

        Returns:
            None
        """

        surface.blit(self.world_surface, self.world_position)

        for entity in self.entities.itervalues():
            entity.render(surface)
            if entity.active_info:
                self.render_info_bar(surface,entity)

    def render_all(self, surface):
        """Calls the clipper's render function, which also calls
        this class's render function. Used so the main file doesn't
        have to call the clipper.

        Args:
            surface: The Pygame.Surface on which to blit everything.

            delta: The time passed (in seconds) since the last frame.

            mouse_pos: tuple of length 2 containing the position of the mouse.

        Returns:
            None
        """
        self.clipper.render(surface)

    def check_minimap_update(self, mouse_pos):
        """This code moves the view to where the user is clicking in
        the minimap. Don't ask me how it works, I have no idea.

        Args:
            mouse_pos: Vector2 instance that contains the position of the mouse

        Returns:
            None
        """

        if (mouse_pos.x > self.clipper.minimap_rect.x and
            mouse_pos.y > self.clipper.minimap_rect.y):

            x_temp_1 = -self.clipper.a * (mouse_pos.x - self.clipper.minimap_rect.x)
            x_temp_2 = self.clipper.rect_view_w * self.clipper.a
            self.world_position.x = x_temp_1 + (x_temp_2 / 2)

            y_temp_1 = -self.clipper.b * (mouse_pos.y - self.clipper.minimap_rect.y)
            y_temp_2 = self.clipper.rect_view_h * self.clipper.b
            self.world_position.y = y_temp_1 + (y_temp_2 / 2)

    # TODO(wazzup771@gmail.com | Nick Wayne): This function doesn't belong in this class, perhaps the entity superclass.
    def render_info_bar(self, surface, entity):
        lst = [self.f_high, self.f_low, self.w_high, self.w_low, self.e_high, self.e_low]
        lst2 = [entity.food, entity.water, entity.energy]
        surface.blit(self.info_bar, (entity.world_location.x + 10, entity.world_location.y - 20))
        for i in xrange(3):
            t = lst2[i] / 100.
            r = self.lerp(lst[2 * i][0], lst[2 * i + 1][0], t)
            g = self.lerp(lst[2 * i][1], lst[2 * i + 1][1], t)
            b = self.lerp(lst[2 * i][2], lst[2 * i + 1][2], t)
            pygame.draw.rect(surface, (r, g, b),
                             pygame.Rect((entity.world_location.x + 20, entity.world_location.y - 14 + (i * 7)),
                                         (int(40 * t), 4)))

    def lerp(self, v1, v2, t):
        return (1 - t) * v2 + t * v1
