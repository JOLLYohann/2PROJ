import json
import os

from src.cup import cup_from_json
from src.wall import obstacle_from_json, Wall
from src.portal import portal_from_json
from src.settings import LOGICAL_SIZE
from src.sugar import Sugar


def find_level(level_id = None):
    project_root = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(project_root, "cache", "level_data.json")

    with open(json_path, encoding="utf-8") as file:
        all_levels = json.load(file)

    if level_id:
        return all_levels[level_id]
    return all_levels

def load_cup(cup_data, level):
    cup = cup_from_json(cup_data)
    level.add_cup(cup)

    for (x, y) in cup.mouth_cells():
        level.place(cup, x, y)

    x, y, size = cup.get_x(), cup.get_y(), cup.get_size()
    thickness = 4  

    left_wall = Wall("rect", {"x": x, "y": y, "width": thickness, "height": size})
    right_wall = Wall("rect", {"x": x + size - thickness, "y": y, "width": thickness, "height": size})
    bottom_wall = Wall("rect", {"x": x, "y": y + size - thickness, "width": size, "height": thickness})

    for wall in (left_wall, right_wall, bottom_wall):
        for (wx, wy) in wall.covered_cells():
            level.place(wall, wx, wy)


def load_portal(portal_data, level):
    portal = portal_from_json(portal_data)
    level.add_portal(portal)

    for (x, y) in portal.covered_cells():
        level.place(portal, x, y)
        level.register_portal_cell(x, y, portal)

    x, y, size = portal.get_x(), portal.get_y(), portal.get_size()
    thickness = 4
    left_wall = Wall("rect", {"x": x, "y": y, "width": thickness, "height": size})
    right_wall = Wall("rect", {"x": x + size - thickness, "y": y, "width": thickness, "height": size})

    for wall in (left_wall, right_wall):
        for (wx, wy) in wall.covered_cells():
            level.place(wall, wx, wy)


def load_level(level_id):
    data = find_level(level_id)

    spawn_point = tuple(data["spawn_point"])  # [x, y] en JSON -> (x, y) en Python
    grain_color = data.get("grain_color", "white")

    level = Level(spawn_point, data.get("total_grains"), grain_color)

    for obstacle_data in data["obstacles"]:
        obstacle = obstacle_from_json(obstacle_data)
        level.add_wall(obstacle)
        for (x, y) in obstacle.covered_cells():
            level.place(obstacle, x, y)

    for cup_data in data["cups"]:
        load_cup(cup_data, level)

    for portal_data in data.get("portals", []):
        load_portal(portal_data, level)

    return level


class Level:
    def __init__(self, spawn_point, total_grains, grain_color="white"):
        self.__width, self.__height = LOGICAL_SIZE
        self.__grid = [[None for _ in range(self.__width)] for _ in range(self.__height)]
        self.__grains = []
        self.__walls = []
        self.__portals = []
        self.__portal_cells = {}
        self.__spawn_point = spawn_point
        self.__cups = []
        self.__total_grains = total_grains
        self.__grains_spawned = 0
        self.__gravity = 1
        self.__grain_color = grain_color

    def get_spawn_point(self):
        return self.__spawn_point

    def get_grains(self):
        return self.__grains

    def get_walls(self):
        return self.__walls

    def add_wall(self, wall):
        self.__walls.append(wall)

    def get_portals(self):
        return self.__portals

    def add_portal(self, portal):
        self.__portals.append(portal)

    def register_portal_cell(self, x, y, portal):
        self.__portal_cells[(x, y)] = portal

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_gravity(self):
        return self.__gravity

    def invert_gravity(self):
        self.__gravity *= -1

    def get_grain_color(self):
        return self.__grain_color

    def get_cups(self):
        return self.__cups

    def add_cup(self, cup):
        self.__cups.append(cup)

    def cell_at(self, x, y):
        if not (0 <= x < self.__width and 0 <= y < self.__height):
            return "OUT_OF_BOUNDS"
        return self.__grid[y][x]

    def is_walkable(self, x, y):
        return self.cell_at(x, y) is None

    def place(self, obj, x, y):
        if 0 <= x < self.__width and 0 <= y < self.__height:
            self.__grid[y][x] = obj

    def remove(self, x, y):
        if 0 <= x < self.__width and 0 <= y < self.__height:
            self.__grid[y][x] = self.__portal_cells.get((x, y))

    def move_grain(self, grain, new_x, new_y):
        self.remove(grain.get_x(), grain.get_y())
        grain.set_position(new_x, new_y)
        self.place(grain, new_x, new_y)

    def remove_grain(self, grain):
        self.remove(grain.get_x(), grain.get_y())
        self.__grains.remove(grain)

    def can_spawn_grain(self):
        if self.__total_grains is None:
            return True
        return self.__grains_spawned < self.__total_grains

    def spawn_grain(self, color=None):
        if not self.can_spawn_grain():
            return None
        if color is None:
            color = self.__grain_color
        x, y = self.__spawn_point
        grain = Sugar(x, y, color)
        self.__grains.append(grain)
        self.place(grain, x, y)
        self.__grains_spawned += 1
        return grain

    def is_complete(self):
        return all(cup.is_full() for cup in self.__cups)