import random
import pygame
import VoronoiMapGen as vmg

detail = 8
TotalSize =  2**detail
surf1 = pygame.Surface((TotalSize,TotalSize))

class terrain:

    def __init__(self, detail):
        self.size = 2**detail + 1
        self.max = self.size -1
        self.map = [[0 for i in range(self.size)] for j in range(self.size)]

    def get(self,x,y):
        if x<0 or x > self.max or y < 0 or y > self.max: return -1
        return self.map[int(x)][int(y)]

    def set(self,x,y,val):
        self.map[int(x)][int(y)] = val

    def average(self,values):
        valid = [v for v in values if v!=-1 ]
        total = sum(valid)
        return total/len(valid)

    def square(self,x,y,size,offset):
        ave = self.average([
            self.get(x-size,y-size),
            self.get(x+size,y-size),
            self.get(x+size,y+size),
            self.get(x-size,y+size)])
        self.set(x,y,ave+offset)

    def diamond(self,x,y,size,offset):
        ave = self.average([
            self.get(x,y-size),
            self.get(x+size,y),
            self.get(x,y+size),
            self.get(x-size,y)])
        self.set(x,y,ave+offset)

    def divide(self, size, roughness):
        x,y,half = size/2.0,size/2.0,size/2.0
        scale = roughness * size
        if half<0.0078125:return

        y = half
        while y < self.max:
            x=half
            while x<self.max:
                self.square(x,y,half,random.uniform(0,1)*scale*2-scale)
                x+=size
            y+=size

        y = 0
        while y <= self.max:
            x=(y+half)%size
            while x <= self.max:
                self.diamond(x,y,half,random.uniform(0,1)*scale*2-scale)
                x+=size
            y+=half
                
        self.divide(size/2.0,roughness)  

    def generate(self,roughness):
        self.set(0,0,.5)
        self.set(self.max,0,.5)
        self.set(self.max,self.max,.5)
        self.set(0,self.max, .5)

        self.divide(1, roughness)

    def addArrayValues(self,arr1,arr2,fav = None):
        toReturn = [[0 for x in xrange(len(arr2))] for y in xrange(len(arr2))]
        for y in xrange(len(arr2)):
            for x in xrange(len(arr2)):
                if fav == 1:
                    toReturn[x][y] = ((arr1[x][y]*2+arr2[x][y]/2)/2)
                if fav == 2:
                    toReturn[x][y] = ((arr1[x][y]/2+arr2[x][y]*2)/2)
                if fav == None:
                    toReturn[x][y] = ((arr1[x][y]+arr2[x][y])/2)
        return toReturn
"""
seed = 18241982
random.seed(seed)
gener = vmg.mapGen()

random.seed(seed) 
vorMap = gener.whole_new(25, size = (TotalSize+1,TotalSize+1), c1=-1,c2=1)

random.seed(seed)
flatMap = gener.flat(25, size = (TotalSize+1, TotalSize+1))

gen = terrain(detail)
gen.generate(512/TotalSize)

gen.map = gener.negativeArray(gen.map)

newTotal = self.addArrayValues(vorMap, flatMap,1)
newTotal = self.addArrayValues(newTotal, gen.map)

MIN=MAX=fives=zeros=neg = 0

surf1.lock()
for y in xrange(TotalSize+1):
    for x in xrange(TotalSize+1):
        clr = newTotal[x][y]
        #print clr,
        
        if clr == 512:
            fives+=1
        elif clr == 0:
            zeros+=1
        if clr <  0:
            neg+=1
        if clr < 512:
            MIN = min(MIN, clr)
            MAX = max(MAX, clr)

        clr=int(clr)
        #print clr
        try:
            surf1.set_at((x,y), (clr,clr,clr))
        except TypeError:
            #print clr
            pass
surf1.unlock()

print MIN, MAX,fives,zeros,neg

pygame.image.save(surf1, 'test.png')
"""