import pygame
import os

class Audio:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.3)

        self.__path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "musics")

        self.__music_index = 0
        self.__music_list = ["Garden", "Overtaken", "Village"]
        self.__music_running = False

        self.__load_sounds()

    def __load_sounds(self):
        self.__music = os.path.join(self.__path, f"{self.__music_list[self.__music_index]}.mp3")

    def get_is_running(self):
        return self.__music_running

    def get_music(self):
        return self.__music_list[self.__music_index]

    def set_music(self, x):
        self.__music_index = (self.__music_index + x) % len(self.__music_list)
        self.__load_sounds()
        if self.__music_running:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.__music)
            pygame.mixer.music.play(-1)

    def play_music(self):
        if self.__music_running:
            pygame.mixer.music.stop()
            self.__music_running = False
        else:
            pygame.mixer.music.load(self.__music)
            pygame.mixer.music.play(-1)
            self.__music_running = True