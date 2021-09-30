from tkinter import *
import tkinter as tk

class Acceueil(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("350x190+500+200")
        self.title("Fichier DAT")
        self.resizable(0, 0)
        self.config(bg="#F7F9F9")
        label = Label(self, text="Le fichier a été bien exporté \n Voulez-Vous l'ouvrir maintenant?", bg="#F7F9F9", font=("Helvetica", 12)).place(x=50, y=30)
        btn1 = Button(self, text="oui", command=self.oui, font=("Times New Roman", 11),
                         bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA",
                         activeforeground="#000000").place(x=120, y=100)
        btn2 = Button(self, text="non",  command=self.non, font=("Times New Roman", 11),
                         fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02",
                         activeforeground="#000000").place(x=190, y=100)

    def oui(self):
        print("oui")
        self.destroy()

    def non(self):
        self.destroy()

'''if __name__ == "__main__":
    app = Acceueil()
    app.mainloop()'''