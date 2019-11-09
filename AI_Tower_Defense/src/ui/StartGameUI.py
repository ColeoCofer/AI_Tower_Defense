from tkinter import *

WINDOW_SIZE = '700x500'
FONT_HEADER = ("Arial Bold", 30)
FONT_BODY = ("Arial", 15)
BTN_BG_COLOR = "grey"
BTN_FG_COLOR = "BLACK"

class StartUpWindow():

    def __init__(self):

        #Window Setup
        window = Tk()
        window.geometry(WINDOW_SIZE)
        window.title("AI Tower Defense")

        welcomeLabel = Label(window, text="Welcome to: AI Tower Defense!", font=FONT_HEADER)
        welcomeLabel.grid(column=0, row=0)

        def manualRadioBtnSelected():
            print("Manual")

        def aiRadioBtnSelected():
            print("AI ")

        #Radio Buttons Manual / AI
        manualRadioBtn = Radiobutton(window, text="Play Game Manually", value=1, command=manualRadioBtnSelected)
        aiRadioBtn = Radiobutton(window, text="Artifical Intelligence", value=2, command=aiRadioBtnSelected)
        manualRadioBtn.grid(column=0, row=1)
        aiRadioBtn.grid(column=0, row=2)

        window.mainloop()

    #Wire button up like
    #btn = Button(window, text="", command=clicked)
    def clicked():
        #self.label.configure(text="Button clicked!")
        print("Button clicked!")
