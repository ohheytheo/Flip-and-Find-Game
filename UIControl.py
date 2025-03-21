
from tkinter import Button, Tk, PhotoImage, Label, CENTER
from typing import Callable, Tuple

"""
UserButton class:
Button controller. Handles callbacks from the UI button using tkinter.Button

Note: We may want to rewrite how the callback works. Rather than allowing the user to 
define the callback from tkinter.Button, UserButton is always the callback which then calls the
user's callback. We need to define the callback signature too then
<https://stackoverflow.com/questions/37835179/how-can-i-specify-the-function-type-in-my-type-hints>
"""
class UserButton:
    def __init__(self, parentElement: Tk, text: str, imageFile: str = "", callback=None) -> None:
        #TODO: Annotate callback type
        if callback is None:
            # if the user didn't pass a callback, use the default method
            callback = self.DefaultHandler
        
        #TODO: Annotate callback type
        self.callback = callback # Function to be called when ui button is clicked

        self.image: PhotoImage

        if imageFile != "":
            self.image = PhotoImage(file=imageFile)
        else:
            self.image = PhotoImage(width=1, height=1)
        
        self.tkButton: Button = Button(
            master=parentElement, 
            command=self.callback, 
            text=text, 
            image=self.image, 
            compound=CENTER
        )
        
        self.tkButton.pack(ipadx=5, ipady=5)

        self.tkButton.update()

    def SetPosition(self, x: int, y: int) -> None:
        self.tkButton.place(x=x, y=y)
        self.tkButton.configure()
    
    def SetBorderWidth(self, borderWidth: int) -> None:
        self.tkButton.configure(borderwidth=borderWidth)
    
    def SetFont(self, fontName: str, fontSize: int) -> None:
        self.tkButton.configure(font=(fontName, fontSize))
    
    # Sets the button's image to newImage and returns the old image
    def SetImage(self, newImage: PhotoImage) -> PhotoImage:
        if newImage is not None:
            oldImage: PhotoImage = self.image

            self.image = newImage
            
            self.tkButton.configure(image=self.image)
            self.tkButton.update()

            return oldImage
        
        self.tkButton.configure()
        return self.image
    
    def GetPhotoImage(self) -> PhotoImage:
        return self.image
    
    def DefaultHandler(self) -> None:
        pass

class UIImage:
    def __init__(self, root: Tk, imageFile: str, x: int = -1, y: int = -1) -> None:
        self.image = PhotoImage(file=imageFile)
        self.element = Label(root, image=self.image)
        self.element.pack()
        
        self.element.update()

        if x >= 0 and y >= 0:
            self.SetPosition(x, y)
    
    def SetPosition(self, x: int, y: int) -> None:
        # Validate X and Y

        self.element.place(x=x, y=y)
        self.element.configure()

class UIText:
    # How should we deal with optional arguments? Make the code creating UIText create the Label?
    def __init__(self, root: Tk, text: str, padY: int = 0, x: int = -1, y: int = -1) -> None:
        self.label: Label = Label(root, text=text)
        self.label.pack(pady=padY)

        if x >= 0 and y >= 0:
            # We should check the width and height of the parent element too
            # but that requires the element being updating to ensure the values are correct
            # should UIText be updating the element?
            self.SetPosition(x, y)
        
        self.label.update()
    
    def SetPosition(self, x: int, y: int) -> None:
        # Validate X and Y

        self.label.place(x=x, y=y)
        self.label.configure()
        self.label.update()
    
    def SetFont(self, fontName: str, fontSize: int) -> None:
        self.label.configure(font=(fontName, fontSize))
