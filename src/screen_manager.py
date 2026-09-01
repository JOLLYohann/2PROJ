import pygame


class ScreenManager:
    def __init__(self, display):
        self.__display = display
        self.__quit_requested = False
        self.__last_click = None

    def poll_events(self):
        self.__last_click = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit_requested = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__last_click = pygame.mouse.get_pos()

    def is_quit_requested(self):
        return self.__quit_requested

    def get_last_click(self):
        return self.__last_click

    def clicked_button(self, name):
        if self.__last_click is None:
            return False
        return self.__display.get_button(name).collidepoint(self.__last_click)