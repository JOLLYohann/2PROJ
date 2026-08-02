import pygame

class GameManager:
    def __init__(self, audio, display):
        self.__audio = audio
        self.__display = display

        self.__clock = pygame.time.Clock()

        self.__is_running = True
        self.__current_page = "home"
        
        self.__navigation()

    def __navigation(self):
        while self.__is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__is_running = False

            if self.__current_page == "home":
                self.__display.draw_home()
            elif self.__current_page == "levels":
                pass

            self.__display.render()
            self.__clock.tick(30)  # 30 FPS