def obstacle_from_json(data):
    shape = data["shape"]
    if shape == "rect":
        return Wall(shape, {"x": data["x"], "y": data["y"],
                                 "width": data["width"], "height": data["height"]})
    if shape == "circle":
        return Wall(shape, {"x": data["x"], "y": data["y"], "radius": data["radius"]})
    if shape == "triangle":
        return Wall(shape, {"points": data["points"]})
    raise ValueError(f"Unknown obstacle shape: {shape}")


def point_in_triangle(pt, v1, v2, v3):
    def sign(a, b, c):
        return (a[0] - c[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (a[1] - c[1])

    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)


def distance_to_segment(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    length_squared = dx * dx + dy * dy

    if length_squared == 0:
        # x1,y1 == x2,y2 : le "segment" est en fait un point
        return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5

    t = ((px - x1) * dx + (py - y1) * dy) / length_squared
    t = max(0, min(1, t))  # borne la projection aux deux extrémités du segment

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    return ((px - closest_x) ** 2 + (py - closest_y) ** 2) ** 0.5


class Wall:
    def __init__(self, shape, params):
        self.__shape = shape
        self.__params = params

    def get_shape(self):
        return self.__shape

    def get_params(self):
        return self.__params

    def covered_cells(self):
        if self.__shape == "rect":
            yield from self.__rect_cells()
        elif self.__shape == "circle":
            yield from self.__circle_cells()
        elif self.__shape == "triangle":
            yield from self.__triangle_cells()
        elif self.__shape == "line":
            yield from self.__line_cells()

    def __rect_cells(self):
        p = self.__params
        for y in range(p["y"], p["y"] + p["height"]):
            for x in range(p["x"], p["x"] + p["width"]):
                yield (x, y)

    def __circle_cells(self):
        p = self.__params
        cx, cy, r = p["x"], p["y"], p["radius"]
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
                    yield (x, y)

    def __triangle_cells(self):
        pts = self.__params["points"]
        min_x = min(p[0] for p in pts)
        max_x = max(p[0] for p in pts)
        min_y = min(p[1] for p in pts)
        max_y = max(p[1] for p in pts)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if point_in_triangle((x, y), *pts):
                    yield (x, y)

    def __line_cells(self):
        p = self.__params
        x1, y1, x2, y2 = p["x1"], p["y1"], p["x2"], p["y2"]
        thickness = p["thickness"]
        min_x = min(x1, x2) - thickness
        max_x = max(x1, x2) + thickness
        min_y = min(y1, y2) - thickness
        max_y = max(y1, y2) + thickness
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if distance_to_segment(x, y, x1, y1, x2, y2) <= thickness / 2:
                    yield (x, y)