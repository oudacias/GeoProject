import tkinter as tk
from tkinter import *
import sys
import os
from UserAPP import Bienvenu

class ChangerMarche(tk.Tk):
    def __init__(self, nom, *args, **kwargs):
        self.nom = nom
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EpGis")
        self.geometry("300x150+500+220")
        self.resizable(0, 0)
        self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.config(bg="#F7F9F9")

        lbl = Label(self, text="Voulez vous vraiment quiter \n l'application?", font=("Times New Roman", 14), bg="#F7F9F9")
        lbl.place(x=40, y=20)
        btn = Button(self, text="Quiter", command=self.oui, font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
        btn.place(x=80, y=95)
        btn2 = Button(self, text="Annuler", command=self.non, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
        btn2.place(x=170, y=95)

    def oui(self):
        os.execv(sys.executable, ['python']+sys.argv)
        file1 = open("MyFile.txt", "w")
        file1.write(self.nom)
        file1.close()

        prj = ['C:/Users/LAILA/PycharmProjects/EpGis2/UserAPP/Bienvenu.py']
        #prj = ['C:/Users/LAILA/PycharmProjects/EpGis2/UserApp/Change.py']

        os.execv(sys.executable, [sys.executable] + prj)

        print('HELLO')
        #Bienvenu.Bienvenu()

    def non(self):
        print('non')

if __name__ == "__main__":
    app = ChangerMarche('hello')
    app.mainloop()