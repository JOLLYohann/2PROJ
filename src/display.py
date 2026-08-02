import pygame
import os

class Display:
    def __init__(self):
        self.__path = os.path.dirname(os.path.dirname(__file__))

        pygame.init()
        self.__LOGICAL_SIZE = (1600, 900)

        self.__surface = pygame.Surface(self.__LOGICAL_SIZE)
        self.__screen = pygame.display.set_mode(self.__LOGICAL_SIZE)

        pygame.display.set_caption("Sugar, Sugar")

        self.__load_pictures()

    def __load_pictures(self):
        self.__background = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "background.jpg"))

        self.__back_button = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "back_button.jpg"))
        self.__back_button_rect = self.__back_button.get_rect(topleft=(50, 50))
        self.__play_button = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "play_button.jpg"))
        self.__play_button_rect = self.__play_button.get_rect(topleft=(900, 200))
        self.__setting_button = pygame.image.load(os.path.join(self.__path, "assets", "pictures", "setting_button.jpg"))
        self.__setting_button_rect = self.__setting_button.get_rect(topleft=(900, 300))

    def get_surface(self):
        return self.__surface

    def draw_home(self):
        self.__surface.blit(self.__background, (0, 0))
        self.__surface.blit(self.__play_button, self.__play_button_rect)
        self.__surface.blit(self.__setting_button, self.__setting_button_rect)

    def draw_level(self):
            self.__surface.blit(self.__background, (0, 0))
            self.__surface.blit(self.__back_button, self.__back_button_rect)

    def draw_setting(self):
            self.__surface.blit(self.__background, (0, 0))
            self.__surface.blit(self.__back_button, self.__back_button_rect)

    def render(self):
        self.__screen.blit(self.__surface, (0, 0))
        pygame.display.flip()