import tkinter as tk
from tkinter import *
import sys
from AdminAPP import ExportDat

class Deconnecte(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EpGis")
        self.geometry("300x150+500+220")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.config(bg="#F7F9F9")

        lbl = Label(self, text="Voulez vous vraiment quiter \n l'application?", font=("Times New Roman", 14), bg="#F7F9F9")
        lbl.place(x=40, y=20)
        btn = Button(self, text="Quiter", command=self.quiter, font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
        btn.place(x=80, y=95)
        btn2 = Button(self, text="Annuler", command=self.annuler, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
        btn2.place(x=170, y=95)

    def quiter(self):
        sys.exit()
    def annuler(self):
        self.destroy()

'''if __name__ == "__main__":
    app = Deconnecte()
    app.mainloop()'''