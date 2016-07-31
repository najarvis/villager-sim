from gametools import vector2
import Tile
import math

def get_tile(world, location):
    tile = get_tile_pos(world, location)
    try:
        return world.tile_array[int(tile.y)][int(tile.x)]
    except IndexError:
        return Tile.Tile(world, "Sand")

def get_tile_pos(world, location):
    return vector2.Vector2(int(location.x) >> 5, int(location.y) >> 5)

def get_entity(world,location, radius = 20):
    for i in world.entities.items():
        ent_location = i[1].world_location
        if ((ent_location.x - location.x)**2 + (ent_location.y - location.y)**2) < radius**2:
            return i
    # print "no ents"

def get_tile_array(world, start_pos, dimensions):
    dimensions = (int(dimensions[0]), int(dimensions[1]))

    start_tile = get_tile_pos(world,start_pos)

    array = [[None for i in xrange((dimensions[0] * 2) + 1)]
             for a in xrange((dimensions[1] * 2) + 1)]

    for i in xrange((dimensions[0] * 2) + 1):
        for a in xrange((dimensions[1] * 2) + 1):
            if start_tile.x + i < 0 or start_tile.y + a < 0:
                continue

            else:
                try:
                    array[a][i] = world.tile_array[int((start_tile.y + a) - 1)][int((start_tile.x + i) - 1)]
                except IndexError:
                    print a, i, start_tile
                    raise IndexError
    return array

def get_vnn_array(world, location, r):
    """ Stands for Von Neumann Neighborhood.
        Simply returns a neighborhood of locations based
        on the initial location and range r"""

    return_array = []

    """
    range: 3
    num rows: 5 (number of rows is equal to (2 * r) - 1
    0     *      1     left column is row_number  
    1   * * *    3     right column is num_in_row
    2 * * * * *  5
    3   * * *    3     middle is illustration of what is looks like
    4     *      1     num_in_row is just how many spots are looked at in the current row.
    """

    for row_number in range((2 * r) - 1):
        if row_number >= r:
            num_in_row = (2 * row_number) - (4 * (row_number - r + 1) - 1)
        else:
            num_in_row = (2 * row_number) + 1

        for cell in range(num_in_row):

            """
            the y_offset goes from -(r - 1) to +(r - 1) (not affected by the inner loop)

            the x_offset goes from -math.floor(num_in_row / 2.0) to +math.floor(num_in_row / 2.0) 

            0     0     1 |                  (0, -2)                  x, y offset pairs of a range 3 vnn array        
            1   0 1 2   3 |         (-1, -1) (0, -1) (1, -1)         
            2 0 1 2 3 4 5 | (-2, 0) (-1, 0 ) (0, 0 ) (1, 0 ) (2, 0)   left column is row_number
            3   0 1 2   3 |         (-1, 1 ) (0, 1 ) (1, 1 )          right column is num_in_row
            4     0     1 |                  (0, 2 )                  middle is cell number
            """

            x_offset = cell - math.floor(num_in_row / 2.0)
            y_offset = row_number - (r - 1)

            new_location = vector2.Vector2(location.x + x_offset, location.y + y_offset)
            return_array.append(new_location)

    return return_array
