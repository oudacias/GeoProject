import tkinter as tk
from tkinter import ttk
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter import messagebox
from PIL import Image, ImageTk
from AdminAPP.Brigades_BE import Brigades
from UserAPP import Interval_BE

class GererBrigd(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Brigades")
        self.geometry("800x450+240+100")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.config(bg="#F7F9F9")
        self.brig = Brigades()
        self.interv = Interval_BE.Intervalle()

        frm = Frame(self, bg="#379BF3", width=103, height=28)
        frm.place(x=6, y=10)
        filterframe = Button(frm, text="Nouvelle Brigade", bg="#CEE6F3", fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.ajouter)
        filterframe.place(x=1, y=1)


# -------------------------------------------------------------TREEVIEW-------------------------------------------------
        global tree

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview", background="#FFFFFF", foreground="#14566D")
        style.configure("Treeview.Heading", background="#8CC7DC", foreground="#0D4EA2")

        self.tree = ttk.Treeview(self)
        self.tree.place(x=5, y=50, width=775, height=385)

        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        ysb.place(x=780, y=50, height=395)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        xsb.place(x=5, y=431, width=775)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        col_name = self.brig.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=100)
            self.tree.heading(c, text=col_name[c])

        lgn = self.brig.select()
        index = iid = 0
        for item in lgn:
            self.tree.insert("", iid, index, values=item)
            index = iid = index + 1

        self.tree.bind("<Double-1>", self.OnDoubleClick)

# -------------------------------------------------------------AFFICHAGE DE LIGNE SELECTIONNEE-------------------------------------------------
    def OnDoubleClick(self, event):
        try:
            self.row_selected = self.tree.item(self.tree.selection())
            value = self.row_selected['values'][0]
            verf = self.brig.verifyBrg(str(value))

            if verf == True:
                self.root = tk.Tk()
                self.root.title("Brigades")
                self.root.resizable(0, 0)
                self.root.geometry("370x187+450+190")
                self.root.config(bg="#F7F9F9")
                self.frameDoubleClick()
            elif verf == False:
                messagebox.showerror("Brigades", "Veuillez sélectionner une brigade")
        except:
            messagebox.showerror("Brigades", "Veuillez sélectionner une brigade")

    def frameDoubleClick(self):

        frlab = LabelFrame(self.root, text="Modifier/Supprimer", font=("Helvetica", 13), bg="#F7F9F9")
        frlab.place(x=10, y=7, width=350, height=170)

        self.row_selected = self.tree.item(self.tree.selection())
        value = self.row_selected['values'][0]
        colonnes = self.brig.select_colName()
        valeurs = self.brig.select_colValue(str(value))

        i = 0
        self.h = [None] * len(colonnes)
        for j in range(len(colonnes)):
            label = tk.Label(frlab, text=''.join(colonnes[j]), font="Helvetica", pady=10, padx=20,
                             bg="#F7F9F9").grid(row=i + 2, column=0)
            nb = StringVar()
            nb.set(i)
            frm = Frame(frlab, bg="#4EB1FA", bd=1, relief=FLAT, width=40)
            frm.grid(row=i + 2, column=1)

            if i == 1:
                self.h[i] = Entry(frm, textvariable=nb, relief=FLAT, width=32, justify=RIGHT)
            else:
                self.h[i] = Entry(frm, textvariable=nb, relief=FLAT, width=32)

            self.h[i].insert(1, valeurs[0][j])
            self.h[i].grid(row=i + 2, column=1)
            i = i + 1
            button = Button(frlab, text="Modifier", command=self.modification, font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
            button.place(x=110, y=100)
            button = Button(frlab, text="Supprimer", command=self.suppr, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
            button.place(x=180, y=100)


                                                #---------------- MODIFICATION ---------------------
    def modification(self):
        if self.h[1].get() != '':
            tab = []
            for i in range(len(self.h)):
                tab.append(self.h[i].get())
            self.brig.update_colValue(tab, str(self.row_selected['values'][0]))

            x = self.tree.selection()[0]
            self.tree.delete(*self.tree.get_children())

            lgn = self.brig.select()
            index = iid = 0
            for item in lgn:
                self.tree.insert("", iid, index, values=item)
                index = iid = index + 1
            self.root.destroy()
        else:
            showerror("Brigade", "Veuillez entrer le nom du brigade")


                                            #---------------- SUPPRESSION --------------------
    def suppr(self):
        self.popinfos = tk.Toplevel()
        self.popinfos.title('Supression')
        self.popinfos.resizable(0, 0)
        self.popinfos.config(bg="#F7F9F9")
        self.popinfos.geometry("368x120+500+300")
        label = tk.Label(self.popinfos, text="Voulez-vous supprimer cette brigade?",
                         font=("Helvetica", 12), pady=13, padx=20, bg="#F7F9F9").grid(row=0, column=0)
        btn1 = tk.Button(self.popinfos, text='Oui', command=self.supprimer, font=("Times New Roman", 11),
                         bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA",
                         activeforeground="#000000")
        btn1.place(x=148, y=70)
        btn2 = tk.Button(self.popinfos, text='Non', command=self.annuler, font=("Times New Roman", 11),
                         fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02",
                         activeforeground="#000000")
        btn2.place(x=200, y=70)

    def supprimer(self):
        self.interv.delteInterv(str(self.row_selected['values'][0]))
        self.brig.deleteBrg(str(self.row_selected['values'][0]))
        self.root.destroy()
        self.popinfos.destroy()
        x = self.tree.selection()[0]
        self.tree.delete(x)
    def annuler(self):
        self.root.destroy()
        self.popinfos.destroy()


                                                        #--------------- Ajouter Nouveau Compte ------------------
    def ajouter(self):
        self.root = Tk()
        self.root.geometry('420x200+500+200')
        #self.root.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.root.config(bg="#F7F9F9")
        self.root.title("Nouvelle Brigade")

        lf = LabelFrame(self.root, text="Nouvelle Brigade", font=("Helvetica", 13), fg="#14566D", bg="#F7F9F9", width=400, height=182)
        lf.place(x=10, y=8)

        label1 = Label(lf, text="Nom de brigade(Fr)", font=("Helvetica", 12), fg="#14566D", bg="#F7F9F9")
        label1.place(x=6, y=20)
        f2 = tk.Frame(lf, bg="#4EB1FA", relief=FLAT, width=222, height=24)
        f2.place(x=160, y=20)
        self.brigd = Entry(f2, relief=FLAT, width=24, font=("Helvetica", 12))
        self.brigd.place(x=1, y=1)

        label2 = Label(lf, text="Nom de brigade(Ar)", font=("Helvetica", 12), fg="#14566D", bg="#F7F9F9")
        label2.place(x=6, y=60)
        f3 = tk.Frame(lf, bg="#4EB1FA", relief=FLAT, width=222, height=24)
        f3.place(x=160, y=60)
        self.brigAr = Entry(f3, relief=FLAT, width=24, font=("Helvetica", 12), justify=RIGHT)
        self.brigAr.place(x=1, y=1)

        btn = Button(lf, text="Créer", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000", command=self.addBrigade)
        btn.place(x=180, y=115)

    def addBrigade(self):
        brg_Fr = self.brigd.get()
        if brg_Fr != '':
            self.brig.insert(self.brigd.get(), self.brigAr.get())
            self.tree.delete(*self.tree.get_children())
            lgn = self.brig.select()
            index = iid = 0
            for item in lgn:
                self.tree.insert("", iid, index, values=item)
                index = iid = index + 1
            self.root.destroy()
        else:
            showerror("Brigade", "Veuillez entrer le nom du brigade")

'''if __name__ == "__main__":
    app = GererBrigd()
    app.mainloop()'''