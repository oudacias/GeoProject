from tkinter import *
from UserAPP import Consistance_BE
from UserAPP import TypeSol_BE
from UserAPP import TypeSpecl_BE
from UserAPP import Parcelle_BE
from UserAPP import Douar_BE
from UserAPP import Marche_BE
from UserAPP import Personnes_BE
from UserAPP import DetailMap
from  UserAPP import Map_BE
from tkinter import ttk
from tkinter import messagebox
from Exceptions import PolygError
from UserAPP import Rivrains_BE

root = Tk()

parcelle = Parcelle_BE.Parcelle()
mrch = Marche_BE.Marche()
nbrlgn = parcelle.lignesNumb()
mrche = mrch.mrchName()

etatBar = Frame(root, bg="#FFFFFF", height=22)
etatBar.grid(row=2, column=0, sticky='nsew', columnspan=2)
lgn = Label(etatBar, text="marché", font=("Helvetica", 10), bg="#FFFFFF")
lgn.place(x=10)


etatBar2 = Frame(root, bg="#14566D", height=20)
etatBar2.grid(row=0, column=0, sticky='ew')


treeV = ttk.Treeview(root)
treeV.grid(row=1, column=0, sticky='ew')

ysb = ttk.Scrollbar(root, orient='vertical', command=treeV.yview)
ysb.grid(row=0, column=1, sticky='ns')
xsb = ttk.Scrollbar(root, orient='horizontal', command=treeV.xview)
xsb.grid(row=1, column=0, sticky='ew', columnspan=2)
treeV['yscroll'] = ysb.set
treeV['xscroll'] = xsb.set

root.mainloop()