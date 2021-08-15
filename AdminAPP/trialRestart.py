import tkinter as tk
from tkinter import *
import os
from Log_in import Login
from AdminAPP import DataBase

from UserAPP import Autocompletecombox#----------------------------------------------------------------- PlaceHolder ---------------------------------------------------------------------------
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

class RestartApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EpGis")
        self.geometry("485x277+400+220")
        self.resizable(0, 0)
        self.config(bg="#F7F9F9")

        frame_labels = LabelFrame(self, text="Nouveau Marché", font=("Times New Roman", 14), bg="#F7F9F9")
        frame_labels.place(x=10, y=7, width=465, height=260)

        lbl = Label(frame_labels, text="Créer une base de données", font=("Times New Roman", 14), bg="#F7F9F9")
        lbl.place(x=130, y=20)

        frm = Frame(frame_labels, bg="#CEE6F3", width=410, height=30)
        frm.place(x=25, y=80)
        frm1 = Frame(frm, bg="#F7F9F9", width=408, height=28)
        frm1.place(x=1, y=1)
        # labl2 = Label(frm1, image=self.dbImge)
        # labl2.place(x=1, y=1)
        self.db_ent = tk.Entry(frm1, width=50, relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.db_ent.place(x=40, y=2)
        add_placeholder_to(self.db_ent, 'Nom du marché')

        frm = Frame(frame_labels, bg="#CEE6F3", width=410, height=30)
        frm.place(x=25, y=130)
        frm2 = Frame(frm, bg="#F7F9F9", width=408, height=28)
        frm2.place(x=1, y=1)
        # labl2 = Label(frm2, image=self.pswrdImg)
        # labl2.place(x=1, y=1)
        self.psw_ent = tk.Entry(frm2, width=50, relief='flat', bg="#F7F9F9", font=("Helvetica", 12), show='**')
        self.psw_ent.place(x=40, y=2)
        add_placeholder_to(self.psw_ent, 'Mot de passe')

        frm3 = Frame(frame_labels, bg="#379BF3", width=408, height=28)
        frm3.place(x=26, y=180)
        self.btn1 = tk.Button(frm3, text="Créer", bg="#CEE6F3", font=("Times New Roman", 13), width=44, fg="#379BF3",
                              relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.creatDB)
        self.btn1.place(x=1, y=1, height=26)

    def creatDB(self):
        db = DataBase.Database()
        #crt = db.createdb(self.db_ent.get(), self.psw_ent.get())
        print(12345)
        #sys.exit()
        #self.destroy()
        #python = sys.executable
        #os.execl(sys.executable, sys.executable, *sys.argv)
        #os.startfile("XML.py")
        #path = Login.FrameWindow()
        #exec(open(path).read())
        #exec(Path("Log_in/Login.py").read_text())
        os.execv(sys.executable, ['python "C:/Users/LAILA\PycharmProjects\EpGis2\Log_in/Login.py"'] + sys.argv)
        #os.system('python "C:/Users/LAILA\PycharmProjects\EpGis2\AdminAPP/ExportDat.py"')

if __name__ == "__main__":
    app = RestartApp()
    app.mainloop()



'''class FrameWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Ep_Gis")
        self.geometry("485x275+400+220")
        #self.overrideredirect(True)
        #self.attributes('-topmost', True)

        container = tk.Frame(self, highlightthickness=0)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        page_name = Login.Createdb.__name__
        frame = Login.Createdb(parent=container, controller=self)
        page_name = Login.Createdb.__name__
        frame = Login.Createdb(parent=container, controller=self)
        self.frames[page_name] = frame
        frame.config(bg="#F7F9F9")
        frame.grid(row=0, column=0, sticky="nsew")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    if __name__ == "__main__":
    app = FrameWindow()
    app.mainloop()
'''