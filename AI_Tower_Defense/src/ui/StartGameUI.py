#from tkinter import
import tkinter as tk
import tkinter.ttk as tkk

WINDOW_SIZE = '700x500'
FONT_HEADER = ("Arial Bold", 30)
FONT_BODY = ("Arial", 15)
BTN_BG_COLOR = "blue"
BTN_FG_COLOR = "black"

class StartUpWindow():

    def __init__(self):

        #Window Setup
        window = tk.Tk()
        window.geometry(WINDOW_SIZE)
        window.title("AI Tower Defense")

        welcomeLabel = tk.Label(window, text="Welcome to: AI Tower Defense!", font=FONT_HEADER)
        welcomeLabel.grid(column=0, row=0)

        #Variables for different radio button groups
        manualOrAI = tk.IntVar()

        def manualRadioBtnSelected():
            print(f"Manual: {manualOrAI}")

        def aiRadioBtnSelected():
            print(f"AI:     {manualOrAI}")

        def hideElement(event):
            event.grid_remove()

        def showElement(event):
            event.grid()

        def startButtonClicked():
            print('Start button clicked')

        #Start Game Button
        startGameBtn = tk.Button(window, text="Start Game", command=startButtonClicked)
        startGameBtn.grid(column=0, row=10)

        #Radio Buttons Manual / AI
        manualRadioBtn = tk.Radiobutton(window, text="Play Game Manually", value=1,variable=manualOrAI, command=manualRadioBtnSelected, indicatoron=0)
        aiRadioBtn = tk.Radiobutton(window, text="Artifical Intelligence", value=2, variable=manualOrAI, command=aiRadioBtnSelected, indicatoron=0)
        manualRadioBtn.grid(column=0, row=1)
        aiRadioBtn.grid(column=0, row=2)

        #AI Settings (none)
        aiTypeCombo = tkk.Combobox(window)
        aiTypeCombo['values']= ("Genetic Algorithm", "Q-Learning","Deep Q-Learning")
        aiTypeCombo.current(1) #set the selected item
        aiTypeCombo.grid(column=0, row=6)




        window.mainloop()
