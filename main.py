from src.audio import Audio
from src.display import Display
from src.game_manager import GameManager

class Main:
    def __init__(self):
        audio = Audio()
        display = Display()
        GameManager(audio, display)

Main()