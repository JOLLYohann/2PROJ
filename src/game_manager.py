import pygame

from src.game_loop import GameLoop
from src.level import find_level
from src.save import load_save
from src.screen_manager import ScreenManager
from src.settings import FPS

class GameManager:
    def __init__(self, audio, display, screen_manager):
        self.__audio = audio
        self.__display = display
        self.__screen_manager = screen_manager

        self.__clock = pygame.time.Clock()

        self.__is_running = True
        self.__current_page = "homepage"

        self.__level_ids = sorted(find_level().keys())
        self.__selected_level_id = None

        self.__navigation()

    def __click_coord(self):
        self.__screen_manager.poll_events()

        if self.__screen_manager.is_quit_requested():
            self.__is_running = False
            return

        if self.__current_page == "homepage":
            if self.__screen_manager.clicked_button("level"):
                self.__current_page = "level"
            elif self.__screen_manager.clicked_button("setting"):
                self.__current_page = "setting"
        elif self.__current_page == "setting":
            if self.__screen_manager.clicked_button("back"):
                self.__current_page = "homepage"
            elif self.__screen_manager.clicked_button("music_left"):
                self.__audio.set_music(-1)
            elif self.__screen_manager.clicked_button("music_right"):
                self.__audio.set_music(1)
            elif self.__screen_manager.clicked_button("music_toggle"):
                self.__audio.play_music()
            elif self.__screen_manager.clicked_button("resolution_left"):
                self.__display.cycle_resolution(-1)
            elif self.__screen_manager.clicked_button("resolution_right"):
                self.__display.cycle_resolution(1)
        elif self.__current_page == "level":
            if self.__screen_manager.clicked_button("back"):
                self.__current_page = "homepage"
            else:
                self.__handle_level_click(self.__screen_manager.get_last_click())

    def __handle_level_click(self, mouse_click):
        if mouse_click is None:
            return

        player_level = load_save()["player"]["level"]
        level_buttons = self.__display.get_level_button_rects(self.__level_ids)

        for index, level_id in enumerate(self.__level_ids):
            if index >= player_level:
                continue

            if level_buttons[level_id].collidepoint(mouse_click):
                self.__selected_level_id = level_id
                self.__current_page = "game"
                return

    def __navigation(self):
        while self.__is_running:
            self.__click_coord()

            if self.__current_page == "homepage":
                self.__display.draw_home()
            elif self.__current_page == "setting":
                self.__display.draw_setting(self.__audio)
            elif self.__current_page == "level":
                player_level = load_save()["player"]["level"]
                self.__display.draw_level(self.__level_ids, player_level)
            elif self.__current_page == "game":
                game = GameLoop(self.__display, self.__selected_level_id, self.__screen_manager)
                result = game.game_loop()
                self.__is_running = not result[0]

                self.__current_page = "level"

            self.__display.render()
            self.__clock.tick(FPS)