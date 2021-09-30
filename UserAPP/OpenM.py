from tkinter import ttk
from tkinter.messagebox import *
from tkinter import *
import tkinter as tk
from UserAPP import Marche_BE
from AdminAPP import MainAdmin


class OpenProject(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("600x180+380+180")
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        container = tk.Frame(self)
        container.config(bg="red")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        page_name = Open.__name__
        frame = Open(parent=container, controller= self)
        frame.config(bg="#F7F9F9")
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky= "nsew")
        self.show_frame("Open")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class Open(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        quit_button = tk.Button(self, text="X", relief='flat', font=("Helvetica", 14), bg="#F7F9F9", command=self.quiter)
        quit_button.place(x=570)

        label = tk.Label(controller, text="Ouvrir un marché", font=("Helvetica", 18), fg="#3B3F42", bg="#F7F9F9")
        label.place(x=180, y=30)

        label = tk.Label(self, text="Marché", font=("Helvetica", 12), fg="#3B3F42", bg="#F7F9F9")
        label.place(x=35, y=100)

        marche = Marche_BE.Marche()
        self.marche_var = StringVar()
        self.marche_box = ttk.Combobox(self, textvariable=self.marche_var, width=55)
        self.marche_box.place(x=117, y=100)
        self.marche_box['values'] = marche.list_project()

        frm = Frame(self, bg="#379BF3", width=64, height=25)
        frm.place(x=495, y=97)
        open_btn = tk.Button(frm, text="Ouvrir ", bg="#CEE6F3", font=("Times New Roman", 13), fg="#379BF3",
                              relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.openProj).place(x=1, y=1, height=23)


    def openProj(self):
        march = Marche_BE.Marche()
        opn = march.open_project(self.marche_var.get())
        if opn == True:
            self.controller.destroy()
            mainAd = MainAdmin.MainAdmin()
            #usr = MainUser()
        else:
            showinfo("suppression", "Aucun marché trouvé")


    def quiter(self):
        self.controller.destroy()


if __name__ == "__main__":
    app = OpenProject()
    app.mainloop()