import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import *
from AdminAPP import User_BE
from tkinter import messagebox
from Exceptions import VerifyAccountError
from AdminAPP import Brigades_BE
from Exceptions import BrigadeNotFound



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

class AddAccount(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Utilisateurs")
        self.geometry("800x450+240+100")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.config(bg="#F7F9F9")
        self.usr = User_BE.User()

        frm2 = Frame(self, bg="#379BF3", width=107, height=28)
        frm2.place(x=6, y=10)
        filterframe = Button(frm2, text="Nouveau Compte", bg="#CEE6F3", fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.add)
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

        col_name = self.usr.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=100)
            self.tree.heading(c, text=col_name[c])

        self.users = self.usr.select()
        index = iid = 0
        for item in self.users:
            self.tree.insert("", index, iid, values=item)
            index = iid = index + 1

        self.tree.selection_set(self.tree.get_children()[0])

        self.tree.bind("<Double-1>", self.OnDoubleClick)


                                                # ---------------------- AFFICHAGE DE LIGNE SELECTIONNEE -------------------

    def OnDoubleClick(self, event):
        try:
            self.row_selected = self.tree.item(self.tree.selection())
            self.value = self.row_selected['values'][0]
            verf = self.usr.verifyAccount(str(self.value))
            print(verf)
            if verf == True:
                self.root = tk.Tk()
                self.root.title("Comptes")
                self.root.resizable(0, 0)
                self.root.geometry("370x300+450+190")
                self.root.config(bg="#F7F9F9")
                self.frameDoubleClick()
            elif verf == False:
               raise VerifyAccountError.VerifyAccount
        except VerifyAccountError.VerifyAccount:
            messagebox.showerror("Sélectionner un utilisateur", "Veuillez sélectionner un utilisateur")

    def frameDoubleClick(self):
        frame_labels = LabelFrame(self.root, text="Modifier/Supprimer", font=("Helvetica", 13), bg="#F7F9F9")
        frame_labels.place(x=10, y=7, width=350, height=285)

        self.row_selected = self.tree.item(self.tree.selection())
        value = self.row_selected['values'][0]
        colonnes = self.usr.select_colName()
        valeurs = self.usr.select_colValue(str(value))
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
            button.place(x=110, y=220)
            button = Button(frame_labels, text="Supprimer", command=self.suppr, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
            button.place(x=180, y=220)

                             # --------------------- MODIFICATION -----------------

    def modification(self):
        try:
            id_brig = Brigades_BE.Brigades.verifyBrg(self, self.h[0].get())
            if id_brig == True:
                idBrigad = self.h[0].get()
                prenom = self.h[1].get()
                nom = self.h[2].get()
                admUSR = self.h[3].get()
                password = self.h[4].get()
                if idBrigad != '' and prenom != '' and nom != '' and admUSR != '' and password != '':
                    tab = []
                    for i in range(len(self.h)):
                        tab.append(self.h[i].get())
                    self.usr.update_colValue(tab, str(self.row_selected['values'][0]))

                    x = self.tree.selection()[0]
                    self.tree.delete(*self.tree.get_children())

                    users = self.usr.select()
                    index = iid = 0
                    for item in users:
                        self.tree.insert("", index, iid, values=item)
                        index = iid = index + 1

                    self.root.destroy()
                    showinfo("Utilisateur", "Modification effectuée avec succès")
                else:
                    showerror("Utilisateur", "Veuillez remplir tous les champs")
            else:
                raise BrigadeNotFound.BrigadeNotFound
        except BrigadeNotFound.BrigadeNotFound:
            showerror("Utilisateur", "Id brigade introuvable")
                            #--------------------- SUPPRESSION --------------------
    def suppr(self):
        self.popinfos = tk.Toplevel()
        self.popinfos.title('Suppression')
        self.popinfos.resizable(0, 0)
        self.popinfos.config(bg="#F7F9F9")
        self.popinfos.geometry("368x120+500+300")
        label = tk.Label(self.popinfos, text="Voulez-vous supprimer ce compte?", font=("Helvetica", 12), pady=13, padx=20, bg="#F7F9F9").place(x=40, y=15)
        btn1 = tk.Button(self.popinfos, text='Oui', command=self.supprimer, font=("Times New Roman", 11), bg="#4EB1FA",fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
        btn1.place(x=148, y=70)
        btn2 = tk.Button(self.popinfos, text='Non', command=self.annuler, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
        btn2.place(x=200, y=70)
    def supprimer(self):
        self.usr.deleteAccount(str(self.row_selected['values'][0]))
        x = self.tree.selection()[0]
        self.tree.delete(x)
        self.root.destroy()
        self.popinfos.destroy()

    def annuler(self):
        self.root.destroy()
        self.popinfos.destroy()


                                                                #--------------- Nouveau Compte -----------------
    def add(self):
        self.root = Tk()
        self.root.geometry('420x300+400+120')
        self.root.config(bg="#F7F9F9")
        self.root.title("Nouveau Compte")
        #self.root.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')


        label = LabelFrame(self.root, text="Ajouter un Nouveau Compte", font=("Helvetica", 13), fg="#14566D", bg="#F7F9F9", width=400, height=282)
        label.place(x=10, y=8)

        idb = Label(label, text="Id_brigade", font=("Helvetica", 12), bg="#F7F9F9", fg="#14566D")
        idb.place(x=27, y=20)
        frm = Frame(label, bg="#4EB1FA", relief=FLAT, width=240, height=24)
        frm.place(x=140, y=20)
        self.idb_ent = Entry(frm, relief=FLAT, width=26, font=("Helvetica", 12))
        self.idb_ent.place(x=1, y=1)
        add_placeholder_to(self.idb_ent, 'Id brigade')

        prn = Label(label, text="Prénom", font=("Helvetica", 12), bg="#F7F9F9", fg="#14566D")
        prn.place(x=40, y=60)
        frm1 = Frame(label, bg="#4EB1FA", relief=FLAT, width=240, height=24)
        frm1.place(x=140, y=60)
        self.prn_ent = Entry(frm1, relief=FLAT, width=26, font=("Helvetica", 12))
        self.prn_ent.place(x=1, y=1)
        add_placeholder_to(self.prn_ent, 'Prénom')

        nm = Label(label, text="Nom", font=("Helvetica", 12), bg="#F7F9F9", fg="#14566D")
        nm.place(x=50, y=100)
        frm2 = Frame(label, bg="#4EB1FA", relief=FLAT, width=240, height=24)
        frm2.place(x=140, y=100)
        self.nm_ent = Entry(frm2, relief=FLAT, width=26, font=("Helvetica", 12))
        self.nm_ent.place(x=1, y=1)
        add_placeholder_to(self.nm_ent, 'Nom')

        adm = Label(label, text="Admin", font=("Helvetica", 12), bg="#F7F9F9", fg="#14566D")
        adm.place(x=40, y=140)
        frm3 = Frame(label, bg="#4EB1FA", relief=FLAT, width=240, height=24)
        frm3.place(x=140, y=140)
        self.adm_ent = Entry(frm3, relief=FLAT, width=26, font=("Helvetica", 12))
        self.adm_ent.place(x=1, y=1)
        add_placeholder_to(self.adm_ent, 'Oui/Non')

        psw = Label(label, text="Mot de passe", font=("Helvetica", 12), bg="#F7F9F9", fg="#14566D")
        psw.place(x=18, y=180)
        frm4 = Frame(label, bg="#4EB1FA", relief=FLAT, width=240, height=24)
        frm4.place(x=140, y=180)
        self.psw_ent = Entry(frm4, relief=FLAT, width=26, font=("Helvetica", 12),  show='**')
        self.psw_ent.place(x=1, y=1)
        add_placeholder_to(self.psw_ent, 'password')


        douar_button = Button(label, text="Ajouter", font=("Times New Roman", 11), bg="#379BF3", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000", command=self.ajouter)
        douar_button.place(x=176, y=223)

    def ajouter(self):
        try:
            id_brig = Brigades_BE.Brigades.verifyBrg(self, self.idb_ent.get())
            if id_brig == True:
                idBrigad = self.idb_ent.get()
                prenom = self.prn_ent.get()
                nom = self.nm_ent.get()
                admUSR = self.adm_ent.get()
                password = self.psw_ent.get()
                if idBrigad != '' and prenom != '' and nom != '' and admUSR != '' and password != '':
                    self.usr.insert(self.idb_ent.get(), self.prn_ent.get(), self.nm_ent.get(), self.adm_ent.get(), self.psw_ent.get())
                    self.tree.delete(*self.tree.get_children())
                    users = self.usr.select()
                    index = iid = 0
                    for item in users:
                        self.tree.insert("", index, iid, values=item)
                        index = iid = index + 1
                    self.root.destroy()
                else:
                    showerror("Utilisateur", "Veuillez remplir tous les champs")
            else:
                raise BrigadeNotFound.BrigadeNotFound
        except BrigadeNotFound.BrigadeNotFound:
            showerror("Utilisateur", "Id brigade introuvable")


'''if __name__ == "__main__":
    app = AddAccount()
    app.mainloop()'''