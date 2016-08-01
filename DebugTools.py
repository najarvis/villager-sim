import TileFuncs

def print_surrounding_tiles(world, print_type="Name"):
    tile_range = 2
    location_array = TileFuncs.get_vnn_array(world, world.entities[0].location, tile_range)
    
    if print_type=="Name":
        tile_list = tile_array_from_location(world, location_array)
    else:
        tile_list = location_array
    # print "Length of tile_list: %d"%len(tile_list)

    print tile_list[0]
    print tile_list[1], tile_list[2], tile_list[3]
    print tile_list[4]
    print ""

def tile_array_from_location(world, array):
    return_array = []
    for i in array:
        return_array.append(TileFuncs.get_tile(world, i).name)

    return return_array

def print_location_tile(world, location):
    print TileFuncs.get_tile(world, location).__class__.__name__
