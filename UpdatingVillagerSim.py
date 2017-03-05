"""This will basically be a rewrite of the original file,
   but this time with a focus on clean code and commenting."""

import sys
import pygame
import gametools.vector2
import TileFuncs
import World
import DebugTools

def run(fullscreen, world_size=64):
    """The main function to run the program.

    Args:
        fullscreen: Boolean value that determines if the program is
            in fullscreen mode.

        world_size: Integer (power of 2) value that determines the
            dimensions of the game world in terms of tiles.

    Returns:
        None
    """

    pygame.init()
    screen_size = (1280, 720)
    if fullscreen:
        screen_size = pygame.display.list_modes()[0]
        if screen_size[0] > 1920:
            screen_size = (1920, 1080)
        screen = pygame.display.set_mode(screen_size,
                 pygame.FULLSCREEN | pygame.HWSURFACE)
    else:
        screen = pygame.display.set_mode(screen_size, 0)

    game_world = World.World((world_size, world_size), screen_size)

    pygame.display.set_caption("Villager Sim")

    # Tick the clock once to avoid one huge tick when the game starts
    game_world.clock.tick()

    pause = False

    done = False
    while not done:

        # Cap the game at 60 fps
        time_passed_seconds = game_world.clock.tick(60) / 1000.0
        pos = gametools.vector2.Vector2(*pygame.mouse.get_pos())

        for event in pygame.event.get():

            # Close button clicked
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:

                # Escape key pressed
                if event.key == pygame.K_ESCAPE:
                    done = True

                elif event.key == pygame.K_SPACE:
                    pause = not pause
                
                elif event.key == pygame.K_F3:
                    pygame.image.save(game_world.world_surface, "FullScreenshot.png")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    entity = TileFuncs.get_entity(game_world, pos)
                    if entity is not None:
                        # Toggle the entity info
                        entity[1].active_info = not entity[1].active_info

        if pygame.mouse.get_pressed()[0]:
            # check to see if the user is clicking on the minimap and update position accordingly
            game_world.check_minimap_update(pos)

        # Process everything in the game world
        if not pause:
            game_world.process(time_passed_seconds)

        # Clear the screen, then draw the world onto it
        screen.fill((0, 0, 0))
        game_world.render_all(screen)

        # Update the screen
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(bool(int(sys.argv[1])))
    elif len(sys.argv) >= 3:
        run(bool(int(sys.argv[1])), int(sys.argv[2]))
    else:
        run(False)
