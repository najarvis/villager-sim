__author__ = 'Nick Jarvis'

import math

def combine_arrays(arr1, arr2, weight1, weight2):
    to_return = [[0 for i in xrange(len(arr1))] for j in xrange(len(arr1[0]))]
    for y in xrange(len(arr1)):
        for x in xrange(len(arr1[0])):
            to_return[x][y] = arr1[x][y] * weight1 + arr2[x][y] * weight2

    return to_return

def clamp(val, low=0, high=255):
    return max(min(high, val), low)

def scale_array(array, scalar):
    to_return = array
    for y in xrange(len(array)):
        for x in xrange(len(array[0])):
            to_return[x][y] = array[x][y] * scalar

    return to_return

def pertubate(base_array, pert_array):
    to_return = [[0 for y in xrange(len(base_array))] for x in xrange(len(base_array[0]))]
    size = len(base_array) - 1

    magnitude = math.log(size + 1, 2) * ((size + 1) / 256)

    for y in xrange(len(base_array)):
        for x in xrange(len(base_array[0])):
            offset = int(((pert_array[x][y] - 128) / 128.0) * magnitude)
            to_return[x][y] = clamp(base_array[clamp(x + offset, high=size)][clamp(y + offset, high=size)], 0, 255)

    return to_return

