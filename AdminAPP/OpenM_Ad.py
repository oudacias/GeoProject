from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from UserAPP import Marche_BE
from AdminAPP import CreateM
from AdminAPP import MainAdmin

class OpenProject_Ad(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("740x220+310+210")
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        container = tk.Frame(self)
        container.config(bg="red")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        page_name = OpenCreateProject.__name__
        frame = OpenCreateProject(parent=container, controller= self)
        #frame.config(bg="#F2F3F5")
        frame.config(bg="#F7F9F9")
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky= "nsew")
        self.show_frame("OpenCreateProject")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class OpenCreateProject(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        quit_button = tk.Button(self, text="X", relief='flat', font=("Helvetica", 14), bg="#F7F9F9", activebackground="#F7F9F9", command=self.quiter)
        quit_button.place(x=708)

        openM = tk.Label(controller, text="Ouvrir un marché", font=("Times New Roman", 18), fg="#000000", bg="#F7F9F9")
        openM.place(x=275, y=25)

        open_label = tk.Label(self, text="Marché", font=("Helvetica", 12), fg="#000000", bg="#F7F9F9")
        open_label.place(x=40, y=110)

        marche = Marche_BE.Marche()
        self.marche_var = StringVar()
        self.marche_box = ttk.Combobox(self, textvariable=self.marche_var, width=55)
        self.marche_box.place(x=118, y=110)
        self.marche_box['values'] = marche.list_project()

        frm = Frame(self, bg="#379BF3", width=64, height=25)
        frm.place(x=492, y=108)
        open = tk.Button(frm, text="Ouvrir ", bg="#CEE6F3", font=("Times New Roman", 13), fg="#379BF3",
                              relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.open).place(x=1, y=1,height=23)

        frm2 = Frame(self, bg="#DF7800", width=123, height=25)
        frm2.place(x=575, y=108)
        create = tk.Button(frm2, text="Nouveau marché ", bg="#FFC98A", font=("Times New Roman", 12),
                              fg ="#DF7800", relief='flat', activebackground="#FEB765", activeforeground="#DF7800", command=self.create).place(x=1, y=1,height=23)


                              # ---------------------- Open ---------------------
    def open(self):

        march = Marche_BE.Marche()
        opn = march.open_project(self.marche_var.get())
        if opn == True:
            self.controller.destroy()
            print("yes")
            p = MainAdmin()
        else:
            showinfo("Ouvrir un marché", "Aucun marché trouvé")


                              # ---------------------- Create ---------------------
    def create(self):
        self.controller.destroy()
        crt = CreateM.Creatproject()


                              # ---------------------- Quiter ---------------------
    def quiter(self):
        self.controller.destroy()

if __name__ == "__main__":
    app = OpenProject_Ad()
    app.mainloop()