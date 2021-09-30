from tkinter import *
import tkinter as tk
from tkinter import filedialog
import os
from AdminAPP import Importation_BE
from tkinter import messagebox

class ImportCoord(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Importation")
        self.geometry("300x150+520+200")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.config(bg="#F7F9F9")

        lf = LabelFrame(self, text="Coordonnées", width=290, height=140, bg="#F7F9F9")
        lf.place(x=5, y=5)
        lbl = Label(lf, text="Importer les coordonnées définitives \n depuis un fichier :", font=("Helvetica", 12),
                    bg="#F7F9F9")
        lbl.place(x=20, y=5)

        frm = Frame(lf, bg="#379BF3", width=55, height=28)
        frm.place(x=85, y=80)
        xslBtn = tk.Button(frm, text="Excel", bg="#CEE6F3", font=("Times New Roman", 13), fg="#379BF3", relief='flat',
                           activebackground="#CEE6F3", activeforeground="#379BF3", command=self.importXsl)
        xslBtn.place(x=1, y=1, height=26)

        frm2 = Frame(lf, bg="#379BF3", width=46, height=28)
        frm2.place(x=155, y=80)
        xslBtn = tk.Button(frm2, text="TXT", bg="#CEE6F3", font=("Times New Roman", 13), fg="#379BF3", relief='flat',
                           activebackground="#CEE6F3", activeforeground="#379BF3", command=self.importTxt)
        xslBtn.place(x=1, y=1, height=26)

    def importXsl(self):
        imprt = Importation_BE.Importation()
        CURRENT_DIRECTORY = os.getcwd()
        options = {
            'initialdir': CURRENT_DIRECTORY,
            'title': 'Choose your file',
            'filetypes': (("Text File", "*.xlsx"),)}

        name_fl = filedialog.askopenfilename(**options)
        imprt.coordXY_xsl(name_fl)
        messagebox.showinfo("Coordonnées X_Y", "Importation des coordonnées effectué avec succées")
        self.destroy()


    def importTxt(self):
        imprt = Importation_BE.Importation()
        CURRENT_DIRECTORY = os.getcwd()
        options = {
            'initialdir': CURRENT_DIRECTORY,
            'title': 'Choose your file',
            'filetypes': (("Text File", "*.txt"),)}

        name_file = filedialog.askopenfilename(**options)
        imprt.coordXY_txt(name_file)
        messagebox.showinfo("Coordonnées X_Y", "Importation des coordonnées effectué avec succées")
        self.destroy()


if __name__ == "__main__":
    app = ImportCoord()
    app.mainloop()
