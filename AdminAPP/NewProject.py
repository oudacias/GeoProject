import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox

from AdminAPP import DataBase

from UserAPP import Marche_BE
#----------------------------------------------------------------- PlaceHolder ---------------------------------------------------------------------------
class Placeholder_State(object):
    __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'with_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")

    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color = normal_color
    state.normal_font = normal_font
    state.placeholder_color = color
    state.placeholder_font = font
    state.placeholder_text = placeholder
    state.with_placeholder = True

    def on_focusin(event, entry=entry, state=state):
        if state.with_placeholder:
            entry.delete(0, "end")
            entry.config(fg=state.normal_color, font=state.normal_font)

            state.with_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg=state.placeholder_color, font=state.placeholder_font)

            state.with_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg=color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")

    entry.placeholder_state = state

    return state

class NewProject(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EpGis")
        self.geometry("485x380+450+150")
        self.resizable(0, 0)
        self.config(bg="#F7F9F9")
        project_directory = os.path.abspath(os.curdir)
        dbimg = project_directory + "/icons/database.png"
        self.dbImge = PhotoImage(file=dbimg, master=self)
        pswrd = project_directory + "/icons/mot-de-passe.png"
        self.pswrdImg = PhotoImage(file=pswrd, master=self)
        usrImg = project_directory + "/icons/user.png"
        self.usrImg = PhotoImage(file=usrImg, master=self)
        epsgImg = project_directory + "/icons/la-grille.png"
        self.epsgImg = PhotoImage(file=epsgImg, master=self)

        frame_labels = LabelFrame(self, text="Nouveau Marché", font=("Times New Roman", 14), bg="#F7F9F9")
        frame_labels.place(x=10, y=7,width=465, height=360)


        lbl = Label(frame_labels, text="Créer une base de données", font=("Times New Roman", 14), bg="#F7F9F9")
        lbl.place(x=130, y=20)

        userFrm = Frame(frame_labels, bg="#CEE6F3", width=410, height=30)
        userFrm.place(x=25, y=80)
        usrFrm = Frame(userFrm, bg="#F7F9F9", width=408, height=28)
        usrFrm.place(x=1, y=1)
        labl = Label(usrFrm, image=self.usrImg)
        labl.place(x=1, y=1)
        self.db_user = tk.Entry(usrFrm, width=50, relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.db_user.place(x=40, y=2)
        add_placeholder_to(self.db_user, 'Utilisateur du marché')

        marcheFrm = Frame(frame_labels, bg="#CEE6F3", width=410, height=30)
        marcheFrm.place(x=25, y=130)
        dbFrm = Frame(marcheFrm, bg="#F7F9F9", width=408, height=28)
        dbFrm.place(x=1, y=1)
        labl = Label(dbFrm, image=self.dbImge)
        labl.place(x=1, y=1)
        self.db_ent = tk.Entry(dbFrm, width=50, relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.db_ent.place(x=40, y=2)
        add_placeholder_to(self.db_ent, 'Nom du marché')

        epsgFrm= Frame(frame_labels, bg="#CEE6F3", width=410, height=30)
        epsgFrm.place(x=25, y=180)
        epsg_frm = Frame(epsgFrm, bg="#F7F9F9", width=408, height=28)
        epsg_frm.place(x=1, y=1)
        labl = Label(epsg_frm, image=self.epsgImg)
        labl.place(x=1, y=1)
        self.epsg_ent = tk.Entry(epsg_frm, width=50, relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.epsg_ent.place(x=40, y=2)
        add_placeholder_to(self.epsg_ent, 'EPSG')

        pswFrm = Frame(frame_labels, bg="#CEE6F3", width=410, height=30)
        pswFrm.place(x=25, y=230)
        psw_frm = Frame(pswFrm, bg="#F7F9F9", width=408, height=28)
        psw_frm.place(x=1, y=1)
        labl = Label(psw_frm, image=self.pswrdImg)
        labl.place(x=1, y=1)
        self.psw_ent = tk.Entry(psw_frm, width=50, relief='flat', bg="#F7F9F9", font=("Helvetica", 12), show='**')
        self.psw_ent.place(x=40, y=2)
        add_placeholder_to(self.psw_ent, 'MotDePasse')

        frm4 = Frame(frame_labels, bg="#379BF3", width=408, height=28)
        frm4.place(x=26, y=280)
        self.btn1 = tk.Button(frm4, text="Créer", bg="#CEE6F3", font=("Times New Roman", 13), width=44, fg="#379BF3",
                              relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3",
                              command=self.creatDB)
        self.btn1.place(x=1, y=1, height=26)


    def creatDB(self):
        db = DataBase.Database()
        crt = db.createdb(self.db_user.get(), self.db_ent.get(), self.psw_ent.get(), self.epsg_ent.get())
        if (crt):
            mrch = Marche_BE.Marche()
            mrch.connect_marche(self.db_ent.get())
            msg = messagebox.showinfo("Créer DB", "Un nouveau marché a été créé avec succès")

