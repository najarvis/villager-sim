from GameEntity import GameEntity
from StateMachine import State
from Tile import *
from Image_funcs import *

from random import randint

import pygame

NoTreeImg = pygame.image.load("Images/Tiles/MinecraftGrass.png")

class Lumberjack(GameEntity):
    
    def __init__(self, world, img):
        GameEntity.__init__(self,world,"Lumberjack", img)
        img_func = image_funcs(18,17)
        
        self.speed = 100.
        self.can_see = (1,1)
        
        self.searching_state = Searching(self)
        self.chopping_state = Chopping(self)
        self.delivering_state = Delivering(self)
        
        self.brain.add_state(self.searching_state)
        self.brain.add_state(self.chopping_state)
        self.brain.add_state(self.delivering_state)
        
        self.worldSize = world.size
        self.TileSize = self.world.TileSize
        
        self.row = 1
        self.times = 3
        self.pic = pygame.image.load("Images/Entities/map.png")
        self.cells = img_func.get_list(self.pic)
        self.ani = img_func.get_images(self.cells,self.times,1,1,1,self.row,self.pic)
        self.start = img_func.get_image(self.cells,1,1,0,self.row,self.pic)
        self.num = 0
        self.num_max = len(self.ani)-1
        self.ani_speed_init = 10
        self.ani_speed = self.ani_speed_init
        self.img = self.ani[0]
        self.update()
        self.hit = 0
        self.main_des = 0

        
    def update(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.image = self.ani[self.num]
            self.image.set_colorkey((255,0,255))
            self.ani_speed = self.ani_speed_init
            if self.num == self.num_max:
                self.num = 0
                self.hit += 1
            else:
                self.num += 1
        

        
class Searching(State):
    """This state will be used to have the Lumberjack looking for
       trees to cut, It needs to be fast enough to have AT LEAST 20 Lumberjacks
       with little to no framerate loss.
       
       Perhaps it could be used to find a clump of trees. and then the Lumberjack
       wouldn't just wander around aimlessly searching for trees even though it
       saw some when it was just at another tree"""
    
    def __init__(self, Lumberjack):
        State.__init__(self, "Searching")
        self.Lumberjack = Lumberjack
        
    def entry_actions(self):
        pass

    def do_actions(self):
        pass
    
    def check_conditions(self):
        if self.Lumberjack.location.get_distance_to(self.Lumberjack.destination) < 2:
            self.tile_array = self.Lumberjack.world.get_tile_array((self.Lumberjack.location),self.Lumberjack.can_see)
            test = self.Lumberjack.world.get_tile(self.Lumberjack.location)
            
            #pygame.draw.rect(self.Lumberjack.world.background, (255,255,255), (test.location[0]-(self.Lumberjack.can_see[0]<<5),test.location[1]-(self.Lumberjack.can_see[1]<<5),(self.Lumberjack.can_see[0]<<6)+32,(self.Lumberjack.can_see[1]<<6)+32), 3)
            
            count = 0
            for i in self.tile_array:
                for Tile in i:
                    count+=1
                    if Tile != None:
                
                        if Tile.name == "TreePlantedTile_W":
                            self.Lumberjack.Tree_tile = Tile
                            self.Lumberjack.tree_id = Tile.id
                            if count == 1:
                                self.Lumberjack.destination = (self.Lumberjack.location[0]-32,self.Lumberjack.location[1]-32)

                            elif count == 2:
                                self.Lumberjack.destination = (self.Lumberjack.location[0],self.Lumberjack.location[1]-32)

                            elif count == 3:
                                self.Lumberjack.destination = (self.Lumberjack.location[0]+32,self.Lumberjack.location[1]-32)

                            elif count == 4:
                                self.Lumberjack.destination = (self.Lumberjack.location[0]-32,self.Lumberjack.location[1])

                            elif count == 5:
                                self.Lumberjack.destination = (self.Lumberjack.location[0],self.Lumberjack.location[1])

                            elif count == 6:
                                self.Lumberjack.destination = (self.Lumberjack.location[0]+32,self.Lumberjack.location[1])

                            elif count == 7:
                                self.Lumberjack.destination = (self.Lumberjack.location[0]-32,self.Lumberjack.location[1]+32)

                            elif count == 8:
                                self.Lumberjack.destination = (self.Lumberjack.location[0],self.Lumberjack.location[1]+32)

                            elif count == 9:
                                self.Lumberjack.destination = (self.Lumberjack.location[0]+32,self.Lumberjack.location[1]+32)
                                
                            self.Lumberjack.main_des = self.Lumberjack.destination
                            return "Chopping"

                                
                            
            self.random_dest()
    
    def exit_actions(self):
        pass
    
    def random_dest(self):
        #Function for going to a random destination, currently limited to top 1/12 of the map
        w,h = self.Lumberjack.worldSize
        offset = self.Lumberjack.TileSize/2
        TileSize = self.Lumberjack.TileSize
        random_dest = (randint(0,25)*TileSize+offset, randint(0,25)*TileSize+offset)
        self.Lumberjack.destination = Vector2(*random_dest)
    
class Chopping(State):
    
    def __init__(self, Lumberjack):
        State.__init__(self, "Chopping")
        self.Lumberjack = Lumberjack
        
    def entry_actions(self):
        pass
    
    def do_actions(self):
        pass
    
    def check_conditions(self):
        check = self.Lumberjack.world.get_tile(Vector2(self.Lumberjack.location))
        if self.Lumberjack.location.get_distance_to(self.Lumberjack.main_des) < 2 :
            self.Lumberjack.destination = Vector2(self.Lumberjack.location)
            
            if check.name != "TreePlantedTile_W":
                self.Lumberjack.hit = 0
                self.Lumberjack.num = 0
                self.Lumberjack.image = self.Lumberjack.start
                self.Lumberjack.ani_speed = self.Lumberjack.ani_speed_init
                return "Searching"

            self.Lumberjack.update()
            
            if self.Lumberjack.hit == 4:
                self.Lumberjack.destination = Vector2(self.Lumberjack.location)
                self.Lumberjack.image = self.Lumberjack.start
                self.Lumberjack.image.set_colorkey((255,0,255))
                
                old_tile = self.Lumberjack.world.get_tile(Vector2(self.Lumberjack.location))
                
                darkness = pygame.Surface((32,32))
                darkness.set_alpha(old_tile.darkness)
                
                new_tile = TreePlantedTile(self.Lumberjack.world, NoTreeImg)
                
                new_tile.darkness = old_tile.darkness
                
                new_tile.location = self.Lumberjack.world.get_tile_pos(self.Lumberjack.destination)*32
                new_tile.rect.topleft = new_tile.location
                new_tile.color = old_tile.color

                
                self.Lumberjack.world.TileArray[int(new_tile.location.y/32)][int(new_tile.location.x/32)] = new_tile
                self.Lumberjack.world.background.blit(new_tile.img, new_tile.location)
                self.Lumberjack.world.background.blit(darkness, new_tile.location)

                self.Lumberjack.hit = 0

                #del self.Lumberjack.world.TreeLocations[str(self.Lumberjack.tree_id)]
                return "Delivering"
    
    def exit_actions(self):
        pass
    
class Delivering(State):
    
    """This state will be used solely to deliver wood from wherever the Lumberjack
       got the wood to the closest Lumber yard. maybe all the lumber yards could
       be stored in a dictionary similar to trees, that would be much faster"""
    
    def __init__(self, Lumberjack):
        State.__init__(self, "Delivering")
        self.Lumberjack = Lumberjack
        
    def entry_actions(self):

        des = self.Lumberjack.world.get_close_entity("LumberYard",self.Lumberjack.location, 100)
        if des == None:
            des = self.Lumberjack.world.get_close_entity("LumberYard",self.Lumberjack.location, 300)
            if des == None:
                des = self.Lumberjack.LastLumberYard
        
        self.Lumberjack.LastLumberYard = des
                    
        self.Lumberjack.destination = des.location.copy()
    
    def do_actions(self):
        pass
        
    def check_conditions(self):

        #if self.Lumberjack.world.wood >= self.Lumberjack.world.MAXwood:
        #    return "IDLE"
        
        if self.Lumberjack.location.get_distance_to(self.Lumberjack.destination) < 2.0:
            self.Lumberjack.world.wood+=5
            return "Searching"

    
    def exit_actions(self):
        pass
    
class IDLE(State):
    
    def __init__(self, Lumberjack):
        State.__init__(self, "Delivering")
        self.Lumberjack = Lumberjack
        
    def entry_actions(self):
        pass
    
    def do_actions(self):
        pass
    
    def check_conditions(self):
        pass
    
    def exit_actions(self):
        pass
