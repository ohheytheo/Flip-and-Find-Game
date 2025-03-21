from tkinter import Tk
from UIControl import UserButton
from Screens.Screen import Screen
from Screens.TitleScreen import TitleScreen
from Screens.GameOverScreen import GameOverScreen
from Card import CardDeck, CardList
from Gamemodes.ZenMode import ZenMode
from Gamemodes.NormalMode import NormalMode
from Gamemodes.ChallengeMode import ChallengeMode
from enum import Enum
from typing import List

class GameMode(Enum):
    NONE        = -1
    TITLE       = 0
    ZEN         = 1
    NORMAL      = 2
    CHALLENGING = 3
    GAMEOVER    = 4

"""
Game main controller class
"""
class MemoryGameApp:
    def __init__(self) -> None:
        self.windowWidth: int = 0
        self.windowHeight: int = 0

        self.active: bool = False

        self.gameMode: GameMode = GameMode.NONE

        self.activeScreen: Screen|None = None

        self.root: Tk = Tk("Flip and Find")
        self.root.state('zoomed')
        self.root.title("Flip and Find")

        self.root.update()

        self.UpdateWindowSize()

        # Escape minimizes the size of the window
        # self.BindKey("<Escape>", False, lambda event: self.root.state('normal'))
        self.BindKey("<Escape>", False, self.MinimizeWindow)

        # F11 makes the window fullscreen
        # self.BindKey("<F11>", False, lambda event: self.root.state('zoom'))
        self.BindKey("<F11>", False, self.SetFullScreen)

        self.BindKey("<Return>", False)

        # Use for positioning UI elements
        # self.BindKey("<Button-1>", lambda event: print(event))

        # activeScreen will change as we play
        self.activeScreen = TitleScreen(self.root, self)

        # Creates the deck of cards used in the game
        self.cardDeck: CardDeck = CardDeck()
    
    def UpdateWindowSize(self) -> None:
        self.root.update()
        self.windowWidth = self.root.winfo_width()
        self.windowHeight = self.root.winfo_width()

        if self.activeScreen is not None:
            self.activeScreen.UpdateWindowSize()
    
    def SetFullScreen(self, event) -> None:
        self.root.state('zoom')
        self.root.update()
        self.UpdateWindowSize()
    
    def MinimizeWindow(self, event) -> None:
        self.root.state('normal')
        self.root.update()
        self.UpdateWindowSize()
    
    # Bind a key to a callback function
    # Allows executing code when the user clicks a button
    # If addEvent is True, the callback will be added to the list of callback to be called
    # by tkinter when the event occurs
    # If addEvent is False, the callback will replace all existing callbacks for the event
    # Return True if the event was added successfull otherwise False
    def BindKey(self, keyName: str, addEvent: bool, callback=None) -> bool:
        if callback is None:
            callback = self.DefaultKeyHandler
        
        self.root.bind(keyName, callback, '+' if addEvent else '')

        return True
    
    def UnbindKey(self, keyName: str) -> None:
        self.root.unbind(keyName)
    
    def DefaultKeyHandler(self, event) -> None:
        print(event)
    
    def ChangeGameMode(self, newGamemode: GameMode) -> None:
        print("Changing game mode from {0} to {1}".format(self.gameMode, newGamemode))
        self.gameMode = newGamemode

        if newGamemode == GameMode.ZEN:
            self.DestroyActiveScreen()
            self.activeScreen = ZenMode(self.root, self)
        elif newGamemode == GameMode.NORMAL:
            self.DestroyActiveScreen()
            self.activeScreen = NormalMode(self.root, self)
        elif newGamemode == GameMode.CHALLENGING:
            self.DestroyActiveScreen()
            self.activeScreen = ChallengeMode(self.root, self)
        elif newGamemode == GameMode.TITLE:
            self.DestroyActiveScreen()
            self.activeScreen = TitleScreen(self.root, self)
        elif newGamemode == GameMode.GAMEOVER:
            self.DestroyActiveScreen()
            self.activeScreen = GameOverScreen(self.root, self)

    def DestroyActiveScreen(self) -> None:
        if self.activeScreen is not None:
            self.activeScreen.Deinit()
            self.activeScreen = None

    # Main loop
    def Run(self) -> None:
        self.active = True
        self.root.mainloop()
        self.active = False
