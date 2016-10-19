import random

class MidpointDisplacement(object):

    def NewMidDis(self, N):
        WIDTH = HEIGHT = (2 ** N)
        to_return = [[0 for x in xrange(WIDTH + 1)] for y in xrange(HEIGHT + 1)]

        to_return[0][0] = random.random()
        to_return[WIDTH][0] = random.random()
        to_return[WIDTH][HEIGHT] = random.random()
        to_return[0][HEIGHT] = random.random()

        for r in xrange(N):
            for y in xrange(2 ** r):
                for x in xrange(2 ** r):
                    self.diamond(to_return, r, x, y, N)
            
            # print r, "iterations done"
            # print "size was", ((2 ** N) / (2 ** r))
            # print "there were", 2 ** r, "iterations in each dimension"
            # print ""

        return to_return

    def rand_h(self, r):
        return (2 * (random.random() - 0.5)) / (2 ** (r + 1))

    def normalize(self, array):
        r_array = array
        
        min_val = r_array[0][0]
        max_val = r_array[0][0]

        for y in xrange(len(r_array)):
            for x in xrange(len(r_array[0])):
                min_val = min(r_array[x][y], min_val)
                max_val = max(r_array[x][y], max_val)

        for y in xrange(len(r_array)):
            for x in xrange(len(r_array[0])):
                r_array[x][y] -= min_val
                r_array[x][y] /= (max_val - min_val)

        return r_array

    def diamond(self, array, recursion_depth, iteration_x, iteration_y, N):
        size = ((2 ** N) / (2 ** recursion_depth))
        tl = array[size * iteration_x][size * iteration_y]
        tr = array[size * iteration_x + size][size * iteration_y]
        br = array[size * iteration_x + size][size * iteration_y + size]
        bl = array[size * iteration_x][size * iteration_y + size]

        array[size * iteration_x + size / 2][size * iteration_y + size / 2] = ((tl + tr + br + bl) / 4) + self.rand_h(recursion_depth + 1)

        # Square step

        mid = array[size * iteration_x + size / 2][size * iteration_y + size / 2]

        # top mid
        array[size * iteration_x + size / 2][size * iteration_y] = (tl + tr + mid) / 3 + self.rand_h(recursion_depth)

        # right mid
        array[size * iteration_x + size][size * iteration_y + size / 2] = (tr + br + mid) / 3 + self.rand_h(recursion_depth)

        # bottom mid
        array[size * iteration_x + size / 2][size * iteration_y + size] = (bl + br + mid) / 3 + self.rand_h(recursion_depth)

        # left mid
        array[size * iteration_x][size * iteration_y + size / 2] = (tl + bl + mid) / 3 + self.rand_h(recursion_depth)

    def square(self, array, recursion_depth, iteration, N):
        pass

