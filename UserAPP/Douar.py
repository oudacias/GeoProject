import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import *
from UserAPP.Douar_BE import Douar

class AddDouar(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Douar")
        self.geometry("801x450+240+100")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.config(bg="#F7F9F9")

        self.dr = Douar()

# -------------------------------------------------------------TREEVIEW-------------------------------------------------
        global tree
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview", background="#FFFFFF", foreground="#14566D")
        style.configure("Treeview.Heading", background="#B0D9E8", foreground="#14566D")

        self.tree = ttk.Treeview(self)
        self.tree.place(x=5, y=5, width=778, height=425)

        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        ysb.place(x=782, y=5, height=439)

        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        xsb.place(x=5, y=430, width=778)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        col_name = self.dr.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4", "5")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=100)
            self.tree.heading(c, text=col_name[c])

        douars = self.dr.select()
        index = iid = 0
        for item in douars:
            self.tree.insert("", index, iid, values=item)
            index = iid = index + 1
        #self.tree.selection_set(self.tree.get_children()[0])

        self.tree.bind("<Double-1>", self.OnDoubleClick)


                                                # ---------------------- AFFICHAGE DE LIGNE SELECTIONNEE -------------------
    def OnDoubleClick(self, event):
        try:
            self.row_selected = self.tree.item(self.tree.selection())
            value = self.row_selected['values'][0]
            verf = self.dr.verifyDr(str(value))
            if verf == True:
                self.root = tk.Tk()
                self.root.title("Douar")
                self.root.resizable(0, 0)
                self.root.geometry("370x187+450+190")
                self.root.config(bg="#F7F9F9")
                self.frameDoubleClick()
            elif verf == False:
                showerror("Douar", "Veuillez sélectionner un douar")
        except:
            showerror("Douar", "Veuillez sélectionner un douar")

    def frameDoubleClick(self):
        frame_labels = LabelFrame(self.root, text="Modifier/Supprimer", font=("Helvetica", 13), bg="#F7F9F9")
        frame_labels.place(x=10, y=7, width=350, height=170)

        self.row_selected = self.tree.item(self.tree.selection())
        value = self.row_selected['values'][0]
        colonnes = self.dr.select_colName()
        valeurs = self.dr.select_colValue(str(value))

        i =0
        self.h = [None] * len(colonnes)
        for j in range(len(colonnes)):
            label = tk.Label(frame_labels, text=''.join(colonnes[j]), font="Helvetica", pady=10, padx=20, bg="#F7F9F9").grid(row=i+2, column=0)
            nb = StringVar()
            nb.set(i)
            frm = Frame(frame_labels, bg="#4EB1FA", bd=1, relief=FLAT, width=40)
            frm.grid(row=i+2, column=1)
            if i == 1:
                self.h[i] = Entry(frm, textvariable=nb, relief=FLAT, width=32, justify=RIGHT)
            else:
                self.h[i] = Entry(frm, textvariable=nb, relief=FLAT, width=32)
            self.h[i].insert(1, valeurs[0][j])
            self.h[i].grid(row=i+2, column=1)
            i = i+1
            button = Button(frame_labels, text="Modifier", command=self.modification, font=("Times New Roman", 11), bg="#4EB1FA",fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
            button.place(x=110, y=100)
            button = Button(frame_labels, text="Supprimer", command=self.suppr, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
            button.place(x=180, y=100)


                                                        #--------------------- MODIFICATION -----------------
    def modification(self):
        if self.h[0].get() != '':
            tab = []
            for i in range(len(self.h)):
                tab.append(self.h[i].get())
            self.dr.update_colValue(tab, str(self.row_selected['values'][0]))

            x = self.tree.selection()[0]
            self.tree.delete(*self.tree.get_children())

            douars = self.dr.select()
            index = iid = 0
            for item in douars:
                self.tree.insert("", index, iid, values=item)
                index = iid = index + 1
            self.root.destroy()
        else:
            showerror("Douar", "Veuillez remplir le champ")


                                            #--------------------- SUPPRESSION --------------------
    def suppr(self):
        self.popinfos = tk.Toplevel()
        self.popinfos.title('Suppression')
        self.popinfos.resizable(0, 0)
        self.popinfos.config(bg="#F7F9F9")
        self.popinfos.geometry("360x120+500+300")
        label = tk.Label(self.popinfos, text="Voulez-vous supprimer ce douar?", font=("Helvetica", 12), pady=13, padx=20, bg="#F7F9F9").place(x=45, y=15)
        btn1 = tk.Button(self.popinfos, text='Oui', command=self.supprimer, font=("Times New Roman", 11), bg="#4EB1FA",fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
        btn1.place(x=148, y=70)
        btn2 = tk.Button(self.popinfos, text='Non', command=self.annuler, font=("Times New Roman", 11), fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
        btn2.place(x=200, y=70)
    def supprimer(self):
        self.dr.deleteDr(str(self.row_selected['values'][0]))
        self.root.destroy()
        self.popinfos.destroy()
        x = self.tree.selection()[0]
        self.tree.delete(x)

    def annuler(self):
        self.root.destroy()
        self.popinfos.destroy()

'''if __name__ == "__main__":
    app = AddDouar()
    app.mainloop()'''
