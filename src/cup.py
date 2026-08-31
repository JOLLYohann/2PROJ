def cup_from_json(data):
    x = data["x"]
    y = data["y"]
    size = data.get("size", 40)
    if "colors" in data:
        # Cup multi-couleur, ex: {"colors": {"red": 10, "blue": 10}}
        requirements = dict(data["colors"])
    else:
        # Cup mono-couleur, ex: {"color": "white", "capacity": 20}
        requirements = {data.get("color", "white"): data["capacity"]}
    return Cup(x, y, size, requirements)


class Cup:
    def __init__(self, x, y, size, requirements):
        self.__x = x
        self.__y = y
        self.__size = size
        self.__requirements = requirements
        self.__filled = {color: 0 for color in requirements}

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_size(self):
        return self.__size

    def get_requirements(self):
        return self.__requirements

    def get_filled(self):
        return self.__filled

    def mouth_cells(self):
        for dx in range(self.__size):
            yield (self.__x + dx, self.__y)

    def accepts_color(self, color):
        return color in self.__requirements and self.__filled[color] < self.__requirements[color]

    def is_full(self):
        return all(self.__filled[color] >= amount for color, amount in self.__requirements.items())

    def catch_grain(self, color):
        if not self.accepts_color(color):
            return False
        self.__filled[color] += 1
        return True