import pygame

from src.game_loop import GameLoop

class GameManager:
    def __init__(self, audio, display):
        self.__audio = audio
        self.__display = display

        self.__clock = pygame.time.Clock()

        self.__is_running = True
        self.__current_page = "homepage"
        
        self.__navigation()

    def __click_coord(self):
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
                elif self.__current_page == "level":
                    if self.__display.get_button("back").collidepoint(mouse_click):
                        self.__current_page = "homepage"
                    else :
                        self.__current_page = "game"
                elif self.__current_page == "game":
                    if self.__display.get_button("back").collidepoint(mouse_click):
                        self.__current_page = "level"

    def __navigation(self):
        while self.__is_running:
            self.__click_coord()

            if self.__current_page == "homepage":
                self.__display.draw_home()
            elif self.__current_page == "setting":
                self.__display.draw_setting()
            elif self.__current_page == "level":
                self.__display.draw_level()
            elif self.__current_page == "game":
                game = GameLoop(self.__display)
                result = game.game_loop()
                self.__is_running = not result[0]

                self.__current_page = "level"

            self.__display.render()
            self.__clock.tick(30)  # 30 FPS