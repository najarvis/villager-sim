import pygame

"""
This is a class I wrote to handle cell-based image storage. Rather than store each image
individually you store each image in one large image split up into self.cells, then use subsurfacing
to get each individual image out. w and h are the individual cell width and height, as each image
may take up more than one cell.
"""


class ImageFuncs():


    def __init__(self, w_cell, h_cell, img):
        """
        :param w_cell: width of one cell
        :param h_cell: height of one cell
        :param img: the image to be divided into cells
        :return: nothing
        """
        self.w_cell = w_cell
        self.h_cell = h_cell
        self.img = img
        self.get_list(self.img)

    def get_list(self, pic):
        """
        :param pic: the picture
        :return: None
        """
        self.w_img, self.h_img = pic.get_size()
        cells = [[0 for i in range(self.w_img // self.w_cell)] for j in range(self.h_img // self.h_cell)]
        for i in range(self.w_img // self.w_cell):
            for a in range(self.h_img // self.h_cell):
                cells[i][a] = pic.subsurface((i*self.w_cell, a*self.h_cell, self.w_cell, self.h_cell))
        self.cells = cells

    def get_cell(self, row, column):
        """
        :param row: num of rows in cell
        :param column: num of columns in in the pic
        :return: The list of images
        """
        return self.cells[row][column]

    def get_image(self, x, y):
        """
        :param x: x location
        :param y: y location
        :return:
        """
        quick_image = pygame.Surface((self.w_cell, self.h_cell))
        quick_image.blit(self.get_cell(x, y), (0, 0))
        return quick_image

    def get_irregular_image(self, num_w, num_h, x, y):
        """
        :param num_w: number width
        :param num_h: number height
        :param x: x location
        :param y: y location
        :return: None
        """
        quick_image = pygame.Surface((self.w_cell*num_w, self.h_cell*num_h))
        for i in range(num_h):
            for g in range(num_w):
                quick_image.blit(self.get_cell(x+i, y+g), (i*self.w_cell, g*self.h_cell))
        return quick_image

    def get_images(self, num_images, x, y):
        """
        :param num_images: number of images
        :param x: x location
        :param y: y location
        :return: List of images at x,y that is number of images long
        """
        lst = []
        for i in range(num_images):
            lst.append(self.get_image(x,y))
            x+=1
        return lst
