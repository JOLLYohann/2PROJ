import pygame

from src.game_loop import GameLoop
from src.level import find_level
from src.save import load_save
from src.settings import FPS

class GameManager:
    def __init__(self, audio, display):
        self.__audio = audio
        self.__display = display

        self.__clock = pygame.time.Clock()

        self.__is_running = True
        self.__current_page = "homepage"

        self.__level_ids = sorted(find_level().keys())
        self.__selected_level_id = None

        self.__navigation()

    def __click_coord(self): # Plus tard -> faire un class ScreenManager dans screen_manager.py, à partager avec game_loop.py
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pos()
                if self.__current_page == "homepage":
                    if self.__display.get_button("level").collidepoint(mouse_click):
                        self.__current_page = "level"
                    elif self.__display.get_button("setting").collidepoint(mouse_click):
                        self.__current_page = "setting"
                elif self.__current_page == "setting":
                    if self.__display.get_button("back").collidepoint(mouse_click):
                        self.__current_page = "homepage"
                    elif self.__display.get_button("music_left").collidepoint(mouse_click):
                        self.__audio.set_music(-1)
                    elif self.__display.get_button("music_right").collidepoint(mouse_click):
                        self.__audio.set_music(1)
                    elif self.__display.get_button("music_toggle").collidepoint(mouse_click):
                        self.__audio.play_music()
                elif self.__current_page == "level":
                    if self.__display.get_button("back").collidepoint(mouse_click):
                        self.__current_page = "homepage"
                    else:
                        self.__handle_level_click(mouse_click)

    def __handle_level_click(self, mouse_click):
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
                game = GameLoop(self.__display, self.__selected_level_id)
                result = game.game_loop()
                self.__is_running = not result[0]

                self.__current_page = "level"

            self.__display.render()
            self.__clock.tick(FPS)