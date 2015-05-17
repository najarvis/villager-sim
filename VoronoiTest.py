import pygame
from pygame.locals import *
from random import randint

screen_size = (256,256)
w,h = screen_size
screen = pygame.display.set_mode(screen_size)

class point:
    
    def __init__(self, pos):
        self.pos = pos
        self.x=pos[0]
        self.y=pos[1]

    def get_distance(self, p2):
        try:
            distance = float((p2.x-self.x)**2)+((p2.y-self.y)**2)
        except DivideByZeroError:
            distance = 0
        self.distance = distance
        return distance
        
def whole_new(num_R, size=(256,256)):

    surface = pygame.Surface(size)

    point_list = [point((randint(0,w), randint(0,h))) for i in range(num_R)]
    p1 = point((w/2,h/2))
    new_pointlist = sorted(point_list, key=lambda point: point.get_distance(p1))

    pygame.display.set_caption("CALCULATING")

    maxB=0
    minB=0


    surface.lock()
    for y in xrange(h):
        for x in xrange(w):
            currentPoint = point((x,y))
            new_pointlist = sorted(point_list, key=lambda point: point.get_distance(currentPoint))
            currentPoint.brightness = int(new_pointlist[1].distance )/(num_R*(w/256))
            maxB = max(maxB, currentPoint.brightness)
            minB = min(minB, currentPoint.brightness)
            clr = abs(currentPoint.brightness)
            clr = min(255, clr)
            surface.set_at((x,y), (clr, clr, clr))
    surface.unlock()

    pygame.display.set_caption("DONE")

    print maxB, minB

    return surface

surface = whole_new(25)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done=True
            elif event.key == K_F2:
                pygame.image.save(screen, "SCREENSHOT_TOSAVE.png")
            elif event.key == K_SPACE:
                surface = whole_new(25)
            

    screen.blit(surface, (0,0))
    pygame.display.flip()
    
pygame.display.quit()

