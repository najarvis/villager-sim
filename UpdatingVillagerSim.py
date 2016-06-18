"""This will basically be a rewrite of the original file,
   but this time with a focus on clean code and commenting."""

import pygame
import gametools.vector2
import World
import sys

def run(fullscreen):
    """The main function to run the program.

    Args:
        fullscreen: Boolean value that determines if the program is
            in fullscreen mode.

    Returns:
        None
    """

    pygame.init()
    screen_size = (1280, 720)
    if fullscreen:
        screen = pygame.display.set_mode(pygame.display.list_modes()[0],
                pygame.FULLSCREEN | pygame.HWSURFACE)
    else:
        screen = pygame.display.set_mode(screen_size, 0)

    game_world = World.World((64, 64), screen_size)

    pygame.display.set_caption("Villager Sim")

    # Tick the clock once to avoid one huge tick when the game starts
    game_world.clock.tick()

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

        if pygame.mouse.get_pressed()[0]:

            # This code moves the view to where the user is clicking in
            # the minimap. Don't ask me how it works, I have no idea.
            if (pos.x > game_world.clipper.minimap_rect.x and \
                pos.y > game_world.clipper.minimap_rect.y):

                x_temp_1 = -game_world.clipper.a * (pos.x - game_world.clipper.minimap_rect.x)
                x_temp_2 = game_world.clipper.rect_view_w * game_world.clipper.a
                game_world.world_position.x = x_temp_1 + (x_temp_2 / 2)

                y_temp_1 = -game_world.clipper.b * (pos.y - game_world.clipper.minimap_rect.y)
                y_temp_2 = game_world.clipper.rect_view_h * game_world.clipper.b
                game_world.world_position.y = y_temp_1 + (y_temp_2 / 2)

        # Process everything in the game world
        game_world.process(time_passed_seconds)

        # Clear the screen, then draw the world onto it
        screen.fill((0, 0, 0))
        game_world.render_all(screen, time_passed_seconds, pos)

        # Update the screen
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    try:
        run(bool(int(sys.argv[1])))
    except Exception:
        run(False)
