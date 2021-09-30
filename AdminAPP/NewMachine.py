from tkinter import *
import tkinter as tk
from tkinter.messagebox import *
from tkinter import ttk
from AdminAPP import Machines_BE
from AdminAPP import NamesDB_BE
from UserAPP import Autocompletecombox

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

class AddMachine(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Machines")
        self.geometry("800x450+240+100")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.config(bg="#F7F9F9")

        frm2 = Frame(self, bg="#379BF3", width=109, height=28)
        frm2.place(x=6, y=10)
        filterframe = Button(frm2, text="Nouvelle Machine", bg="#CEE6F3", fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.add)
        filterframe.place(x=1, y=1)


# -------------------------------------------------------------TREEVIEW-------------------------------------------------
        global tree
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview", background="#FFFFFF", foreground="#14566D")
        style.configure("Treeview.Heading", background="#B0D9E8", foreground="#14566D")

        self.tree = ttk.Treeview(self)
        self.tree.place(x=5, y=50, width=775, height=385)

        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        ysb.place(x=780, y=50, height=395)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        xsb.place(x=5, y=431, width=775)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        self.machn = Machines_BE.NewMachin()
        col_name = self.machn.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=100)
            self.tree.heading(c, text=col_name[c])

        val = self.machn.select()
        index = iid = 0
        for item in val:
            self.tree.insert("", index, iid, values=item)
            index = iid = index + 1

        self.tree.bind("<Double-1>", self.OnDoubleClick)


                                                # ---------------------- AFFICHAGE DE LIGNE SELECTIONNEE -------------------

    def OnDoubleClick(self, event):
        self.root = tk.Tk()
        self.root.title("Machines")
        self.root.resizable(0, 0)
        self.root.geometry("370x207+450+190")
        self.root.config(bg="#F7F9F9")

        frame_labels = LabelFrame(self.root, text="Modifier/Supprimer", font=("Helvetica", 13), bg="#F7F9F9")
        frame_labels.place(x=10, y=7, width=350, height=190)

        self.row_selected = self.tree.item(self.tree.selection())
        value = self.row_selected['values'][0]
        colonnes = self.machn.select_colName()
        valeurs = self.machn.select_colValue(str(value))

        i = 0
        self.h = [None] * len(colonnes)
        for j in range(len(colonnes)):
            label = tk.Label(frame_labels, text=''.join(colonnes[j]), font="Helvetica", pady=10, padx=20, bg="#F7F9F9").grid(row=i + 2, column=0)
            nb = StringVar()
            nb.set(i)
            frm = Frame(frame_labels, bg="#4EB1FA", bd=1, relief=FLAT, width=40)
            frm.grid(row=i + 2, column=1)
            self.h[i] = Entry(frm, textvariable=nb, relief=FLAT, width=32)
            self.h[i].insert(1, valeurs[0][j])
            self.h[i].grid(row=i + 2, column=1)
            i = i + 1
            button = Button(frame_labels, text="Modifier", command=self.modification, font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
            button.place(x=110, y=120)
            button = Button(frame_labels, text="Supprimer", command=self.suppr, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
            button.place(x=180, y=120)


# --------------------- MODIFICATION -----------------
    def modification(self):
        for i in range(len(self.h)):
            if self.h[i].get() != '':
                tab = []
                for i in range(len(self.h)):
                    tab.append(self.h[i].get())
                self.machn.update_colValue(tab, str(self.row_selected['values'][0]))
                self.tree.delete(*self.tree.get_children())
                val = self.machn.select()
                index = iid = 0
                for item in val:
                    self.tree.insert("", index, iid, values=item)
                    index = iid = index + 1

                self.root.destroy()
            else:
                showerror("Machine", "Veuillez remplir tous les champs ")

            #--------------------- SUPPRESSION --------------------
    def suppr(self):
        verf = self.machn.verifyMachine(str(self.row_selected['values'][0]))
        if verf == 1:
            self.popinfos = tk.Toplevel()
            self.popinfos.title('Suppression')
            self.popinfos.resizable(0, 0)
            self.popinfos.config(bg="#F7F9F9")
            self.popinfos.geometry("368x120+500+300")
            label = tk.Label(self.popinfos, text="Voulez-vous supprimer cette machine?", font=("Helvetica", 12), pady=13, padx=20, bg="#F7F9F9").place(x=25, column=14)
            btn1 = tk.Button(self.popinfos, text='Oui', command=self.supprimer, font=("Times New Roman", 11), bg="#4EB1FA",fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
            btn1.place(x=148, y=70)
            btn2 = tk.Button(self.popinfos, text='Non', command=self.annuler, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
            btn2.place(x=200, y=70)
    def supprimer(self):
        self.machn.deleteMachine(str(self.row_selected['values'][0]))
        self.tree.delete(*self.tree.get_children())
        val = self.machn.select()
        index = iid = 0
        for item in val:
            self.tree.insert("", index, iid, values=item)
            index = iid = index + 1
        self.popinfos.destroy()
        self.root.destroy()

    def annuler(self):
        self.popinfos.destroy()
        self.root.destroy()


# --------------------- NOUVELLE MACHINE --------------------
    def add(self):
        self.root = Tk()
        self.root.geometry('420x255+400+220')
        self.root.config(bg="#F7F9F9")
        self.root.title("Nouvelle Machine")

        lFrm = LabelFrame(self.root, text="Ajouter une machine", bg="#F7F9F9", fg="#3B3F42", font=("Helvetica", 13), width=400, height=240)
        lFrm.place(x=10, y=7)

        nom = tk.Label(lFrm, text="Nom", fg="#3B3F42", bg="#F7F9F9", font=("Helvetica", 12))
        nom.place(x=55, y=20)
        frm = Frame(lFrm, bg="#4EB1FA", relief=FLAT, width=222, height=24)
        frm.place(x=140, y=20)
        self.nom_ent = tk.Entry(frm, width=24, relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.nom_ent.place(x=1, y=1)
        add_placeholder_to(self.nom_ent, 'Nom de la machine')

        psw = tk.Label(lFrm, text="address IP", fg="#3B3F42", bg="#F7F9F9", font=("Helvetica", 12))
        psw.place(x=26, y=70)
        frm2 = Frame(lFrm, bg="#4EB1FA", relief=FLAT, width=222, height=24)
        frm2.place(x=140, y=70)
        self.ip_ent = tk.Entry(frm2, width=24, relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.ip_ent.place(x=1, y=1)
        add_placeholder_to(self.ip_ent, "L'adresse Ip")

        typeMachine = Label(lFrm, text="Type", fg="#3B3F42", bg="#F7F9F9", font=("Helvetica", 12))
        typeMachine.place(x=50, y=120)
        frm3 = Frame(lFrm, bg="#4EB1FA", relief=FLAT, width=223, height=26)
        frm3.place(x=140, y=120)
        typeVal =  ['Server', 'Client']
        type_var = StringVar()
        self.typeComb = Autocompletecombox.Autocompletecombox(frm3, textvariable=type_var, width=22, font=("Helvetica", 12))
        self.typeComb.set_completion_list(typeVal)
        self.typeComb.place(x=1, y=1)

        self.btn1 = tk.Button(self.root, text="Ajouter", font=("Times New Roman", 12), bg="#379BF3", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000", command=self.creat)
        self.btn1.place(x=190, y=200)

    def creat(self):
        mchn = Machines_BE.NewMachin()
        nwDB = NamesDB_BE.NewDB()
        machine = self.nom_ent.get()
        ipMachine = self.ip_ent.get()
        typMachine = self.typeComb.get()
        if machine != '' and ipMachine != '' and typMachine != '':
            crt = mchn.addMachine(self.nom_ent.get(), self.ip_ent.get(), self.typeComb.get())
            self.tree.delete(*self.tree.get_children())
            val = self.machn.select()
            index = iid = 0
            for item in val:
                self.tree.insert("", index, iid, values=item)
                index = iid = index + 1
            self.root.destroy()
        else:
            showerror("Machine", "Veuillez remplir tous les champs ")


'''if __name__ == "__main__":
    app = AddMachine()
    app.mainloop()'''