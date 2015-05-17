import pygame
import glob

dialol = pygame.image.load("Images/Dial/dial_outline2.png")
dial = pygame.image.load("Images/Dial/dial.png")
dialol.set_colorkey((255,0,255))
dial.set_colorkey((255,0,255))

buildings = ["House","LumberYard","Dock", "Manor"]


class Clips:
    """
    ______________________
    |_ |_ |              |
    |_ |_ |              |
    |_ |_ |              |
    |Desc.|              |
    |     |              |
    |_____|              |
    |f:   |         _____|
    |w:   |        |MINI-|
    |p:   |        |MAP  |
    ----------------------
    """
    
    def __init__(self, world, Osizes):
        self.size = Osizes
        self.world = world
        #ratio = self.size[0]/float(self.size[1])
        #ratio = (self.size[0]/4, self.size[1]/4)
        self.minimap_size = int(self.size[0]/4) , int(self.size[1]/4)
        self.minimap = pygame.transform.scale(self.world.minimap_img, self.minimap_size)
        
        self.a = self.world.w/float(self.minimap_size[0])
        self.b = self.world.h/float(self.minimap_size[1])
        
        
        self.rect_view_w = (self.size[0]/self.a)-((self.size[0]/self.a)/5)
        self.rect_view_h = self.size[1]/self.b
        
        self.minimap_rect = pygame.Rect(self.size[0]-self.minimap_size[0],self.size[1]-self.minimap_size[1], self.minimap_size[0], self.minimap_size[1])
        print self.minimap_rect.w,self.minimap_rect.h
        self.side = sidebar(world, self.size)
       
    def render(self, surface, tp, mouse_pos):

        self.rect_view_pos = ((-1*self.world.background_pos.x/self.a)+self.size[0]-self.minimap_size[0]+((self.size[0]/5)/self.a),
                              (-1*self.world.background_pos.y/self.b)+self.size[1]-self.minimap_size[1])
        
        self.rect_view = (self.rect_view_pos, (self.rect_view_w, self.rect_view_h))
        
#         surface.set_clip((0,0,self.size[0],20))
#         surface.blit(self.world.wood_text, (40,2))
#         surface.blit(self.world.food_text, (200,2))
#         surface.blit(self.world.pop_text, (360,2))
#         surface.blit(self.world.frame_text, (520,2))

        surface.set_clip((0,0,self.size[0]/5.0,self.size[1]))
        self.side.render(surface, mouse_pos, tp)
        
        surface.set_clip((self.size[0]/5.0,0,self.size[0], self.size[1]))
        self.world.render(surface)
        self.update_dial(surface, tp)
        
        surface.set_clip(self.minimap_rect)
        pygame.draw.rect(surface, (255,255,255), (0,self.size[1]-300, self.size[0], 300))
        surface.blit(self.minimap, (self.size[0]-self.minimap_size[0], self.size[1]-self.minimap_size[1]))
        pygame.draw.rect(surface, (255,255,255), self.rect_view, 1)
        
        pygame.draw.rect(surface, (0,0,0), (self.size[0]-self.minimap_size[0],self.size[1]-self.minimap_size[1], self.minimap_size[0], self.minimap_size[1]),2)
        surface.set_clip(None)
        
    def update_dial(self, surface, tp):        #Dial goes below here
        box = (self.size[0]-55, self.size[1]/50-40)
        boxtest = pygame.Rect((box[0]-20, box[1] + 80), (50, 50))
        oldCenter = boxtest.center
        rotateddial =  pygame.transform.rotate(dial, self.world.clock_degree)
        rotRect = rotateddial.get_rect()
        rotRect.center = oldCenter
        self.world.clock_degree += tp
        if self.world.clock_degree>=360.0: self.world.clock_degree = 0.0
        
        surface.blit(rotateddial, rotRect)
        surface.blit(dialol,(box[0]-44,box[1]+55))
        
    def convert_all(self):
        for i in range(2):
            pass
    
class sidebar():
    
    def __init__(self, world, size):
        self.world = world
        
        self.wood = self.world.wood
        self.MAXwood = self.world.MAXwood
        
        self.food = self.world.food
        self.MAXfood = self.world.MAXfood
        
        self.population = self.world.population
        self.MAXpop = self.world.MAXpopulation
        
        self.Lgray = (200,200,200)
        self.Dgray = (160,160,160)
        self.outline = (0,0,0)
        self.text_color = (255,255,255)
        
        self.size = size
        
        self.h = self.size[1]
        self.w = self.size[0]/5.0
        
        self.len_tiles_x = 4
        self.len_tiles_y = 3
        
        self.tile_width = (self.w/self.len_tiles_x)
        self.tile_height = ((self.h/4)/self.len_tiles_y)
        
        self.tile_size = int(self.tile_width),int(self.tile_height)
        
        self.top_rect = pygame.Rect((0,0,self.w,self.h/4))
        self.mid_rect = pygame.Rect((0,self.h/4,self.w,self.h/2))
        self.bottom_rect = pygame.Rect((0,self.h*0.75,self.w,self.h/4))
        
        self.top_render = pygame.Surface((self.top_rect.w, self.top_rect.h))
        self.top_render.fill(self.Dgray)
        #self.top_render.blit(pygame.transform.scale(test_image, self.tile_size),(0,0))
        self.tiles = []
        num = 0
        for x in range(self.len_tiles_x):
            self.tiles.append([])
            for y in range(self.len_tiles_y):
                try:
                    self.tiles[x].append(icon_tile(self.tile_size, buildings[num], (x*self.tile_width,y*self.tile_height)))
                    self.tiles[x][y].render(self.top_render)
                    pygame.draw.rect(self.top_render, self.outline, (x*self.tile_width,y*self.tile_height,self.tile_width,self.tile_height),2)
                except Exception:
                    self.tiles[x].append(None)
                    
                    #pygame.draw.rect(self.top_render, self.Dgray, (x*self.tile_width,y*self.tile_height,self.tile_width,self.tile_height))
                
                num+=1
                

    def render(self, surface, mouse_pos, tp):
        pygame.draw.rect(surface, self.Dgray, (0,0,self.w,self.h))
        
        pygame.draw.rect(surface, self.outline, self.top_rect,4)
        
        surface.blit(self.top_render, self.top_rect)
        pygame.draw.rect(surface, self.outline, self.mid_rect,4)
        
        try:
            height = "HEIGHT: " + str(self.world.get_tile(mouse_pos-self.world.background_pos).color)
            name = "NAME: " + str(self.world.get_tile(mouse_pos-self.world.background_pos).name)
        except IndexError:
            height = "NULL"
            name = "NULL"
        
        fps = "FPS: %.2f"%self.world.clock.get_fps()
        food = "FOOD: %d"%self.world.food
        wood = "WOOD: %d"%self.world.wood
        population = "POPULATION: %d/%d"%(self.world.population,self.world.MAXpopulation)
        
        pos_str = "%.0f, %.0f"%(mouse_pos.x, mouse_pos.y)
            
        rendered_height = self.world.font.render(height, True, (255,255,255))
        rendered_name = self.world.font.render(name, True, (255,255,255))
        rendered_fps = self.world.font.render(fps, True, (255,255,255))
        rendered_food = self.world.font.render(food, True, (255,255,255))
        rendered_wood = self.world.font.render(wood, True, (255,255,255))
        rendered_population = self.world.font.render(population, True, (255,255,255))
        rendered_pos_str = self.world.font.render(pos_str, True, (255,255,255))
        
        pygame.draw.rect(surface, self.outline, self.bottom_rect,4)
        
        surface.blit(rendered_height, (self.bottom_rect.topleft[0]+5, self.bottom_rect.topleft[1]+15))
        surface.blit(rendered_name, (self.bottom_rect.topleft[0]+5, self.bottom_rect.topleft[1]+40))
        surface.blit(rendered_fps, (self.bottom_rect.topleft[0]+5, self.bottom_rect.topleft[1]+65))
        surface.blit(rendered_food, (self.bottom_rect.topleft[0]+5, self.bottom_rect.topleft[1]+90))
        surface.blit(rendered_wood, (self.bottom_rect.topleft[0]+5, self.bottom_rect.topleft[1]+115))
        surface.blit(rendered_population, (self.bottom_rect.topleft[0]+5, self.bottom_rect.topleft[1]+140))
        surface.blit(rendered_pos_str, (self.bottom_rect.topleft[0]+5, self.bottom_rect.topleft[1]+165))
        
        pygame.draw.rect(surface, self.outline,(0,0,self.w,self.h),4)
        
        
        
    def update(self, Tile=None):
        for x in range(self.len_tiles_x):
            for y in range(self.len_tiles_y):
                try:
                    self.tiles[x][y].selected = False
                    if self.tiles[x][y] == Tile:
                        self.tiles[x][y].selected = True
                        
                    self.tiles[x][y].render(self.top_render)
                    pygame.draw.rect(self.top_render, self.outline, (x*self.tile_width,y*self.tile_height,self.tile_width,self.tile_height),2)
                except Exception:
                    pass
    
class icon_tile():
    
    def __init__(self, const, representing, pos):
        self.selected_image = pygame.image.load("Images/Buildings/SELECTED_%s_Icon.png"%representing)
        self.icon_image = pygame.image.load("Images/Buildings/%s_Icon.png"%representing)

        self.icon_image = pygame.transform.scale(self.icon_image, const)
        self.selected_image = pygame.transform.scale(self.selected_image, const)
        
        self.rep = representing
        self.pos = pos
        self.rect = self.icon_image.get_rect()
        self.rect.topleft = self.pos
        self.selected = False
        
    def render(self, surface):
        if self.selected:
            surface.blit(self.selected_image, self.pos)
        else:
            surface.blit(self.icon_image, self.pos)
