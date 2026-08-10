import pygame

class GameLoop:
    def __init__(self, display):
        self.__display = display

        self.__game_closed = False

        self.__clock = pygame.time.Clock()

        self.__game_finished = False

    def __click_coord(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__game_finished = True
                    self.__game_closed = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = pygame.mouse.get_pos()
                    if self.__display.get_button("back").collidepoint(mouse_click):
                        self.__game_finished = True

    def game_loop(self):
        while not self.__game_finished:
            self.__click_coord()
            # update_physics()

            self.__display.draw_game()
            self.__display.render()
            self.__clock.tick(30)

        return [self.__game_closed]