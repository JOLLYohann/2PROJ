import pygame
import os

from src.settings import LOGICAL_SIZE, WALL_COLOR, CUP_COLOR, GRAIN_COLORS, GRAVITY_BUTTON_COLOR, RESET_BUTTON_COLOR

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
        self.__level_background = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "TEMP_level_background.png"))
        self.__setting_background = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "TEMP_setting_background.png"))
        self.__game_background = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "TEMP_game_background.png"))

        self.__back_button = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "back_button.png"))
        self.__back_button_rect = self.__back_button.get_rect(topleft=(25, 25))
        self.__play_button = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "play_button.png"))
        self.__play_button_rect = self.__play_button.get_rect(topleft=(900, 200))
        self.__setting_button = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "setting_button.png"))
        self.__setting_button_rect = self.__setting_button.get_rect(topleft=(900, 300))

    def __load_buttons(self):
        self.__gravity_button_rect = pygame.Rect(1500, 25, 75, 50)
        self.__reset_button_rect = pygame.Rect(1500, 85, 75, 50)
        self.__button_font = pygame.font.SysFont(None, 24)
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

    def draw_home(self):
        self.__surface.blit(self.__home_background, (0, 0))
        self.__surface.blit(self.__play_button, self.__play_button_rect)
        self.__surface.blit(self.__setting_button, self.__setting_button_rect)

    
    def draw_setting(self):
        self.__surface.blit(self.__setting_background, (0, 0))
        self.__surface.blit(self.__back_button, self.__back_button_rect)

    def draw_level(self):
        self.__surface.blit(self.__level_background, (0, 0))
        self.__surface.blit(self.__back_button, self.__back_button_rect)

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
            pygame.draw.rect(self.__surface, WALL_COLOR, (p["x"], p["y"], p["width"], p["height"]))
        elif shape == "circle":
            pygame.draw.circle(self.__surface, WALL_COLOR, (p["x"], p["y"]), p["radius"])
        elif shape == "triangle":
            pygame.draw.polygon(self.__surface, WALL_COLOR, p["points"])
        elif shape == "line":
            pygame.draw.line(self.__surface, WALL_COLOR, (p["x1"], p["y1"]), (p["x2"], p["y2"]), p["thickness"])

    def __draw_cup(self, cup):
        pygame.draw.rect(self.__surface, CUP_COLOR, (cup.get_x(), cup.get_y(), cup.get_size(), cup.get_size()))

    def __draw_portal(self, portal):
        rect = (portal.get_x(), portal.get_y(), portal.get_size(), portal.get_size())
        fill_color = GRAIN_COLORS.get(portal.get_output_color(), GRAIN_COLORS["white"])
        pygame.draw.rect(self.__surface, fill_color, rect)
        pygame.draw.rect(self.__surface, (0, 0, 0), rect, 2)

    def __draw_grain(self, grain):
        color = GRAIN_COLORS.get(grain.get_color(), GRAIN_COLORS["white"])
        self.__surface.set_at((grain.get_x(), grain.get_y()), color)

    def render(self):
        self.__screen.blit(self.__surface, (0, 0))
        pygame.display.flip()