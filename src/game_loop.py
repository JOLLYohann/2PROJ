import pygame
import random

from src.cup import Cup
from src.wall import Wall
from src.portal import Portal
from src.level import load_level
from src.save import set_save
from src.settings import SPAWN_INTERVAL_FRAMES, FPS, WALL_THICKNESS

class GameLoop:
    def __init__(self, display, level_id, screen_manager):
        self.__display = display
        self.__level_id = level_id
        self.__level = load_level(level_id)
        self.__screen_manager = screen_manager

        self.__game_closed = False

        self.__clock = pygame.time.Clock()

        self.__game_finished = False
        self.__frame_count = 0
        self.__last_draw_pos = None

    def __click_coord(self):
        self.__screen_manager.poll_events()

        if self.__screen_manager.is_quit_requested():
            self.__game_finished = True
            self.__game_closed = True
            return

        if self.__screen_manager.clicked_button("back"):
            self.__game_finished = True
        elif self.__screen_manager.clicked_button("gravity"):
            self.__level.invert_gravity()
        elif self.__screen_manager.clicked_button("reset"):
            self.__reset_level()

    def __reset_level(self):
        self.__level = load_level(self.__level_id)
        self.__frame_count = 0
        self.__last_draw_pos = None

    def __spawn_tick(self):
        self.__frame_count += 1
        if self.__frame_count % SPAWN_INTERVAL_FRAMES == 0:
            self.__level.spawn_grain()

    def __handle_drawing(self):
        if not pygame.mouse.get_pressed()[0]:
            self.__last_draw_pos = None
            return

        current_pos = self.__display.screen_to_logical(pygame.mouse.get_pos())

        if self.__display.get_button("back").collidepoint(current_pos):
            self.__last_draw_pos = None
            return

        if self.__display.get_button("gravity").collidepoint(current_pos):
            self.__last_draw_pos = None
            return

        if self.__display.get_button("reset").collidepoint(current_pos):
            self.__last_draw_pos = None
            return

        if self.__last_draw_pos is not None:
            self.__add_wall_segment(self.__last_draw_pos, current_pos)

        self.__last_draw_pos = current_pos

    def __add_wall_segment(self, start, end):
        segment = Wall("line", {
            "x1": start[0], "y1": start[1],
            "x2": end[0], "y2": end[1],
            "thickness": WALL_THICKNESS,
        })
        self.__level.add_wall(segment)
        for (x, y) in segment.covered_cells():
            self.__level.place(segment, x, y)

    def game_loop(self):
        while not self.__game_finished:
            self.__click_coord()
            self.__handle_drawing()
            self.__spawn_tick()
            self.__update_physics()

            if self.__level.is_complete():
                set_save(self.__level_id)
                self.__game_finished = True

            self.__display.draw_game(self.__level)
            self.__display.render()
            self.__clock.tick(FPS)

        return [self.__game_closed]

    def __update_physics(self):
        for grain in list(self.__level.get_grains()):
            self.__update_grain(grain)

    def __update_grain(self, grain):
        x, y = grain.get_x(), grain.get_y()
        gravity = self.__level.get_gravity()
        target_y = y + gravity

        if target_y < 0 or target_y >= self.__level.get_height():
            target_y = self.__level.get_height() - 1 if target_y < 0 else 0

        candidates = []

        for dx in (0, -1, 1):
            target_x = x + dx

            if target_x < 0 or target_x >= self.__level.get_width():
                self.__level.remove_grain(grain)
                return

            cell = self.__level.cell_at(target_x, target_y)

            if cell is None:
                candidates.append((target_x, target_y))
            elif isinstance(cell, Cup):
                if cell.catch_grain(grain.get_color()):
                    self.__level.remove_grain(grain)
                    return
            elif isinstance(cell, Portal):
                grain.set_color(cell.get_output_color())
                candidates.append((target_x, target_y))

        if candidates:
            target_x, target_y = random.choice(candidates)
            self.__level.move_grain(grain, target_x, target_y)