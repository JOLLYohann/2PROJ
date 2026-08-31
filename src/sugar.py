class Sugar:
    def __init__(self, x, y, color):
        self.__x = x
        self.__y = y
        self.__color = color

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_color(self):
        return self.__color

    def set_position(self, x, y):
        self.__x = x
        self.__y = y

    def set_color(self, color):
        self.__color = color