import random
from typing import List, Tuple
from enum import Enum

class Card:
    def __init__(self, id: int) -> None:
        # This makes every two cards have the same number (used to match up pictures to cards later) 
        self._matchID: int = id // 2

        self._cardID: int = id

    def GetID(self) -> int:
        return self._cardID

    def GetMatchID(self) -> int:
        return self._matchID

class CardDeck:
    _MAX_CARDS: int = 36
    
    # This function creates 36 instances of cards and stores them for the entire project
    def __init__(self) -> None:
        from main import ReadCardImages
        self._deck: List[Card] = [None] * self._MAX_CARDS

        self.imagePaths: List[str] = ReadCardImages()

        for i in range(0, self._MAX_CARDS, 1):
            self._deck[i] = Card(i)

    def GetCard(self, index: int) -> Card|None:
        if index < 0 or index >= self._MAX_CARDS:
            return None
        
        return self._deck[index]
    
    def ShufflePictures(self) -> None:
        random.shuffle(self.imagePaths)

    def GetDeck(self) -> List[Card]:
        return self._deck
    
    def GetImageName(self, index: int) -> str:
        return self.imagePaths[index]

class CardList:
    def __init__(self, width: int, height: int, deck: CardDeck) -> None:

        if self.CheckValidity(width, height) == False:
            # If the total cards is odd, add 1 more
            print("Invalid number of cards. Adding 1")
            width += 1
        
        self.width: int = width
        self.height: int = height
        
        self.totalCards: int = self.width * self.height

        self.cards: List[Card] = [None] * self.totalCards
        
        deckIndex: int = 0
        for i in range(0, self.width, 1):
            for j in range(0, self.height, 1):
                self.cards[i * self.height + j] = deck.GetCard(i * self.height + j)
                deckIndex += 1
    
    def __eq__(self, other) -> bool:
        if isinstance(other, CardList):
            if (self.width == other.width and self.height == other.height and self.cards == other.cards):
                return True
        
        return False
    
    def GetWidth(self) -> int:
        return self.width
    
    def GetHeight(self) -> int:
        return self.height

    def GetCardCount(self) -> int:
        return self.totalCards

    def Shuffle(self) -> None:
        random.shuffle(self.cards)

    def CheckValidity(self, width: int, height: int) -> bool:
        # Returns true if (width * height) % 2 is 0 (divisible by two)
        return ((width * height) % 2) == 0
    
    def GetCard(self, x: int, y: int) -> Card:
        index: int = x * self.height + y
        assert index < len(self.cards)
        return self.cards[index]
