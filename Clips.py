import pygame

dialol = pygame.image.load("Images/Dial/dial_outline2.png")
dial = pygame.image.load("Images/Dial/dial.png")
dialol.set_colorkey((255, 0, 255))
dial.set_colorkey((255, 0, 255))

buildings = ["House", "LumberYard", "Dock", "Manor", "Town Center"]


class Clips(object):
    """
    ______________________
    |                    |
    |                    |
    |                    |
    |                    |
    |                    |
    |                    |
    |               _____|
    |              |MINI-|
    |              |MAP  |
    ----------------------
    """

    def __init__(self, world, screen_size):
        self.size = screen_size
        self.world = world

        # The minimap is 1/4 the size of the screen in each dimension (1/16 total size)
        self.minimap_size = int(self.size[0] / 4), int(self.size[1] / 4)

        # TODO: Is this necessary?
        self.minimap = pygame.transform.scale(
            self.world.minimap_img,
            self.minimap_size)

        # Ratio between the size of the tile array and the minimap size
        self.a = self.world.w / float(self.minimap_size[0])
        self.b = self.world.h / float(self.minimap_size[1])

        # Not quite sure what this does
        self.rect_view_w = (self.size[0] / self.a) - ((self.size[0] / self.a) / 5)
        self.rect_view_h = self.size[1] / self.b

        self.minimap_rect = pygame.Rect(self.size[0] - self.minimap_size[0], self.size[1] - self.minimap_size[1],
                                        self.minimap_size[0], self.minimap_size[1])

    def render(self, surface):

        rect_view_pos = (
            (-1 * self.world.world_position.x / self.a) + self.size[0] - self.minimap_size[0] + ((self.size[0] / 5) / self.a),
            (-1 * self.world.world_position.y / self.b) + self.size[1] - self.minimap_size[1])

        rect_view = (
            rect_view_pos,
            (self.rect_view_w,
             self.rect_view_h))

        self.world.render(surface)
        # self.update_dial(surface, tp)

        # Draw minimap below here ------------------
        surface.set_clip(self.minimap_rect)

        # Drawing the actual minimap
        surface.blit(self.minimap, self.minimap_rect)

        # Draw the white rectangle displaying where the user is located
        pygame.draw.rect(surface, (255, 255, 255), rect_view, 1)

        # Draw a black border
        pygame.draw.rect(surface, (0, 0, 0), self.minimap_rect, 2)

        surface.set_clip(None)
        # Draw minimap above here --------------------

    def update_dial(self, surface, tp):  # Dial goes below here
        box = (self.size[0] - 55, self.size[1] / 50 - 40)
        boxtest = pygame.Rect((box[0] - 20, box[1] + 80), (50, 50))
        oldCenter = boxtest.center
        rotateddial = pygame.transform.rotate(dial, self.world.clock_degree)
        rotRect = rotateddial.get_rect()
        rotRect.center = oldCenter
        self.world.clock_degree += tp
        if self.world.clock_degree >= 360.0:
            self.world.clock_degree = 0.0

        surface.blit(rotateddial, rotRect)
        surface.blit(dialol, (box[0] - 44, box[1] + 55))