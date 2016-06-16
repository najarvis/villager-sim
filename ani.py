class Ani(object):
    """
    Creates an animation given the cell width, height, and the image and it returns the image needed at the time passed
    in seconds
    """

    def __init__(self,num,counter):
        self.counter_max = counter
        self.counter = counter
        self.finished = False
        self.ani_num_max = num
        self.ani_num = 0


    def reset(self):
        self.counter = self.counter_max
        self.ani_num = 0


    def get_frame(self):
        self.counter -= 1
        if self.counter <= 0:
            self.counter = self.counter_max
            self.ani_num += 1
            if self.ani_num == self.ani_num_max:
                self.reset()
                self.finished = True
        return self.ani_num


