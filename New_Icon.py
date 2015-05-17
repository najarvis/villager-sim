import pygame
pygame.init()

screen = pygame.display.set_mode((10,10))

red_color = (200,50,50)
yellow_color = (128,128,0)

class new_icon_maker:
    
    def __init__(self):
        pass
    
    def get_icon(self, big, tile, size, name):
        new_surface = pygame.Surface(big.get_size())
        x, y = big.get_size()[0]/int(size), big.get_size()[1]/int(size)
        for i in range(x):
            for a in range(y):
                new_surface.blit(tile, (i*size, a*size))
                
        new_surface.blit(big, (0,0))
        pygame.image.save(new_surface, "Images/Buildings/%s_Icon.png"%name)
        return new_surface
    
    def color(self, big, tile, size, name, color):
        first_img = self.get_icon(big, tile, size, name)
        
        test_surface = pygame.Surface((64,64))
        test_surface.set_alpha(128)
        
        if color == "RED":
            test_surface.fill(red_color)
        elif color == "SELECTED":
            test_surface.fill(yellow_color)
            
        final_icon = pygame.Surface((64,64))
        final_icon.blit(first_img,(0,0))
        final_icon.blit(test_surface, (0,0))
        
        pygame.image.save(final_icon, "Images/Buildings/%s_%s_Icon.png"%(color,name))       
     
maker = new_icon_maker()

big_img = pygame.image.load("Images/Buildings/Dock.png").convert()
big_img.set_colorkey((255,0,255))

tile_img = pygame.image.load("Images/Tiles/AndrewWater.png").convert()
#icon1 = maker.color(big_img, tile_img, 32, "Dock", "SELECTED")
icon1 = maker.color(big_img, tile_img, 32, "Dock", "SELECTED")