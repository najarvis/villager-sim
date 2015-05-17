import pygame
pygame.init()

class CrossFade(pygame.sprite.Sprite):
    
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        w,h = surface.get_size()
        self.image = pygame.Surface((w,h))
        self.image = self.image.convert()
        self.image.fill((0,0,0))
        
        self.rect = self.image.get_rect()
        
        self.fade_dir = 1
        
        #255 is opaque, 0 is transparent
        self.trans_value = 255
        
        self.fade_speed = 5
        
        self.delay = 1
        
        #increment increases with each frame (each call to update)
        self.increment = 0
        
        self.image.set_alpha(self.trans_value)
        
        self.rect.centerx = w/2
        self.rect.centery = h/2
        
    def update(self):
        self.image.set_alpha(self.trans_value)
        
        self.increment+=1
        
        if self.increment >= self.delay:
            self.increment = 0
            
            if self.fade_dir > 0:
                #Make sure transparent value doesn't go negative
                if self.trans_value - self.fade_speed < 0:
                    self.trans_value = 0
                else:
                    self.trans_value -= self.fade_speed
                    
            elif self.fade_dir < 0:
                if self.trans_value + self.fade_speed > 255:
                    self.trans_value = 255
                    
                else:
                    self.trans_value+=self.fade_speed
                    
def main(screen):
    pygame.display.set_caption("Fading")
    
    clock = pygame.time.Clock()
    keepPlaying = True
    
    logo = pygame.image.load("me.jpg")
    
    screen.blit(logo, (0,0))
    
    fade = CrossFade(screen)
    all_Sprites = pygame.sprite.Group(fade)
    
    while keepPlaying:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepPlaying = False
                
        if fade.trans_value == 0:
            pygame.time.delay(1500)
            fade.fade_dir *= -1
            
        all_Sprites.clear(screen, logo)
        all_Sprites.update()
        all_Sprites.draw(screen)
        
        pygame.display.flip()
