import pygame
from pygame.locals import *
pygame.init()
 
w = 640
h = 480
screen_size = w,h
 
screen = pygame.display.set_mode(screen_size)


done = False
clock = pygame.time.Clock()

class lumberjack:
    def __init__(self):
        self.x = w/2
        self.y = h/2
        self.ani = ["Farmer_dig1.png","Farmer_dig2.png","Farmer_dig3.png","Farmer_dig4.png","Farmer_dig5.png","Farmer_dig6.png"]
        self.num = 0
        self.num_max = len(self.ani)-1
        self.ani_speed_init = 10
        self.ani_speed = self.ani_speed_init
        self.img = pygame.image.load(self.ani[0])
        self.update(0)
        
    def update(self, num):
        if num != 0:
            self.ani_speed -= 1
            if self.ani_speed == 0:
                self.img = pygame.image.load(self.ani[self.num])
                self.ani_speed = self.ani_speed_init
                if self.num == self.num_max:
                    self.num = 0
                else:
                    self.num += 1
        self.img.set_colorkey((255,0,255))
        screen.blit(self.img,(self.x,self.y))
            
lum = lumberjack()

num = 1
while done == False:
    tp = clock.tick(60)
    tps = tp/1000.
    screen.fill((255,255,255))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
    
    lum.update(num)
        
    
    pygame.display.flip()
    
pygame.quit()