from src.audio import Audio
from src.display import Display
from src.screen_manager import ScreenManager
from src.game_manager import GameManager

class Main:
    def __init__(self):
        audio = Audio()
        display = Display()
        screen_manager = ScreenManager(display)
        GameManager(audio, display, screen_manager)

Main()