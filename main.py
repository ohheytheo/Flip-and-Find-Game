from Game import MemoryGameApp
import os
from typing import List

# Gets the path of a filename relative to the source directory
def GetFullAssetFileName(fileName: str) -> str:
    mainDir = os.path.dirname(__file__).replace("\\", "/")
    return f"{mainDir}/assets/{fileName}"

def ReadCardImages() -> List[str]:
    resultFilepaths: List[str] = []

    imagePath = GetFullAssetFileName("cards/")

    for filename in os.listdir(imagePath):
        resultFilepaths.append(f"{imagePath}{filename}")
    
    return resultFilepaths

def main() -> None:
    game: MemoryGameApp = MemoryGameApp()

    game.Run()

if __name__ == "__main__":
    main()