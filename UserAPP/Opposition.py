import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import *
from UserAPP import Oppostition_BE

class AddOppostition(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Type Opposition")
        self.geometry("800x450+240+100")
        self.resizable(0, 0)
        self.config(bg="#F7F9F9")
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.tpOppost = Oppostition_BE.TypeOppos()

        frm2 = Frame(self, bg="#379BF3", width=161, height=28)
        frm2.place(x=6, y=10)
        filterframe = Button(frm2, text="Nouveau Type d'Opposition", bg="#CEE6F3", fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.add)
        filterframe.place(x=1, y=1)


                                                            # ------------------ TREEVIEW ---------------------
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

        col_name = self.tpOppost.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=100)
            self.tree.heading(c, text=col_name[c])

        typSpeclt = self.tpOppost.select()
        index = iid = 0
        for item in typSpeclt:
            self.tree.insert("", index, iid, values=item)
            index = iid = index + 1
        self.tree.selection_set(self.tree.get_children()[0])

        self.tree.bind("<Double-1>", self.OnDoubleClick)

# -------------------------------------------------------------AFFICHAGE DE LIGNE SELECTIONNEE-------------------------------------------------
    def OnDoubleClick(self, event):
        try:
            self.row_selected = self.tree.item(self.tree.selection())
            value = self.row_selected['values'][0]
            verf = self.tpOppost.verifyOppost(str(value))
            if verf == True:
                self.root = tk.Tk()
                self.root.title("Type d'opposition")
                self.root.resizable(0, 0)
                self.root.geometry("366x201+450+190")
                self.root.config(bg="#F7F9F9")
                self.frameDoubleClick()
            elif verf == False:
                showerror("Opposition", "Veuillez sélectionner un type d'opposition")
        except:
            showerror("Opposition", "Veuillez sélectionner un type d'opposition")

    def frameDoubleClick(self):
        frame_labels = LabelFrame(self.root, text="Modifier/Supprimer", font=("Helvetica", 13), bg="#E3F3F3")
        frame_labels.place(x=8, y=7, width=350, height=186)

        self.row_selected = self.tree.item(self.tree.selection())
        value = self.row_selected['values'][0]
        colonnes = self.tpOppost.select_colName()
        valeurs = self.tpOppost.select_colValue(str(value))

        i =0
        self.h = [None] * len(colonnes)
        for j in range(len(colonnes)):
            label = tk.Label(frame_labels, text=''.join(colonnes[j]), font="Helvetica", pady=10, padx=20, bg="#E3F3F3").grid(row=i+2, column=0)
            nb = StringVar()
            nb.set(i)
            frm = Frame(frame_labels, bg="#4EB1FA", bd=1, relief=FLAT, width=40)
            frm.grid(row=i + 2, column=1)
            if i == 1:
                self.h[i] = Entry(frm, textvariable=nb, relief=FLAT, width=32, justify=RIGHT)
            else:
                self.h[i] = Entry(frm, textvariable=nb, relief=FLAT, width=32)
            self.h[i].insert(1, valeurs[0][j])
            self.h[i].grid(row=i + 2, column=1)
            i = i + 1

        frm2 = Frame(frame_labels, bg="#379BF3", width=78, height=28)
        frm2.place(x=80, y=110)
        button = Button(frm2, text="Modifier", bg="#CEE6F3", font=("Times New Roman", 13), fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.modification)
        button.place(x=1, y=1, height=26)

        frm3 = Frame(frame_labels, bg="#F9983F", width=87, height=28)
        frm3.place(x=185, y=110)
        button = Button(frm3, text="Supprimer", bg="#CEE6F3", font=("Times New Roman", 13), fg="#F9983F", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.suppr)
        button.place(x=1, y=1, height=26)


                                                    #------------------ MODIFICATION ---------------------
    def modification(self):
        if self.h[0].get() != '':
            tab = []
            for i in range(len(self.h)):
                tab.append(self.h[i].get())
            self.tpOppost.update_colValue(tab, str(self.row_selected['values'][0]))

            self.tree.delete(*self.tree.get_children())

            typSpeclt = self.tpOppost.select()
            index = iid = 0
            for item in typSpeclt:
                self.tree.insert("", index, iid, values=item)
                index = iid = index + 1

            self.root.destroy()
        else:
            showerror("Opposition", "Veuillez remplir le champ: Libelle Fr")

                                                    #------------------ SUPPRESSION ---------------------
    def suppr(self):
        self.popinfos = tk.Toplevel()
        self.popinfos.title('Supression')
        self.popinfos.resizable(0, 0)
        self.popinfos.config(bg="#F7F9F9")
        self.popinfos.geometry("368x120+500+300")
        label = tk.Label(self.popinfos, text="Voulez-vous supprimer ce type d'opposition?", font=("Helvetica", 12),
                         pady=13, padx=20, bg="#F7F9F9").grid(row=0, column=0)
        btn1 = tk.Button(self.popinfos, text='Oui', command=self.supprimer, font=("Times New Roman", 11),
                         bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA",
                         activeforeground="#000000")
        btn1.place(x=148, y=70)
        btn2 = tk.Button(self.popinfos, text='Non', command=self.annuler, font=("Times New Roman", 11),
                         fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02",
                         activeforeground="#000000")
        btn2.place(x=200, y=70)

    def supprimer(self):
        self.tpOppost.deleteOppost(str(self.row_selected['values'][0]))
        self.root.destroy()
        self.popinfos.destroy()
        x = self.tree.selection()[0]
        self.tree.delete(x)

    def annuler(self):
        self.root.destroy()
        self.popinfos.destroy()

#-----------------------------------------------------------L'ajout d'un Nouveau Type de Speculation-----------------------------------------------------

    def add(self):
        self.root = Toplevel()
        self.root.geometry("396x200+450+190")
        self.root.title("Type d'opposition")
        self.root.resizable(0, 0)
        self.root.config(bg="#F7F9F9")

        label = LabelFrame(self.root, text="Nouveau type d'opposition", font=("Helvetica", 13), bg="#E3F3F3", width=380, height=185)
        label.place(x=8, y=8)

        libelleFr = Label(self.root, text="Libelle_Fr", font=("Helvetica", 12), bg="#E3F3F3")
        libelleFr.place(x=30, y=50)
        frm = Frame(self.root, bg="#4EB1FA", relief=FLAT, width=231, height=24)
        frm.place(x=130, y=50)
        self.libelleFr_entry = Entry(frm, relief=FLAT, width=25, font=("Helvetica", 12), bg="#F7F9F9")
        self.libelleFr_entry.place(x=1, y=1)

        libelleAr = Label(self.root, text="Libelle_Ar", font=("Helvetica", 12), bg="#E3F3F3")
        libelleAr.place(x=30, y=90)
        frm2 = Frame(self.root, bg="#4EB1FA", relief=FLAT, width=231, height=24)
        frm2.place(x=130, y=90)
        self.libelleAr_entry = Entry(frm2, relief=FLAT, width=25, font=("Helvetica", 12), bg="#F7F9F9", justify=RIGHT)
        self.libelleAr_entry.place(x=1, y=1)

        frm = Frame(self.root, bg="#379BF3", width=68, height=28)
        frm.place(x=170, y=140)
        spBtn = Button(frm, text="Ajouter", bg="#CEE6F3", font=("Times New Roman", 13), fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.ajouter)
        spBtn.place(x=1, y=1, height=26)

    def ajouter(self):
        if self.libelleFr_entry.get() != '':

            self.tpOppost.insertOppost(self.libelleFr_entry.get(), self.libelleAr_entry.get())

            self.tree.delete(*self.tree.get_children())

            typSpeclt = self.tpOppost.select()
            index = iid = 0
            for item in typSpeclt:
                self.tree.insert("", index, iid, values=item)
                index = iid = index + 1
            self.tree.selection_set(self.tree.get_children()[0])

            self.root.destroy()
        else:
            showerror("Oppostion", "Veuillez remplir le champ: Libelle Fr")

'''if __name__ == "__main__":
    app = AddOppostition()
    app.mainloop()'''