import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import *
import os
from PIL import Image, ImageTk
from UserAPP import Consistance_BE

class AddConsistance(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Consistance")
        self.geometry("800x450+240+100")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.config(bg="#F7F9F9")

        frm2 = Frame(self, bg="#379BF3", width=127, height=28)
        frm2.place(x=6, y=10)
        filterframe = Button(frm2, text="Nouvelle Consistance", bg="#CEE6F3", fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.add)
        filterframe.place(x=1, y=1)
        self.const = Consistance_BE.Consistance()

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

        col_name = self.const.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4", "5")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=100)
            self.tree.heading(c, text=col_name[c])

        self.consists = self.const.selectConsist()
        index = iid = 0
        for item in self.consists:
            self.tree.insert("", index, iid, values=item)
            index = iid = index + 1
        self.tree.selection_set(self.tree.get_children()[0])

        self.tree.bind("<Double-1>", self.OnDoubleClick)


                                                # ---------------------- AFFICHAGE DE LIGNE SELECTIONNEE -------------------
    def OnDoubleClick(self, event):
        try:
            self.row_selected = self.tree.item(self.tree.selection())
            value = self.row_selected['values'][0]
            verf = self.const.verifyConsistance(str(value))

            if verf == True:
                self.root = tk.Tk()
                self.root.title("Consistance")
                self.root.resizable(0, 0)
                self.root.geometry("370x230+450+190")
                self.root.config(bg="#F7F9F9")
                self.frameDoubleClick()
            elif verf == False:
                showerror("Consistance", "Veuillez s??lectionner une consistance")
        except:
            showerror("Consistance ", "Veuillez s??lectionner une consistance")

    def frameDoubleClick(self):

        frame_labels = LabelFrame(self.root, text="Modifier", font=("Helvetica", 13), bg="#F7F9F9")
        frame_labels.place(x=10, y=7, width=350, height=210)

        self.row_selected = self.tree.item(self.tree.selection())
        value = self.row_selected['values'][0]
        colonnes = self.const.select_colName()
        valeurs = self.const.select_colValue(str(value))

        i = 0
        self.h = [None] * len(colonnes)
        for j in range(len(colonnes)):
            label = tk.Label(frame_labels, text=''.join(colonnes[j]), font="Helvetica", pady=10, padx=20, bg="#F7F9F9").grid(row=i+2, column=0)
            nb = StringVar()
            nb.set(i)
            frm = Frame(frame_labels, bg="#4EB1FA", bd=1, relief=FLAT, width=40)
            frm.grid(row=i + 2, column=1)
            if i == 1:
                self.h[i] = Entry(frm, textvariable=nb, relief=FLAT, width=32, justify=RIGHT)
            else:
                self.h[i] = Entry(frm, textvariable=nb, relief=FLAT, width=32)
            self.h[i].insert(1, valeurs[0][j])
            self.h[i].grid(row=i+2, column=1)
            i = i+1
            button = Button(frame_labels, text="Modifier", command=self.modification, font=("Times New Roman", 11), bg="#4EB1FA",fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
            button.place(x=100, y=150)
            button = Button(frame_labels, text="Supprimer", command=self.suppr, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
            button.place(x=170, y=150)


                                                        # --------------------- MODIFICATION -----------------
    def modification(self):
        if self.h[0].get() != '':
            tab = []
            for i in range(len(self.h)):
                tab.append(self.h[i].get())
            self.const.update_colValue(tab, str(self.row_selected['values'][0]))

            self.tree.delete(*self.tree.get_children())

            self.consists = self.const.selectConsist()
            index = iid = 0
            for item in self.consists:
                self.tree.insert("", index, iid, values=item)
                index = iid = index + 1
            self.root.destroy()
        else:
            showerror("Consistance", "Veuillez remplir le champ: Libelle Fr")

                                                 #--------------------- SUPPRESSION --------------------
    def suppr(self):
        self.popinfos = tk.Toplevel()
        self.popinfos.title('Supression')
        self.popinfos.resizable(0, 0)
        self.popinfos.config(bg="#F7F9F9")
        self.popinfos.geometry("368x120+500+300")
        label = tk.Label(self.popinfos, text="Voulez-vous supprimer ce type de consistance?", font=("Helvetica", 12), pady=13, padx=20, bg="#F7F9F9").place(x=25, y=15)
        btn1 = tk.Button(self.popinfos, text='Oui', command=self.supprimer, font=("Times New Roman", 11), bg="#4EB1FA",fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
        btn1.place(x=148, y=70)
        btn2 = tk.Button(self.popinfos, text='Non', command=self.annuler, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
        btn2.place(x=200, y=70)

    def supprimer(self):
        self.const.deleteConsistance(str(self.row_selected['values'][0]))
        self.root.destroy()
        self.popinfos.destroy()
        x = self.tree.selection()[0]
        self.tree.delete(x)
    def annuler(self):
        self.root.destroy()
        self.popinfos.destroy()


                                                                #--------------- Nouvelle Consistance -----------------
    def add(self):
        self.root = Toplevel()
        self.root.geometry("400x250+450+190")
        self.root.title("Nouvelle Consistance")
        self.root.resizable(0, 0)
        self.root.config(bg="#F7F9F9")

        label = LabelFrame(self.root, text="Ajouter une nouvelle consistance", font=("Helvetica", 13), bg="#F7F9F9", width=380, height=230)
        label.place(x=10, y=8)

        libelleFr = Label(self.root, text="Libelle Fr", font=("Helvetica", 12), bg="#F7F9F9")
        libelleFr.place(x=20, y=50)
        frm2 = Frame(self.root, bg="#4EB1FA", relief=FLAT, width=231, height=24)
        frm2.place(x=140, y=50)
        self.libelleFr_entry = Entry(frm2, relief=FLAT, width=25, font=("Helvetica", 12))
        self.libelleFr_entry.place(x=1, y=1)

        libelleAr = Label(self.root, text="Libelle Ar", font=("Helvetica", 12), bg="#F7F9F9", justify=RIGHT)
        libelleAr.place(x=20, y=90)
        frm = Frame(self.root, bg="#4EB1FA", relief=FLAT, width=231, height=24)
        frm.place(x=140, y=90)
        self.libelleAr_entry = Entry(frm, relief=FLAT, width=25, font=("Helvetica", 12), justify=RIGHT)
        self.libelleAr_entry.place(x=1, y=1)

        abrv = Label(self.root, text="Abr??viation", font=("Helvetica", 12), bg="#F7F9F9")
        abrv.place(x=30, y=130)
        frm3 = Frame(self.root, bg="#4EB1FA", relief=FLAT, width=231, height=24)
        frm3.place(x=140, y=130)
        self.abrv_entry = Entry(frm3, relief=FLAT, width=25, font=("Helvetica", 12))
        self.abrv_entry.place(x=1, y=1)

        douar_button = Button(self.root, text="Ajouter", font=("Times New Roman", 11), bg="#4EB1FA",fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000", command=self.ajouter)
        douar_button.place(x=170, y=190)

    def ajouter(self):
        if self.libelleFr_entry.get()!= '':
            self.const.addNewConsis(self.libelleFr_entry.get(), self.libelleAr_entry.get(), self.abrv_entry.get())
            self.tree.delete(*self.tree.get_children())
            self.consists = self.const.selectConsist()
            index = iid = 0
            for item in self.consists:
                self.tree.insert("", index, iid, values=item)
                index = iid = index + 1
            self.tree.selection_set(self.tree.get_children()[0])

            self.root.destroy()
        else:
            showerror("Consistance", "Veuillez remplir le champ: Libelle Fr")

'''if __name__ == "__main__":
    app = AddConsistance()
    app.mainloop()'''