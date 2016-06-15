#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame

pygame.init()

from gametools.vector2 import Vector2
from World import World
from datetime import datetime
from Clips import Clips


def run():
    """Run the Game"""
    tile_size = 32
    font = pygame.font.SysFont("Terminal", 20)
    bool_full = False
    screen_size = (1280, 720)

    screen_width, screen_height = screen_size

    side_size = screen_width / 5.0

    if bool_full:
        screen = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN | pygame.HWSURFACE, 32)
    else:
        screen = pygame.display.set_mode(screen_size, 0, 32)

    draw = False
    held = False

    s_size = 128
    size = (s_size, s_size)

    seed = None

    world = World(size, font, seed, screen_size)

    # These are all loaded here to be used in the main file.
    # TODO: Move these somewhere else
    placing_lumberyard_img = pygame.image.load("Images/Buildings/Dark_LumberYard.png").convert()
    placing_lumberyard_img.set_colorkey((255, 0, 255))
    
    placing_house_img = pygame.image.load("Images/Buildings/Dark_House.png").convert()
    placing_house_img.set_colorkey((255, 0, 255))
    
    placing_dock_img = pygame.image.load("Images/Buildings/Dark_Dock.png").convert()
    placing_dock_img.set_colorkey((255, 0, 255))
    
    placing_manor_img = pygame.image.load("Images/Buildings/Dark_Manor.png").convert()
    placing_manor_img.set_colorkey((255, 0, 255))

    bad_lumberyard_img = pygame.image.load("Images/Buildings/Red_LumberYard.png").convert()
    bad_lumberyard_img.set_colorkey((255, 0, 255))

    world.clipper = Clips(world, (screen_width, screen_height))
    selected_building = "LumberYard"
    selected_img = pygame.image.load(
        "Images/Buildings/Dark_LumberYard.png").convert()
    selected_img.set_colorkey((255, 0, 255))

    world.clock.tick()
    done = False
    while not done:
        
        time_passed_seconds = world.clock.tick_busy_loop(60) / 1000.
        pos = Vector2(*pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pos.x > world.clipper.minimap_rect.x and pos.y >
                        world.clipper.minimap_rect.y):
                    pass
                else:
                    if event.button == 1 and selected_building is None:
                        """This determines what icon you clicked on in the building selector"""
                        held = True
                        start = Vector2(*pygame.mouse.get_pos())
                        draw = True
                        if (pos.x < world.clipper.side.w) and (pos.y < world.clipper.side.top_rect.h):
                            for tile_list in world.clipper.side.tiles:
                                for tile in tile_list:
                                    if tile is None:
                                        continue

                                    if tile.rect.collidepoint((pos.x, pos.y)):
                                        if tile.selected:
                                            tile.selected = False
                                        else:
                                            tile.selected = True

                                        selected_building = tile.rep
                                        world.clipper.side.update(tile)

                        else:
                            world.clipper.side.update()

                    elif event.button == 1 and selected_building is not None:
                        if pos.x > world.clipper.side.w:
                            world.add_building(selected_building, pos)
                            if world.test_buildable(selected_building, 0, pos):
                                selected_building = None
                                world.clipper.side.update()
                            
                    if event.button == 3:
                        selected_building = None

            if event.type == pygame.MOUSEBUTTONUP:
                draw = False
                held = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2 or event.key == pygame.K_F3 or \
                        event.key == pygame.K_F4:
                    str1 = str(datetime.now())
                    str1 = str1.split(".")
                    str2 = str1[0] + str1[1]
                    str2 = str2.split(":")
                    str1 = ""
                    for i in str2:
                        str1 += i
                        
                    if event.key == pygame.K_F2:
                        pygame.image.save(screen, "Images/Screenshots/SCREENSHOT%s.png" %str1)
                        
                    elif event.key == pygame.K_F3:
                        pygame.image.save(world.clipper.minimap, "Images/Screenshots/MinimapSCREENSHOT%s.png" %str1)
                        
                    elif event.key == pygame.K_F4:
                        pygame.image.save(world.background, "Images/Screenshots/FULL_MAP_RENDER%s.png" %str1)
                        
                if event.key == pygame.K_n:
                    world.new_world()

                if event.key == pygame.K_ESCAPE:
                    done = True

            if event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size

        # ------------------Keys Below--------------------------------------
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_ESCAPE]:  # quits the game
            done = True

        if pressed_keys[pygame.K_SPACE]:  # Resets wood
            world.wood = 0

        if pressed_keys[pygame.K_d]:  # Fast-forward function
            world.clock_degree += 5

        # Test to see what the first entity'select_surface state is
        if pressed_keys[pygame.K_l]:
            print world.entities[0].brain.active_state

        # --------------Keys Above----------------------------------------
        # --------------Mouse Below---------------------------------------

        if int(pos.x) <= 15:
            if not bool_full:
                pygame.mouse.set_pos((15, pos.y))
            world.background_pos.x += 500 * time_passed_seconds
            # print world.background_pos.x
            if world.background_pos.x > side_size:
                world.background_pos.x = side_size

        elif int(pos.x) >= screen_width - 16:
            if not bool_full:
                pygame.mouse.set_pos((screen_width - 16, pos.y))
            world.background_pos.x -= 500 * time_passed_seconds

            if world.background_pos.x < -1 * (world.w - screen_width):
                world.background_pos.x = -1 * (world.w - screen_width)

            # print world.background_pos.x

        if int(pos.y) <= 15:
            if not bool_full:
                pygame.mouse.set_pos((pos.x, 15))
            world.background_pos.y += 500 * time_passed_seconds

            if world.background_pos.y > 0:
                world.background_pos.y = 0

        elif int(pos.y) >= screen_height - 16:

            if not bool_full:
                pygame.mouse.set_pos((pos.x, screen_height - 16))

            world.background_pos.y -= 500 * time_passed_seconds

            if world.background_pos.y < -1 * (world.h - screen_height):
                world.background_pos.y = -1 * (world.h - screen_height)

        if pygame.mouse.get_pressed()[0]:
            if pos.x > world.clipper.minimap_rect.x and pos.y > world.clipper.minimap_rect.y:
                """ If the player clicked on the mini map,
                    go to that location with the view centered on the event position"""
                draw = False
                if not held:
                    # E712 comparison to True should be 'if cond is not True:' or 'if not cond:'
                    world.background_pos.x = (-1 * (pos.x - world.clipper.minimap_rect.x) * world.clipper.a) + (
                        world.clipper.rect_view_w * world.clipper.a) / 2

                    world.background_pos.y = (-1 * (pos.y - world.clipper.minimap_rect.y) * world.clipper.b) + (
                        world.clipper.rect_view_h * world.clipper.b) / 2

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

        world.grow_trees(world.baby_tree_locations)

        if selected_building is not None:
            if (pos.x > world.clipper.minimap_rect.x and pos.y > world.clipper.minimap_rect.y) or (
                    pos.x < world.clipper.side.w + 32):
                pass
            else:
                if not world.test_buildable(selected_building, 0, pos):
                    selected_img = bad_lumberyard_img
                blit_pos = world.get_tile_pos(pos - world.background_pos) * 32
                screen.blit(selected_img, ((blit_pos.x - (selected_img.get_width() - 32)) + world.background_pos.x,
                                           (blit_pos.y - (selected_img.get_height() - 32)) + world.background_pos.y))

        # This is for selecting-------------
        if draw and selected_building is None:
            # E712 comparison to True should be 'if cond is True:' or 'if cond:'
            # E711 comparison to None should be 'if cond is None:'
            current_mouse_pos = Vector2(*pygame.mouse.get_pos())

            lst = world.get_tile_array(start, ((current_mouse_pos.x - start.x) / 32, (current_mouse_pos.x - start.x) / 32))
            for i in lst:
                for j in i:
                    j.selected = 1

            select_surface = pygame.Surface((abs(current_mouse_pos.x - start.x), abs(current_mouse_pos.y - start.y)))
            select_surface.set_alpha(25)
            select_surface.fill((255, 255, 255))

            if current_mouse_pos.x - \
                    start.x <= 0 and current_mouse_pos.y < start.y and current_mouse_pos.x > start.x:
                newa = (current_mouse_pos.x - (current_mouse_pos.x - start.x), current_mouse_pos.y)
                screen.blit(select_surface, (newa))
            if current_mouse_pos.x - \
                    start.x <= 0 and current_mouse_pos.y > start.y and current_mouse_pos.x < start.x:
                newa = (current_mouse_pos.x, current_mouse_pos.y - (current_mouse_pos.y - start.y))
                screen.blit(select_surface, (newa))
            if current_mouse_pos.x - \
                    start.x > 0 and current_mouse_pos.y - start.y > 0:
                screen.blit(select_surface, (start))
            if current_mouse_pos.x - \
                    start.x < 0 and current_mouse_pos.y - start.y < 0:
                screen.blit(select_surface, (current_mouse_pos))
            pygame.draw.rect(
                screen, (255, 255, 255), (start, (current_mouse_pos.x - start.x, current_mouse_pos.y - start.y)), 1)
        # Selecting Above------------------

        # --------------Render Above------------------------

        pygame.display.flip()
        pygame.display.set_caption("VillagerSim! Have fun!")

    pygame.quit()

if __name__ == "__main__":
    run()
