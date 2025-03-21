class Score:
    def __init__(self) -> None:
        self.matches: int = 0
        self.moves: int = 0
        self.accuracy: float = 0.0
    
    def UpdateMoves(self) -> None:
        self.moves += 1

    def UpdateMatches(self) -> None:
        self.matches += 1
        self.CalcAccuracy()

    def CalcAccuracy(self) -> None:
        if self.moves == 0:
            return
        else:
            self.accuracy = (self.matches / self.moves)
