def get_tile(self, location):
    tile = self.get_tile_pos(location)
    try:
        return self.TileArray[int(tile.y)][int(tile.x)]
    except IndexError:
        return Tile.NullTile(self, self.sand_img)

def get_tile_pos(self, location):
    return Vector2(int(location.x) >> 5, int(location.y) >> 5)

def get_tile_array(self, start_pos, dimensions):
    dimensions = (int(dimensions[0]), int(dimensions[1]))

    start_tile = self.get_tile_pos(start_pos)

    array = [[None for i in xrange((dimensions[0] * 2) + 1)]
             for a in xrange((dimensions[1] * 2) + 1)]

    for i in xrange((dimensions[0] * 2) + 1):
        for a in xrange((dimensions[1] * 2) + 1):
            if start_tile.x + i < 0 or start_tile.y + a < 0:
                continue

            else:
                try:
                    array[a][i] = self.TileArray[int((start_tile.y + a) - 1)][int((start_tile.x + i) - 1)]
                except IndexError:
                    print a, i, start_tile
                    raise IndexError
    return array

def get_vnn_array(self, location, r):
    """ Stands for Von Neumann Neighborhood.
        Simply returns a neighborhood based
        on the initial location and range r"""
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
