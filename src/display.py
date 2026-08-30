import pygame
import os

from src.settings import LOGICAL_SIZE, WALL_COLOR, OBSTACLE_COLOR, GRAIN_COLORS, GRAVITY_BUTTON_COLOR, RESET_BUTTON_COLOR, LEVEL_BUTTON_TEXT_COLOR

class Display: # Ne pas oublié le smooth scale 
    def __init__(self):
        self.__path = os.path.dirname(os.path.dirname(__file__))

        pygame.init()

        self.__surface = pygame.Surface(LOGICAL_SIZE)
        self.__screen = pygame.display.set_mode(LOGICAL_SIZE)

        pygame.display.set_caption("Sugar, Sugar")

        self.__load_pictures()

        self.__load_buttons()

    def __load_pictures(self):
        self.__home_background = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "home_background.png"))
        self.__level_background = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "level_background.png"))
        self.__setting_background = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "TEMP_setting_background.png"))
        self.__game_background = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "game_background.png"))

        self.__back_button = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "back_button.png"))
        self.__back_button_rect = self.__back_button.get_rect(topleft=(25, 25))
        self.__play_button = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "play_button.png"))
        self.__play_button_rect = self.__play_button.get_rect(topleft=(900, 200))
        self.__setting_button = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "setting_button.png"))
        self.__setting_button_rect = self.__setting_button.get_rect(topleft=(900, 300))

        self.__cup_image = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "cup.png"))
        self.__level_button_image = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "available_level_button.png"))
        self.__unavailable_level_button_image = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "unavailable_level_button.png"))
        self.__portal_images = {}

    def __load_buttons(self):
        self.__gravity_button_rect = pygame.Rect(1500, 25, 75, 50)
        self.__reset_button_rect = pygame.Rect(1500, 85, 75, 50)
        self.__button_font = pygame.font.SysFont(None, 24)
        self.__level_button_font = pygame.font.SysFont("kristenitc", 20)
        self.__button = {
            "back": self.__back_button_rect,
            "setting": self.__setting_button_rect,
            "level": self.__play_button_rect,
            "gravity": self.__gravity_button_rect,
            "reset": self.__reset_button_rect,
        }

    def get_surface(self):
        return self.__surface

    def get_button(self, name):
        return self.__button[name]

    def get_level_button_rects(self, level_ids):
        columns = 5
        spacing_x = 260
        spacing_y = 200
        start_x = 100
        start_y = 150

        rects = {}
        for index, level_id in enumerate(sorted(level_ids)):
            column = index % columns
            row = index // columns
            x = start_x + column * spacing_x
            y = start_y + row * spacing_y
            rects[level_id] = self.__level_button_image.get_rect(topleft=(x, y))
        return rects

    def draw_home(self):
        self.__surface.blit(self.__home_background, (0, 0))
        self.__surface.blit(self.__play_button, self.__play_button_rect)
        self.__surface.blit(self.__setting_button, self.__setting_button_rect)

    
    def draw_setting(self):
        self.__surface.blit(self.__setting_background, (0, 0))
        self.__surface.blit(self.__back_button, self.__back_button_rect)

    def draw_level(self, level_ids, unlocked_count):
        self.__surface.blit(self.__level_background, (0, 0))

        sorted_ids = sorted(level_ids)
        rects = self.get_level_button_rects(level_ids)

        for index, level_id in enumerate(sorted_ids):
            rect = rects[level_id]
            if index < unlocked_count:
                self.__surface.blit(self.__level_button_image, rect)
                self.__draw_level_button_label(level_id, rect)
            else:
                self.__surface.blit(self.__unavailable_level_button_image, rect)

        self.__surface.blit(self.__back_button, self.__back_button_rect)

    def __draw_level_button_label(self, level_id, rect):
        text_surface = self.__level_button_font.render(level_id, True, LEVEL_BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        self.__surface.blit(text_surface, text_rect)

    def draw_game(self, level):
        self.__surface.blit(self.__game_background, (0, 0))

        for wall in level.get_walls():
            self.__draw_wall(wall)

        for portal in level.get_portals():
            self.__draw_portal(portal)

        for cup in level.get_cups():
            self.__draw_cup(cup)

        for grain in level.get_grains():
            self.__draw_grain(grain)

        self.__draw_gravity_button(level)
        self.__draw_reset_button()
        self.__surface.blit(self.__back_button, self.__back_button_rect)

    def __draw_gravity_button(self, level):
        pygame.draw.rect(self.__surface, GRAVITY_BUTTON_COLOR, self.__gravity_button_rect)

        cx = self.__gravity_button_rect.centerx
        cy = self.__gravity_button_rect.centery
        arrow_color = (255, 255, 255)

        if level.get_gravity() == 1:
            points = [(cx - 10, cy - 8), (cx + 10, cy - 8), (cx, cy + 12)]  # flèche vers le bas
        else:
            points = [(cx - 10, cy + 8), (cx + 10, cy + 8), (cx, cy - 12)]  # flèche vers le haut

        pygame.draw.polygon(self.__surface, arrow_color, points)

    def __draw_reset_button(self):
        pygame.draw.rect(self.__surface, RESET_BUTTON_COLOR, self.__reset_button_rect)
        text_surface = self.__button_font.render("RESET", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.__reset_button_rect.center)
        self.__surface.blit(text_surface, text_rect)

    def __draw_wall(self, wall):
        shape = wall.get_shape()
        p = wall.get_params()
        if shape == "rect":
            pygame.draw.rect(self.__surface, OBSTACLE_COLOR, (p["x"], p["y"], p["width"], p["height"]))
        elif shape == "circle":
            pygame.draw.circle(self.__surface, OBSTACLE_COLOR, (p["x"], p["y"]), p["radius"])
        elif shape == "triangle":
            pygame.draw.polygon(self.__surface, OBSTACLE_COLOR, p["points"])
        elif shape == "line":
            pygame.draw.line(self.__surface, WALL_COLOR, (p["x1"], p["y1"]), (p["x2"], p["y2"]), p["thickness"])

    def __draw_cup(self, cup):
        rect = self.__cup_image.get_rect(topleft=(cup.get_x(), cup.get_y()))
        self.__surface.blit(self.__cup_image, rect)

    def __get_portal_image(self, color):
        if color not in self.__portal_images:
            path = os.path.join(self.__path, "assets", "pictures", f"{color}_portal.png")
            try:
                self.__portal_images[color] = pygame.image.load(path)
            except (pygame.error, FileNotFoundError):
                self.__portal_images[color] = None
        return self.__portal_images[color]

    def __draw_portal(self, portal):
        color = portal.get_output_color()
        image = self.__get_portal_image(color)

        rect = image.get_rect(topleft=(portal.get_x(), portal.get_y()))
        self.__surface.blit(image, rect)

    def __draw_grain(self, grain):
        color = GRAIN_COLORS.get(grain.get_color(), GRAIN_COLORS["white"])
        self.__surface.set_at((grain.get_x(), grain.get_y()), color)

    def render(self):
        self.__screen.blit(self.__surface, (0, 0))
        pygame.display.flip()