import pygame
import os

from src.settings import LOGICAL_SIZE, AVAILABLE_RESOLUTIONS, WALL_COLOR, OBSTACLE_COLOR, GRAIN_COLORS, GRAVITY_BUTTON_COLOR, RESET_BUTTON_COLOR, TEXT_COLOR

class Display:
    def __init__(self):
        self.__path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "pictures")

        pygame.init()

        self.__surface = pygame.Surface(LOGICAL_SIZE)

        self.__resolution_index = AVAILABLE_RESOLUTIONS.index(LOGICAL_SIZE)
        self.__screen = None
        self.__apply_resolution()

        pygame.display.set_caption("Sugar, Sugar")

        self.__load_pictures()

        self.__load_buttons()

    def __apply_resolution(self):
        if self.__resolution_index == len(AVAILABLE_RESOLUTIONS):
            self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.__screen = pygame.display.set_mode(AVAILABLE_RESOLUTIONS[self.__resolution_index])

    def cycle_resolution(self, direction):
        """direction = -1 ou 1. Le dernier cran au-delà des résolutions listées est le plein écran."""
        total_options = len(AVAILABLE_RESOLUTIONS) + 1
        self.__resolution_index = (self.__resolution_index + direction) % total_options
        self.__apply_resolution()

    def get_resolution_label(self):
        if self.__resolution_index == len(AVAILABLE_RESOLUTIONS):
            return "Fullscreen"
        width, height = AVAILABLE_RESOLUTIONS[self.__resolution_index]
        return f"{width}x{height}"

    def __compute_scale_and_offset(self):
        screen_width, screen_height = self.__screen.get_size()
        logical_width, logical_height = LOGICAL_SIZE

        scale = min(screen_width / logical_width, screen_height / logical_height)
        scaled_width = int(logical_width * scale)
        scaled_height = int(logical_height * scale)

        offset_x = (screen_width - scaled_width) // 2
        offset_y = (screen_height - scaled_height) // 2

        return scale, offset_x, offset_y

    def screen_to_logical(self, pos):
        """Convertit une position souris (espace fenêtre réelle) en coordonnées logiques (1600x900)."""
        scale, offset_x, offset_y = self.__compute_scale_and_offset()
        x, y = pos
        return (int((x - offset_x) / scale), int((y - offset_y) / scale))

    def __load_pictures(self):
        self.__home_background = pygame.image.load(os.path.join(self.__path, "backgrounds", "home_background.png"))
        self.__level_background = pygame.image.load(os.path.join(self.__path, "backgrounds", "level_background.png"))
        self.__setting_background = pygame.image.load(os.path.join(self.__path, "backgrounds", "setting_background.png"))
        self.__game_background = pygame.image.load(os.path.join(self.__path, "backgrounds", "game_background.png"))

        self.__back_button = pygame.image.load(os.path.join(self.__path, "buttons", "back_button.png"))
        self.__back_button_rect = self.__back_button.get_rect(topleft=(25, 25))
        self.__play_button = pygame.image.load(os.path.join(self.__path, "buttons", "play_button.png"))
        self.__play_button_rect = self.__play_button.get_rect(topleft=(900, 200))
        self.__setting_button = pygame.image.load(os.path.join(self.__path, "buttons", "setting_button.png"))
        self.__setting_button_rect = self.__setting_button.get_rect(topleft=(900, 300))
        self.__level_button_image = pygame.image.load(os.path.join(self.__path, "buttons", "available_level_button.png"))
        self.__lock_level_button_image = pygame.image.load(os.path.join(self.__path, "buttons", "unavailable_level_button.png"))
        self.__music_on_button = pygame.image.load(os.path.join(self.__path, "buttons", "music_on_button.png"))
        self.__music_off_button = pygame.image.load(os.path.join(self.__path, "buttons", "music_off_button.png"))
        self.__music_button_rect = self.__music_on_button.get_rect(topleft=(1500, 50))
        self.__left_arrow_music = pygame.image.load(os.path.join(self.__path, "buttons", "left_arrow_button.png"))
        self.__left_arrow_music_rect = self.__left_arrow_music.get_rect(topleft=(50, 300))
        self.__right_arrow_music = pygame.image.load(os.path.join(self.__path, "buttons", "right_arrow_button.png"))
        self.__right_arrow_music_rect = self.__right_arrow_music.get_rect(topleft=(450, 300))
        self.__left_arrow_resolution = pygame.image.load(os.path.join(self.__path, "buttons", "left_arrow_button.png"))
        self.__left_arrow_resolution_rect = self.__left_arrow_resolution.get_rect(topleft=(50, 600))
        self.__right_arrow_resolution = pygame.image.load(os.path.join(self.__path, "buttons", "right_arrow_button.png"))
        self.__right_arrow_resolution_rect = self.__right_arrow_resolution.get_rect(topleft=(450, 600))
        self.__buffer = pygame.image.load(os.path.join(self.__path, "buttons", "buffer.png"))

        self.__cup_image = pygame.image.load(os.path.join(self.__path, "levels", "cup.png"))
        self.__portal_images = {
            "red": pygame.image.load(os.path.join(self.__path, "levels", "red_portal.png")),
            "blue": pygame.image.load(os.path.join(self.__path, "levels", "blue_portal.png")),
            "white": pygame.image.load(os.path.join(self.__path, "levels", "white_portal.png")),
        }

    def __load_buttons(self):
        self.__gravity_button_rect = pygame.Rect(1500, 25, 75, 50)
        self.__reset_button_rect = pygame.Rect(1500, 85, 75, 50)
        self.__font = pygame.font.SysFont("kristenitc", 20)
        self.__button = {
            "back": self.__back_button_rect,
            "setting": self.__setting_button_rect,
            "level": self.__play_button_rect,
            "gravity": self.__gravity_button_rect,
            "reset": self.__reset_button_rect,
            "music_toggle": self.__music_button_rect,
            "music_left": self.__left_arrow_music_rect,
            "music_right": self.__right_arrow_music_rect,
            "resolution_left": self.__left_arrow_resolution_rect,
            "resolution_right": self.__right_arrow_resolution_rect,
        }

    def get_surface(self):
        return self.__surface

    def get_button(self, name):
        return self.__button[name]

    def get_level_button_rects(self, level_ids):
        columns = 5
        spacing_x = 300
        spacing_y = 300
        start_x = 150
        start_y = 250

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

    def draw_setting(self, audio):
        self.__surface.blit(self.__setting_background, (0, 0))

        if audio.get_is_running():
            self.__surface.blit(self.__music_on_button, self.__music_button_rect)
        else:
            self.__surface.blit(self.__music_off_button, self.__music_button_rect)

        self.__surface.blit(self.__left_arrow_music, self.__left_arrow_music_rect)
        self.__surface.blit(self.__right_arrow_music, self.__right_arrow_music_rect)
        self.__surface.blit(self.__buffer, (200, 300))
        music_text = self.__font.render(audio.get_music(), True, TEXT_COLOR)
        music_rect = music_text.get_rect(center=(300, 350))
        self.__surface.blit(music_text, music_rect)

        self.__surface.blit(self.__left_arrow_resolution, self.__left_arrow_resolution_rect)
        self.__surface.blit(self.__right_arrow_resolution, self.__right_arrow_resolution_rect)
        self.__surface.blit(self.__buffer, (200, 600))
        resolution_text = self.__font.render(self.get_resolution_label(), True, TEXT_COLOR)
        resolution_rect = resolution_text.get_rect(center=(300, 650))
        self.__surface.blit(resolution_text, resolution_rect)

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
                self.__surface.blit(self.__lock_level_button_image, rect)

        self.__surface.blit(self.__back_button, self.__back_button_rect)

    def __draw_level_button_label(self, level_id, rect):
        text_surface = self.__font.render(level_id, True, TEXT_COLOR)
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
        text_surface = self.__font.render("RESET", True, (255, 255, 255))
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
        self.__draw_cup_remaining(cup, rect)

    def __draw_cup_remaining(self, cup, rect):
        requirements = cup.get_requirements()
        filled = cup.get_filled()

        text_y = rect.bottom + 4
        for color, amount in requirements.items():
            remaining = max(0, amount - filled[color])
            text_color = GRAIN_COLORS.get(color, GRAIN_COLORS["white"])
            text_surface = self.__font.render(str(remaining), True, text_color)
            text_rect = text_surface.get_rect(midtop=(rect.centerx, text_y))
            self.__surface.blit(text_surface, text_rect)
            text_y += text_surface.get_height() + 2

    def __draw_portal(self, portal):
        image = self.__portal_images[portal.get_output_color()]
        rect = image.get_rect(topleft=(portal.get_x(), portal.get_y()))
        self.__surface.blit(image, rect)

    def __draw_grain(self, grain):
        color = GRAIN_COLORS.get(grain.get_color(), GRAIN_COLORS["white"])
        self.__surface.set_at((grain.get_x(), grain.get_y()), color)

    def render(self):
        scale, offset_x, offset_y = self.__compute_scale_and_offset()
        scaled_size = (int(LOGICAL_SIZE[0] * scale), int(LOGICAL_SIZE[1] * scale))
        scaled_surface = pygame.transform.scale(self.__surface, scaled_size)

        self.__screen.fill((0, 0, 0))  # bandes noires si le ratio ne correspond pas exactement
        self.__screen.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.flip()