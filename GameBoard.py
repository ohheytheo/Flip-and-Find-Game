from Card import CardList, Card, CardDeck
from UIControl import UserButton
from typing import List
from tkinter import PhotoImage, Label
import time
from Screens.PlayScreen import PlayScreen
from Score import Score


# Represents the button and image for a Card
class PhysicalCard:
    def __init__(self, cardMatchId: int, deck: CardDeck, parentElement, gameBoard) -> None:
        self.gameBoard: GameBoard = gameBoard
        self._cardMatchId: int = cardMatchId
        self.shown: bool = False
        self.matched: bool = False  # Whether we have matched this card with the other

        # Image the user is matching to others
        self.cardImageFile: str = deck.GetImageName(self._cardMatchId)
        self.cardImage: PhotoImage = PhotoImage(file=self.cardImageFile)

        self.blankImage: PhotoImage = PhotoImage()

        # Debug Cards (with answers)
        # self.button: UserButton = UserButton(parentElement, f"Match ID: {cardMatchId}", imageFile="", callback=self.OnClick)

        # Final Cards (actual ones)
        self.button: UserButton = UserButton(parentElement, "", imageFile="", callback=self.OnClick)

    def OnClick(self) -> None:
        if self.gameBoard.selectionPaused == False and self.gameBoard.cardsSelected != 2:
            # Only update when the game board isn't paused and there aren't 2 cards selected
            self.shown = True
            self.button.SetImage(self.cardImage)

            self.gameBoard.Selection(self)

    def SetToDefaultImage(self) -> None:
        self.button.SetImage(self.blankImage)

    def GetMatchID(self) -> int:
        return self._cardMatchId

    def SetMatched(self) -> None:
        self.matched = True


class GameBoard:
    def __init__(self, width: int, height: int, cardDeck: CardDeck, cardParentElement, activeGame: PlayScreen, score: Score) -> None:
        cardDeck.ShufflePictures()
        self.cardList = CardList(width, height, cardDeck)
        self.score: Score = score

        # Int in seconds, the time for freeze after incorrect match
        self.selectionTimer: int = 1

        self.selectionPaused: bool = False

        self.firstFlippedCard: PhysicalCard = None
        self.secondFlippedCard: PhysicalCard = None

        self.cardsSelected: int = 0

        self.matchedPairCount: int = 0

        self.cardList.Shuffle()

        self._width: int = self.cardList.GetWidth()
        self._height: int = self.cardList.GetHeight()

        self.activeGame: PlayScreen = activeGame

        # (x, y)
        self.cardButtons: List[List[PhysicalCard]] = []

        for i in range(0, self._width):  # width is the number of columns
            self.cardButtons.append([None] * self._height)
            for j in range(0, self._height):  # height is the number of rows
                self.cardButtons[i][j] = PhysicalCard(
                    self.cardList.GetCard(i, j).GetMatchID(),
                    cardDeck,
                    cardParentElement,
                    self
                )
                self.cardButtons[i][j].button.tkButton.grid(row=j, column=i, padx=40, pady=20)
                self.cardButtons[i][j].button.tkButton.configure(width=150 // 2, height=210 // 2)
                self.cardButtons[i][j].button.tkButton.update()

    def GetWidth(self) -> int:
        return self._width

    def GetHeight(self) -> int:
        return self._height

    def Selection(self, card: PhysicalCard) -> None:
        if card.matched == True or self.selectionPaused == True:
            # If the new card is matched or the selection is paused
            # don't add the card to the selected cards
            return

        if self.firstFlippedCard == None:
            # Add the first selected card
            self.firstFlippedCard = card
            self.cardsSelected = 1
        elif card != self.firstFlippedCard:
            # Add the second selected card as long as it isn't the first card
            self.secondFlippedCard = card
            self.cardsSelected = 2
            self.CheckMatch()  # Check the match when we have 2 unique card objects

    def CheckMatch(self) -> bool:
        cardsMatch: bool = self.firstFlippedCard.GetMatchID() == self.secondFlippedCard.GetMatchID()

        if cardsMatch == True:
            # If the cards have the same match id
            # set both to matched
            self.firstFlippedCard.SetMatched()
            self.secondFlippedCard.SetMatched()

            self.matchedPairCount += 1

            # Update score
            self.score.UpdateMatches()

            if self.matchedPairCount == ((self._width * self._height) / 2):
                self.activeGame.GameOver()
        else:
            # otherwise, set them to the default image
            # we need to wait to prevent the 2nd image from resetting immediately without
            # showing the user

            self.selectionPaused = True
            time.sleep(self.selectionTimer)
            self.selectionPaused = False
            self.firstFlippedCard.SetToDefaultImage()
            self.secondFlippedCard.SetToDefaultImage()

        self.score.UpdateMoves()

        self.cardsSelected = 0
        self.firstFlippedCard = None
        self.secondFlippedCard = None

        return cardsMatch
