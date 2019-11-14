#from tkinter import
import tkinter as tk
import tkinter.ttk as tkk

WINDOW_SIZE = '350x250'
FONT_HEADER = ("Arial Bold", 20)
FONT_BODY = ("Arial", 15)
BTN_BG_COLOR = "blue"
BTN_FG_COLOR = "black"

class StartUpWindow():

    def __init__(self):

        #Window Setup
        window = tk.Tk()
        window.geometry(WINDOW_SIZE)
        window.title("AI Tower Defense")

        welcomeLabel = tk.Label(window, text="== AI Tower Defense ==", font=FONT_HEADER)
        welcomeLabel.grid(column=0, row=0, pady=5, padx=10)

        #UI Elements
        aiTypeCombo = tkk.Combobox(window, state="readonly")

        #Variables for different radio button groups
        manualOrAI = tk.IntVar()

        def manualRadioBtnSelected():
            hideElement(aiTypeCombo)

        def aiRadioBtnSelected():
            showElement(aiTypeCombo)

        def hideElement(event):
            event.grid_remove()

        def showElement(event):
            event.grid()

        def startButtonClicked():
            print('Start button clicked')

        #Start Game Button
        startGameBtn = tk.Button(window, text="Start Game", command=startButtonClicked)
        startGameBtn.grid(column=0, row=10, padx=10, pady=10)

        #Radio Buttons Manual / AI
        manualRadioBtn = tk.Radiobutton(window, text="Play Game Manually", value=1,variable=manualOrAI, command=manualRadioBtnSelected)
        aiRadioBtn = tk.Radiobutton(window, text="Artifical Intelligence", value=2, variable=manualOrAI, command=aiRadioBtnSelected)
        manualRadioBtn.grid(column=0, row=1)
        aiRadioBtn.grid(column=0, row=2, pady=10)

        #AI Settings (none)
        aiTypeCombo['values']= ("Genetic Algorithm", "Q-Learning","Deep Q-Learning")
        aiTypeCombo.current(1) #set the selected item
        aiTypeCombo.grid(column=0, row=6, pady=10)
        hideElement(aiTypeCombo)




        window.mainloop()
