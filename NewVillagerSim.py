import pygame

pygame.init()

from random import randint
from vector2 import Vector2
from World import World
from datetime import datetime
from Clips import Clips
from crossfade import CrossFade
from random import randint

def run():
    tile_size = 32 

    font = pygame.font.SysFont("Terminal", 20)

    bool_full = 0
    
    pygame.display.set_caption("Villager Simulation")

    sizes = pygame.display.list_modes()
    screen_size = (1600,900)
    
    """Original screen size"""
    screen_width, screen_height = screen_size
    
    side_size = screen_width/5.0

    if bool_full:
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN|pygame.HWSURFACE, 32)
    else:
        screen = pygame.display.set_mode(screen_size, 0, 32)
    
    fade = CrossFade(screen)
    all_sprites = pygame.sprite.Group(fade)

    draw = False
    held = False
    
    size = (128,128)
    w_size = size[0] * tile_size, size[1] * tile_size

    # seed = randint(0,100)
    seed = None

    world = World(screen_size, w_size, font, seed, screen)
    #pygame.image.save(world.minimap_img, "Images/UBER-COOL-small.png")


    #These are all loaded here to be used in the main file. 
    #TODO: Move these somewhere else
    Villager_image = pygame.image.load("Images/Entities/Villager.png").convert()
    Farmer_image = pygame.image.load("Images/Entities/Farmer.png").convert()
    Lumberjack_image = pygame.image.load("Images/Entities/Lumberjack.png").convert()
    Builder_image = pygame.image.load("Images/Entities/Builder.png").convert()

    placing_lumberyard_img = pygame.image.load("Images/Buildings/Dark_LumberYard.png").convert()
    placing_lumberyard_img.set_colorkey((255, 0, 255))
    placing_house_img = pygame.image.load("Images/Buildings/Dark_House.png").convert()
    placing_house_img.set_colorkey((255, 0, 255))
    placing_dock_img = pygame.image.load("Images/Buildings/Dark_Dock.png").convert()
    placing_dock_img.set_colorkey((255, 0, 255))
    placing_manor_img = pygame.image.load("Images/Buildings/Dark_Manor.png").convert()
    placing_manor_img.set_colorkey((255, 0, 255))

    bad_lumberyard_img = pygame.image.load("Images/Buildings/Red_LumberYard.png").convert()
    bad_lumberyard_img.set_colorkey((255,0,255))
    
    world.clipper = Clips(world, (screen_width, screen_height))
    selected_building = "LumberYard"
    selected_img = pygame.image.load("Images/Buildings/Dark_LumberYard.png").convert()
    selected_img.set_colorkey((255, 0, 255))

    world.clock.tick()
    while True:

        time_passed_seconds = world.clock.tick(60)/1000.
        pos = Vector2(*pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pos.x > world.clipper.minimap_rect.x and pos.y > world.clipper.minimap_rect.y):
                    pass
                else:
                    if event.button == 1:
                        #TODO: Figure out what the fuck this does
                        held = True
                        start = Vector2(*pygame.mouse.get_pos())
                        draw = True
                        if (pos.x < world.clipper.side.w) and (pos.y < world.clipper.side.top_rect.h):
                            for L in world.clipper.side.tiles:
                                for T in L:
                                    if T == None:
                                        continue

                                    if T.rect.collidepoint((pos.x, pos.y)):
                                        if T.selected:
                                            T.selected = False
                                        else:
                                            T.selected = True

                                        selected_building = T.rep
                                        world.clipper.side.update(T)

                        else:
                            selected_building = None
                            world.clipper.side.update()

                    if event.button == 3 and selected_building != None:
                        world.add_building(selected_building, pos)
                        if world.test_buildable(selected_building, 0, pos):
                            selected_building = None
                            world.clipper.side.update()

            if event.type == pygame.MOUSEBUTTONUP:
                draw = False
                held = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2 or event.key == pygame.K_F3 or event.key == pygame.K_F4:
                    str1 = str(datetime.now())
                    str1 = str1.split(".")
                    str2 = str1[0]+str1[1]
                    str2 = str2.split(":")
                    str1 = ""
                    for i in str2:
                        str1 += i
                    if event.key == pygame.K_F2:
                        pygame.image.save(screen, "Images/Screenshots/SCREENSHOT%s.png"%str1)
                    elif event.key == pygame.K_F3:
                        pygame.image.save(world.clipper.minimap, "Images/Screenshots/MinimapSCREENSHOT%s.png"%str1)
                    elif event.key == pygame.K_F4:
                        pygame.image.save(world.background, "Images/Screenshots/FULL_MAP_RENDER%s.png"%str1)
                if event.key == pygame.K_n:
                    world.new_world()
                    # pygame.image.save(world.background, "Images/ShadowsRandomWorldGen.png")

            if event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                
        #------------------Keys Below--------------------------------------------------
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_ESCAPE]:  # quits the game
            pygame.quit()
            exit()

        if pressed_keys[pygame.K_SPACE]:  # Resets wood
            world.wood = 0

        if pressed_keys[pygame.K_d]:  # Fast-forward-esk functionability
            world.clock_degree += 5

        if pressed_keys[pygame.K_l]:  # Test to see what the first entity's state is
            print world.entities[1].brain.active_state

        # --------------Keys Above----------------------------------------
        # --------------Mouse Below---------------------------------------

        if int(pos.x) <= 15:
            if not bool_full:
                pygame.mouse.set_pos((15, pos.y))
            world.background_pos.x += 500*time_passed_seconds
            # print world.background_pos.x
            if world.background_pos.x > side_size:
                world.background_pos.x = side_size
            
        elif int(pos.x) >= screen_width-16:
            if not bool_full:
                pygame.mouse.set_pos((screen_width-16, pos.y))
            world.background_pos.x-=500*time_passed_seconds
            
            
            if world.background_pos.x < -1*(world.w - screen_width):
                world.background_pos.x = -1*(world.w - screen_width)
            
            #print world.background_pos.x
            
        if int(pos.y) <= 15:
            if not bool_full:
                pygame.mouse.set_pos((pos.x, 15))
            world.background_pos.y += 500*time_passed_seconds

            if world.background_pos.y > 0:
                world.background_pos.y = 0
            
        elif int(pos.y) >= screen_height-16:
            
            if not bool_full:
                pygame.mouse.set_pos((pos.x, screen_height-16))
            
            world.background_pos.y-= 500 * time_passed_seconds
            
            if world.background_pos.y < -1*(world.h - screen_height):
                world.background_pos.y = -1*(world.h - screen_height)
            
        if pygame.mouse.get_pressed()[0]:
            if pos.x > world.clipper.minimap_rect.x and pos.y > world.clipper.minimap_rect.y:
                """If the player clicked on the minimap, go to that location with the view centered on the event position"""
                draw = False
                if held != True:
                    world.background_pos.x = (-1*(pos.x-world.clipper.minimap_rect.x)*world.clipper.a)+(
                                                                                                       world.clipper.rect_view_w*world.clipper.a)/2
                    world.background_pos.y = (-1*(pos.y-world.clipper.minimap_rect.y)*world.clipper.b)+(
                                                                                                       world.clipper.rect_view_h*world.clipper.b)/2



        # --------------Mouse Above---------------------------------------
        # --------------Process below-------------------------------------

        world.process(time_passed_seconds)

        if selected_building == "House":
            selected_img = placing_house_img
        elif selected_building == "LumberYard":
            selected_img = placing_lumberyard_img
        elif selected_building == "Dock":
            selected_img = placing_dock_img
        elif selected_building == "Manor":
            selected_img = placing_manor_img

        # --------------Process above-------------------------------------
        # --------------Render Below------------------------

        screen.fill((0, 0, 0))
        world.render_all(screen, time_passed_seconds, pos)

        all_sprites.clear(screen, world.background)
        all_sprites.update()
        all_sprites.draw(screen)

        world.grow_trees(world.Baby_TreeLocations)

        if fade.trans_value == 0:
            all_sprites.remove(fade)

        if selected_building != None:
            if (pos.x > world.clipper.minimap_rect.x and pos.y > world.clipper.minimap_rect.y) or (
                pos.x < world.clipper.side.w+32):
                pass
            else:
                if not world.test_buildable(selected_building, 0, pos):
                    selected_img = bad_lumberyard_img
                blit_pos = world.get_tile_pos(pos-world.background_pos)*32
                screen.blit(selected_img, ((blit_pos.x-(selected_img.get_width()-32))+world.background_pos.x,
                                           (blit_pos.y-(selected_img.get_height()-32))+world.background_pos.y))

        # This is for selecting-------------
        if draw == True and selected_building == None:
            a = Vector2(*pygame.mouse.get_pos())
            lst = world.get_tile_array(start, ((a.x-start.x)/32, (a.x-start.x)/32))
            for i in lst:
                for j in i:
                    j.selected = 1
            s = pygame.Surface((abs(a.x-start.x), abs(a.y-start.y)))
            s.set_alpha(25)
            s.fill((255, 255, 255))
            if a.x-start.x <= 0 and a.y < start.y and a.x > start.x:
                newa = (a.x-(a.x-start.x), a.y)
                screen.blit(s, (newa))
            if a.x-start.x <= 0 and a.y > start.y and a.x < start.x:
                newa = (a.x, a.y-(a.y-start.y))
                screen.blit(s, (newa))
            if a.x-start.x > 0 and a.y-start.y > 0:
                screen.blit(s, (start))
            if a.x-start.x < 0 and a.y-start.y < 0:
                screen.blit(s, (a))
            pygame.draw.rect(screen, (255, 255, 255), (start, (a.x-start.x, a.y-start.y)), 1)
        # Selecting Above------------------

        # --------------Render Above------------------------


        pygame.display.flip()
        # pygame.display.set_caption("%.2f"%world.clock.get_fps())


if __name__ == "__main__":
    run()
