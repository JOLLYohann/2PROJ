def portal_from_json(data):
    x = data["x"]
    y = data["y"]
    size = data.get("size", 20)
    output_color = data["output_color"]
    return Portal(x, y, size, output_color)


class Portal:
    def __init__(self, x, y, size, output_color):
        self.__x = x
        self.__y = y
        self.__size = size
        self.__output_color = output_color

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_size(self):
        return self.__size

    def get_output_color(self):
        return self.__output_color

    def covered_cells(self):
        for dy in range(self.__size):
            for dx in range(self.__size):
                yield (self.__x + dx, self.__y + dy)