import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import *
import os
from PIL import Image, ImageTk
from UserAPP import SousZone_BE

class AddSousZone(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("IFE_GIS")
        self.geometry("800x450+240+100")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.config(bg="#F7F9F9")

        self.sz = SousZone_BE.SousZ()

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

        col_name = self.sz.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=100)
            self.tree.heading(c, text=col_name[c])

        consists = self.sz.select()
        index = iid = 0
        for item in consists:
            self.tree.insert("", index, iid, values=item)
            index = iid = index + 1
        #self.tree.selection_set(self.tree.get_children()[0])

        self.tree.bind("<Double-1>", self.OnDoubleClick)


                                                # ---------------------- AFFICHAGE DE LIGNE SELECTIONNEE -------------------
    def OnDoubleClick(self, event):
        try:
            self.row_selected = self.tree.item(self.tree.selection())
            value = self.row_selected['values'][0]
            verf = self.sz.verifySZ(str(value))
            if verf == True:
                self.root = tk.Tk()
                self.root.title("Sous-Zone")
                self.root.resizable(0, 0)
                self.root.geometry("345x135+450+190")
                self.root.config(bg="#F7F9F9")
                self.frameDoubleClick()
            elif verf == False:
                showerror("Sous Zone", "Veuillez sélectionner une sous zone")
        except:
             showerror("Sous Zone", "Veuillez sélectionner une sous zone")


    def frameDoubleClick(self):

        frame_labels = LabelFrame(self.root, text="Modifier/Supprimer", font=("Helvetica", 13), bg="#E3F3F3")
        frame_labels.place(x=8, y=7, width=330, height=120)

        self.row_selected = self.tree.item(self.tree.selection())
        value = self.row_selected['values'][0]
        colonnes = self.sz.select_colName()
        valeurs = self.sz.select_colValue(str(value))

        i =0
        self.h = [None] * len(colonnes)
        for j in range(len(colonnes)):
            label = tk.Label(frame_labels, text=''.join(colonnes[j]), font="Helvetica", pady=10, padx=20, bg="#E3F3F3").grid(row=i+2, column=0)
            nb = StringVar()
            nb.set(i)

            self.h[i] = Entry(frame_labels, textvariable=nb, relief=FLAT, width=23, font=("Helvetica", 12), bg="#F7F9F9")
            self.h[i].insert(1, valeurs[0][j])
            self.h[i].grid(row=i+2, column=1)
            i = i+1

            frm2 = Frame(frame_labels, bg="#379BF3", width=78, height=28)
            frm2.place(x=125, y=60)
            button = Button(frm2, text="Modifier", bg="#CEE6F3", font=("Times New Roman", 13), fg="#379BF3", relief='flat', activebackground="#379BF3", activeforeground="#FFFFFF",  command=self.modification)
            button.place(x=1, y=1, height=26)

                                                        #--------------------- MODIFICATION -----------------
    def modification(self):
        if self.h[0].get() != '':
            tab = []
            for i in range(len(self.h)):
                tab.append(self.h[i].get())
            self.sz.update_colValue(tab, str(self.row_selected['values'][0]))

            x = self.tree.selection()[0]
            self.tree.delete(*self.tree.get_children())

            consists = self.sz.select()
            index = iid = 0
            for item in consists:
                self.tree.insert("", index, iid, values=item)
                index = iid = index + 1
            self.root.destroy()
        else:
            showerror("Sous Zone", "Veuillez remplir le champ")

'''if __name__ == "__main__":
    app = AddSousZone()
    app.mainloop()'''
