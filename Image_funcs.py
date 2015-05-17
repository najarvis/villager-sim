import pygame

class image_funcs():
    
    def __init__(self,w,h):
        self.w = w
        self.h = h
    def get_list(self,pic):      #Takes and image and returns a list of all the 16x16 cells inside
        width, height = pic.get_size()
        cells = [[0 for i in xrange(width/self.w)] for i in xrange(height/self.h)]
        for i in xrange(width/self.w):
            for a in xrange(height/self.h):
                cells[i][a] = pic.subsurface((i*self.w, a*self.h, self.w, self.h))
    
        return cells
    
    def get_cell(self,cells, row, collumn, pic):     #Returns just 1 cell
        return cells[row][collumn]
    
    def get_image(self,cells, width, height, xpos, ypos, pic):       #Returns 1 image depending on it's dimensions and position
        quick_image = pygame.Surface((width*self.w, height*self.h))
        for i in range(width):
            for a in range(height):
                quick_image.blit(self.get_cell(cells, i+xpos, a+ypos, pic), (i*self.w, a*self.h))
        quick_image.set_colorkey((255,0,255))
        return quick_image
    
    def get_images(self,cells, width, width2, height, xpos, ypos, pic):      #Returns a list of images based on how many images
        lst = []                                                        #and then the dimensions and starting position
        for i in range(width):
            lst.append(self.get_image(cells, width2, height, xpos, ypos, pic))
            xpos+=width2
                        
        return lst