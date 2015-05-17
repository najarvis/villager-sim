import pygame
from pygame.locals import *
from random import randint

class point:
    
    def __init__(self, pos):
        #Basic point, this will be used for the "feature points"
        #these will hold their position, as well as a seperate x and y
        #variable for easy use. Also a distance variable will be assigned
        #for when calculating the voronoi diagram

        self.pos = pos
        self.x=pos[0]
        self.y=pos[1]
        self.distance = 0

    def get_distance(self, p2):
        #Basic distance formula. I don't square root everything
        #in order to speed up the process
        try:
            distance = float((p2.x-self.x)**2)+((p2.y-self.y)**2)
        except DivideByZeroError:
            distance = 0
        self.distance = distance
        return distance

    def get_taxicab_dist(self, p2):
        distance = (abs(p2.x-self.x)+abs(p2.y-self.y))**2
        self.distance = distance
        return distance
        
class mapGen:

    def lerp(self,c1,c2,a):
        return c1+(c2-c1)*a

    def whole_new(self, num_R, size=(256,256), c1=0, c2=0,c3=0,DrawSurface=None, name="",num=1):
        distances = open("Distances.txt", "w")
        #Creates 1 image of the voronoi diagram. I only listed the first 3
        #coefficients because that's all I will really need, but feel free
        #to add more
        surface = pygame.Surface(size)
        w,h = size  #Very easy to use w and h instead of size[0] and size[1]
        if DrawSurface!=None:
            DrawSurfaceWidth = DrawSurface.get_width() 
        
        point_list = [point((randint(0,w), randint(0,h))) for i in range(num_R)]        #Creates the random "interest" points,

        #old_caption = pygame.display.get_caption()
        pygame.display.set_caption("CALCULATING "+name)
        #Let the player know if the program is still calculating

        #maxB=0
        #minB=0

        surface.lock()      #Lock because we are setting individual points
        for y in xrange(h):     #Do row-by-row instead of
            for x in xrange(w): #collumn-by-collumn
                currentPoint = point((x,y))
                new_pointlist = sorted(point_list, key=lambda point: point.get_taxicab_dist(currentPoint))  #sort the points in a new list by their distance from the current point

                currentPoint.brightness = int(c1*new_pointlist[0].distance+c2*new_pointlist[1].distance+c3*new_pointlist[2].distance)/(num_R*(size[0]/((512.0/size[0])*256)))
                distances.write(str(currentPoint.brightness)+"\n")
                #this uses the coefficients and the new list to find the brightness of the wanted pixel
                #the math at the end is something I came to after about a half hour of fiddling around
                #with values. This will keep the value at a constant and good level, and not flatten anything.

                #maxB = max(maxB, currentPoint.brightness)
                #minB = min(minB, currentPoint.brightness)

                clr = abs(currentPoint.brightness)  #a lot of the times the values are negative!
                clr = min(255, clr)                 #Make sure we don't for some reason overflow
                surface.set_at((x,y), (clr, clr, clr))  #set the point
            if DrawSurface!=None:
                barWidth=((y*w)/float(h*w))*DrawSurfaceWidth
                pygame.draw.rect(DrawSurface, (self.lerp(255,0,.2*num),self.lerp(0,255,.2*num),0), (0,50*num,barWidth,20))
                pygame.display.update()
        surface.unlock()    #unlock because the loop is done
        if DrawSurface!=None:
            #DrawSurface.fill((0,0,0))
            pass

        pygame.display.set_caption("DONE")  #tell the user that the program has finished calculating

        return surface

    def lerp_two_images(self, pic1, pic2, a):
        w,h= pic1.get_size()
        surface = pygame.Surface((w,h))

        for y in xrange(h):
            for x in xrange(w):
                clr1 = pic1.get_at((x,y))
                clr2 = pic2.get_at((x,y))
                clrR = (clr1[0]*(1-a)+clr2[0]*a)
                clrG = (clr1[1]*(1-a)+clr2[1]*a)
                clrB = (clr1[2]*(1-a)+clr2[2]*a)
                try:
                    surface.set_at((x,y), (clrR, clrG, clrB))
                except TypeError, e:
                    print clr
                    raise e

        return surface

    def combine_images(self, *pics):
        #Takes a list of images and combines them (grayscale).
        #All picture sizes must be of equal or less length
        #but it is reccomended to have the exact same size for each

        num_pics = len(pics)
        w,h = pics[0].get_size() #Again, this is very nice for keeping things quick
        surface = pygame.Surface((w,h)) #Create the surface we will return 

        total_map = [[0 for i in xrange(w)] for i in xrange(h)] #Create a 2D array to hold all the values
        for PIC in pics:    #Loops through each of the given pictures
            for y in xrange(h):         #Row-by-Row
                for x in xrange(w):
                    total_map[x][y]+=PIC.get_at((x,y))[0]   #Adds the current value at the map to the corresponding cell on the array

        surface.lock()
        for y in xrange(h):     #Loop through again, row-by-row
            for x in xrange(w):
                total_map[x][y]/=num_pics   #average out each cell
                clr = total_map[x][y]       #use clr so we don't have to use 'total_map[x][y]' 3 times
                surface.set_at((x,y), (clr, clr, clr))  #set the colors
        surface.unlock()

        return surface

    def threshold(self, surface, lower=100, upper=128):
        #returns a thresholded surface of the image provided

        w,h = surface.get_size()
        new_surface = pygame.Surface((w,h))     #Create a surface with an identical size as the provided image
        new_surface.fill((0,0,0))   #fill with black, we will be setting the white values
        for y in xrange(h):     #Row-by-Row
            for x in xrange(w):
                if lower <= surface.get_at((x,y))[0] <= upper: #Checks to see if the value is in the threshold
                    new_surface.set_at((x,y), (255,255,255))    #Sets the pixel at that position to white if it is

        return new_surface

    def negative(self, surface):
        #Just returns the negative of an image (grayscale only)
        #this is usefull because the function favors darker colors
        #in the middle of the image
        
        w,h = surface.get_size()
        new_surface = pygame.Surface((w,h))
        for y in xrange(h):
            for x in xrange(w):
                clr = 255-surface.get_at((x,y))[0]
                new_surface.set_at((x,y), (clr,clr,clr))

        return new_surface


    def reallyCoolFull(self, total_size=(256,256), name="", num_p=25,  ds = None):
        #Uses 4 (or as many as you make, but I have found this to look cool)
        #calls to "whole_new()" and averages them out to create one cool image
        #that can be used in map generation! :D

        #WARNING: THIS CAN TAKE A VERY LONG TIME
        #32x32: 0.4s, 64x64: 0.8s, 128x128:2.5s 
        #256x256: 9.8s, 512x512: 37.1s!

        pic1 = self.whole_new(num_p, total_size, c1=-1, name=name, DrawSurface=ds, num=1)
        pic2 = self.whole_new(num_p, total_size, c2=1, name=name+".", DrawSurface=ds, num=2)
        pic3 = self.whole_new(num_p, total_size, c3=1, name=name+"..", DrawSurface=ds, num=3)
        pic4 = self.whole_new(num_p, total_size, c1=-1, c2=1, name=name+"...", DrawSurface=ds, num=4)

        return self.combine_images(pic1,pic2,pic3,pic4)

mapGener = mapGen()

pygame.image.save(mapGener.negative(mapGener.reallyCoolFull()), "TaxiCab.png")