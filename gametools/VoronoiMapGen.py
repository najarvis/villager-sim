import pygame
from random import randint

class point:

    def __init__(self, pos, color=False):
        #Basic point, this will be used for the "feature points"
        #these will hold their position, as well as a seperate x and y
        #variable for easy use. Also a distance variable will be assigned
        #for when calculating the voronoi diagram

        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.distance = 0
        self.color = None
        #if color: self.color = randint(0,255)

    def get_distance(self, p2):
        #Basic distance formula. I don't square root everything
        #in order to speed up the process (AKA Manhattan Distance)
        try:
            distance = float((p2.x - self.x) ** 2) + ((p2.y - self.y) ** 2)
        except DivideByZeroError:
            distance = 0
        self.distance = distance
        return distance

    def addColor(self):
        if randint(0, 1):
            self.color = randint(1, 10) * 10
        else:
            self.color = 0
        
class mapGen:

    def lerp(self, c1, c2, a):
        return c1 + (c2 - c1) * a

    def whole_new(self, num_R, size=(256, 256), c1=0, c2=0, c3=0):
        #Creates 1 image of the voronoi diagram. I only listed the first 3
        #coefficients because that's all I will really need, but feel free
        #to add more
        w, h = size  #Very easy to use w and h instead of size[0] and size[1]

        toReturn = [[0 for _ in xrange(size[0])] for _ in xrange(size[1])]

        point_list = [point((randint(0, w), randint(0, h))) for i in range(num_R)]
        #Creates the random "interest" points,

        for y in xrange(h):     #Do row-by-row instead of
            for x in xrange(w): #collumn-by-collumn
                currentPoint = point((x, y))
                new_pointlist = sorted(point_list, key=lambda point: point.get_distance(currentPoint))  #sort the points in a new list by their distance from the current point

                currentPoint.brightness = int(c1*new_pointlist[0].distance+c2*new_pointlist[1].distance+c3*new_pointlist[2].distance)/(num_R*(size[0]/((512.0/size[0])*256)))
                #this uses the coefficients and the new list to find the brightness of the wanted pixel
                #the math at the end is something I came to after about a half hour of fiddling around
                #with values. This will keep the value at a constant and good level, and not flatten anything.

                #maxB = max(maxB, currentPoint.brightness)
                #minB = min(minB, currentPoint.brightness)

                clr = abs(currentPoint.brightness)  #a lot of the times the values are negative!
                clr = min(255, clr)                 #Make sure we don't for some reason overflow
                toReturn[x][y] = clr

        return toReturn

    def whole_new_updated(self, size=(256, 256), rpd=4, ppr=3, c1=0, c2=0, c3=0):
        """Creates and returns an array of given size containing values calculated by a voronoi diagram.

        The updated version is more controlled, with regions per dimension (rpd) and points per region (ppr). The array
        is split up into rpd * rpd  regions, while each region contains ppr interest points. These points are used along
        with coefficients c1, c2, and c3 to customize the array.

        Arguments:
            size: 
                The size of the return array. This should probably just be an 
                integer to keep the array square in the future.
            rpd:
                This is the amount of regions on each side of the diagram. 
                A value of 4 would result in 16 regions, 4 on each side.
            ppr:
                The amount of interest points in a region. Randomly distributed
            c1, c2, c3:
                Coeffiecients that determine how the final outcome will be.
                A c1 of 1 and the rest 0's will result in 'bubbles', while
                a c1 of 1 and a c2 of -1 will result in straight lines that
                divide the diagram into regions

        Returns a 2-Dimensional array with size equal to the argument size."""

        w, h = size
        to_return = [[0 for i in xrange(w)] for j in xrange(h)]
        num_regions = rpd * rpd
        region_size = size[0] / rpd
        num_points = num_regions * ppr

        interest_points = []

        for region_y in xrange(rpd):
            for region_x in xrange(rpd):
                
                for p in xrange(ppr):
                    rx = randint(region_x * region_size, (region_x + 1) * region_size)
                    ry = randint(region_y * region_size, (region_y + 1) * region_size)
                    interest_points.append(point((rx, ry)))

        max_val = 0
        min_val = 0

        for y in xrange(h):
            for x in xrange(w):
                current_point = point((x, y))

                #sort the points in a new list by their distance from the current point
                new_pointlist = sorted(interest_points, key=lambda point: point.get_distance(current_point)) 

                current_point.brightness = c1 * new_pointlist[0].distance + \
                                           c2 * new_pointlist[1].distance + \
                                           c3 * new_pointlist[2].distance

                if y == x == 0:
                    max_val = current_point.brightness
                    min_val = current_point.brightness

                elif current_point.brightness > max_val:
                    max_val = current_point.brightness

                elif current_point.brightness < min_val:
                    min_val = current_point.brightness

                to_return[x][y] = current_point.brightness

        max_val -= min_val
        print max_val, min_val
        for y in xrange(h):
            for x in xrange(w):
                to_return[x][y] -= min_val
                
                to_return[x][y] = int((to_return[x][y] / max_val) * 255)

        return to_return

    def flat(self, num_R, size=(256, 256)):
        #Creates 1 image of the voronoi diagram. I only listed the first 3
        #coefficients because that's all I will really need, but feel free
        #to add more
        w,h = size  #Very easy to use w and h instead of size[0] and size[1]
        
        toReturn = [[0 for i in xrange(size[0])] for j in xrange(size[1])]

        point_list = [point((randint(0,w), randint(0,h)),True) for i in range(num_R)]        #Creates the random "interest" points,
        for POINT in point_list:
            POINT.addColor()

        for y in xrange(h):     #Do row-by-row instead of
            for x in xrange(w): #collumn-by-collumn
                currentPoint = point((x, y))
                new_pointlist = sorted(point_list, key=lambda point: point.get_distance(currentPoint))  #sort the points in a new list by their distance from the current point

                currentPoint.brightness = new_pointlist[0].color
                clr = abs(currentPoint.brightness)
                clr = min(255, clr)

                toReturn[x][y] = clr

        return toReturn
    
    
    def lerp_two_images(self, pic1, pic2, a):
        w, h = len(pic1), len(pic1[0]) #pic1.get_size()
        surface = pygame.Surface((w, h))

        for y in xrange(h):
            for x in xrange(w):
                clr1 = pic1.get_at((x, y))
                clr2 = pic2.get_at((x, y))
                clrR = (clr1[0]*(1-a)+clr2[0]*a)
                clrG = (clr1[1]*(1-a)+clr2[1]*a)
                clrB = (clr1[2]*(1-a)+clr2[2]*a)
                try:
                    surface.set_at((x, y), (clrR, clrG, clrB))
                except TypeError, e:
                    print clr
                    raise e

        return surface

    def combine_images(self, *pics):
        #Takes a list of images and combines them (grayscale).
        #All picture sizes must be of equal or less length
        #but it is reccomended to have the exact same size for each

        num_pics = len(pics)
        w, h= len(pics[0]), len(pics[0][0])#Again, this is very nice for keeping things quick
        
        total_map = [[0 for i in xrange(h)] for i in xrange(w)] #Create a 2D array to hold all the values
        for PIC in pics:    #Loops through each of the given pictures
            for y in xrange(h):         #Row-by-Row
                for x in xrange(w):
                    try:
                        total_map[x][y] += PIC[x][y]   #Adds the current value at the map to the corresponding cell on the array
                    except IndexError:
                        print x,y
                        print len(total_map), len(total_map[0])
                        raise IndexError

        to_return = [[0 for i in range(h)] for j in range(w)]
        for y in xrange(h):     #Loop through again, row-by-row
            for x in xrange(w):
                total_map[x][y]/=num_pics   #average out each cell
                clr = total_map[x][y]       #use clr so we don't have to use 'total_map[x][y]' 3 times
                to_return[x][y] = clr

        return to_return

    def threshold(self, array, lower=100, upper=128):
        #returns a thresholded surface of the image provided
        #NOTE: array must have equal size dimensions

        w = h = len(array)
        toReturn = [[0 for x in xrange(w)] for y in xrange(h)]
        for y in xrange(h):     #Row-by-Row
            for x in xrange(w):
                if lower <= array[x][y] <= upper: #Checks to see if the value is in the threshold
                    toReturn[x][y] = 255    #Sets the pixel at that position to white if it is

        return toReturn

    def negative(self, ARRAY):
        w = h = len(ARRAY)
        toReturn = [[0 for x in xrange(w)]for y in xrange(h)]
        for y in xrange(h):
            for x in xrange(w):
                toReturn[x][y] = 255-ARRAY[x][y]

        return toReturn


    def reallyCoolFull(self, total_size=(256,256), num_p=25):
        #Uses 4 (or as many as you make, but I have found this to look cool)
        #calls to "whole_new()" and averages them out to create one cool image
        #that can be used in map generation! :D

        pic1 = self.whole_new(num_p, total_size, c1=-1)
        pic2 = self.whole_new(num_p, total_size, c2=1)
        pic3 = self.whole_new(num_p, total_size, c3=1)
        pic4 = self.whole_new(num_p, total_size, c1=-1, c2=1)

        return self.combine_images(pic1, pic2, pic3, pic4)

    def full_updated(self, size=(256, 256), rpd=4, ppr=3):
        pic1 = self.whole_new_updated(size, rpd, ppr, c1=-1)
        pic2 = self.whole_new_updated(size, rpd, ppr, c2=1)
        pic3 = self.whole_new_updated(size, rpd, ppr, c3=1)
        pic4 = self.whole_new_updated(size, rpd, ppr, c1=-1, c2=1)
        #pic5 = self.whole_new_updated(size, 4, 2, c1=1)
        #pic4 = self.whole_new_updated(size, 4, 2, c2=1)

        #return self.combine_images(pic5, pic4)
        return self.combine_images(pic1, pic2, pic3, pic4)
