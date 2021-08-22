import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from AdminAPP import User_BE
from AdminAPP import MainAdmin
from AdminAPP import CreateM
from UserAPP import MainUser
from UserAPP import Marche_BE
from Exceptions import SplitError
from Exceptions import LoginError

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

# --------------------------------------------------------------------- Login GUI ----------------------------------------------------------------
class LoginFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EpGis")
        self.geometry("485x277+400+220")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')

        container = tk.Frame(self, highlightthickness=0)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (LogIn, Modifypass):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.config(bg="#F7F9F9")
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LogIn")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        project_directory = os.path.abspath(os.curdir)
        usrImg = project_directory + "/icons/user.png"
        self.usrImg = PhotoImage(file=usrImg)
        pswrd = project_directory + "/icons/padlock.png"
        self.pswrdImg = PhotoImage(file=pswrd)

        frame_labels = LabelFrame(self, text="Login", font=("Times New Roman", 14), bg="#F7F9F9")
        frame_labels.place(x=10, y=7, width=465, height=260)

        frm = Frame(frame_labels, bg="#CEE6F3", width=410, height=30)
        frm.place(x=25, y=30)
        frm1 = Frame(frm ,bg="#F7F9F9", width=408, height=28)
        frm1.place(x=1, y=1)
        labl = Label(frm1, image=self.usrImg)
        labl.place(x=1, y=1)
        self.userentry = tk.Entry(frm1, width=50, relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.userentry.place(x=40, y=2)
        add_placeholder_to(self.userentry, 'Nom et Prénom')

        frm = Frame(frame_labels, bg="#CEE6F3", width=410, height=30)
        frm.place(x=25, y=80)
        frm2 = Frame(frm, bg="#F7F9F9", width=408, height=28)
        frm2.place(x=1, y=1)
        labl2 = Label(frm2, image=self.pswrdImg)
        labl2.place(x=1, y=1)
        self.passentry = tk.Entry(frm2, width=50, relief='flat', bg="#F7F9F9", font=("Helvetica", 12), show='**')
        self.passentry.place(x=40, y=2)
        add_placeholder_to(self.passentry, 'Mot de passe')

        frm3 = Frame(frame_labels, bg="#379BF3", width=408, height=28)
        frm3.place(x=26, y=140)
        self.btn1 = tk.Button(frm3, text="Login", bg="#CEE6F3", font=("Times New Roman", 13), width=44, fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.connexion)
        self.btn1.place(x=1, y=1, height=26)

        self.btn1 = tk.Button(frame_labels, text="Mot de passe oublié?", bg="#F7F9F9", font=("Times New Roman", 13), fg="#DF7800", relief='flat', activebackground="#F7F9F9", activeforeground="#DF7800", command=self.modifypass)
        self.btn1.place(x=160, y=190)

    def quiter(self):
        self.controller.destroy()

    def modifypass(self):
        self.controller.show_frame("Modifypass")

    def connexion(self):
        try:
            mrch = Marche_BE.Marche()
            self.userentry = "admin admin"
            self.passentry ="123"

            if (len(str(self.userentry.get()).split()) == 2):
                user = User_BE.User()
                usr = user.user_verification(self.userentry.get(), self.passentry.get())
                if (usr):
                        admn = user.admin_verification(self.userentry.get(), self.passentry.get())
                        if admn == True:
                            marche = mrch.verifyMarche()
                            if marche == True:
                                self.controller.destroy()
                                opn = MainAdmin.MainAdmin()
                            else:
                                self.controller.destroy()
                                crt = CreateM.Creatproject()
                        else:
                            self.controller.destroy()
                            opn = MainUser.MainUser()
                else:
                    raise LoginError.LoginError
            else:
                raise SplitError.SplitError
        except SplitError.SplitError:
            msg = messagebox.showerror("Ouvrir le Marché", "Vous devez saisir votre nom et prénom")
        except LoginError.LoginError:
            msg = messagebox.showerror("Ouvrir le Marché", "Votre nom d'utilisateur ou votre mot de passe est incorrect")


            #---------------------- Change Password ----------------------------

class Modifypass(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lFrm = LabelFrame(self, text="Modifier votre mot de passe", font=("Times New Roman", 14), bg="#F7F9F9")
        lFrm.place(x=10, y=7, width=465, height=260)

        prnm = tk.Label(lFrm, text="Nom", fg="#3B3F42", bg="#F7F9F9", font=("Helvetica", 12))
        prnm.place(x=90, y=30)
        frm = Frame(lFrm, bg="#CEE6F3", width=222, height=24)
        frm.place(x=210, y=30)
        self.prnm_ent = tk.Entry(frm, width=24,  relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.prnm_ent.place(x=1, y=1)
        add_placeholder_to(self.prnm_ent, 'Prénom')

        nom = tk.Label(lFrm, text="Prénom", fg="#3B3F42", bg="#F7F9F9", font=("Helvetica", 12))
        nom.place(x=80, y=80)
        frm = Frame(lFrm, bg="#CEE6F3", width=222, height=24)
        frm.place(x=210, y=80)
        self.nm_ent = tk.Entry(frm, width=24, relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.nm_ent.place(x=1, y=1)
        add_placeholder_to(self.nm_ent, 'Nom')

        psw = tk.Label(lFrm, text="Nouveau mot de passe", fg="#3B3F42", bg="#F7F9F9", font=("Helvetica", 12))
        psw.place(x=20, y=130)

        frm = Frame(lFrm, bg="#CEE6F3", width=222, height=24)
        frm.place(x=210, y=130)
        self.psw_ent = tk.Entry(frm, width=24, relief='flat', bg="#F7F9F9", font=("Helvetica", 12), show='*')
        self.psw_ent.place(x=1, y=1)
        add_placeholder_to(self.psw_ent, 'Mot de passe')

        frm3 = Frame(lFrm, bg="#379BF3", width=219, height=26)
        frm3.place(x=212, y=180)
        self.btn1 = tk.Button(frm3, text="Modifier", bg="#CEE6F3", font=("Times New Roman", 13), width=23, fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.updat)
        self.btn1.place(x=1, y=1, height=24)

    def updat(self):
        try:
            usr = User_BE.User()
            user = usr.verify_User(self.nm_ent.get(), self.prnm_ent.get())
            if user == True:
                usr.change_password(self.nm_ent.get(), self.prnm_ent.get(), self.psw_ent.get())
                msg = messagebox.showinfo("Modifier votre mot de passe", "Votre mot de passe a été bien modifiée")
                self.controller.show_frame("Login")
            else:
                raise LoginError.LoginError
        except LoginError.LoginError:
            msg = messagebox.showwarning("Modifier votre mot de passe", "Ce compte n'exsite pas")

if __name__ == "__main__":
    app = LoginFrame()
    app.mainloop()