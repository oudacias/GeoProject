import tkinter as tk
from tkinter import *
from AdminAPP import XML
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from UserAPP import Douar_BE
from UserAPP import Parcelle_BE
from AdminAPP import Point_BE
from UserAPP import Personnes_BE
from AdminAPP import Rivrain_BE
from UserAPP import Consistance_BE
from UserAPP import TypeSpecl_BE
from UserAPP import TypeSol_BE

class Confirm():

    def __init__(self, root):
        self.newroot = root
        root.geometry("450x250")
        root.title("HEllo")
        btn = Button(self.newroot, text="Ajouter à la liste", pady=12, command=self.buttonSelection).grid(row=5, column=1)
    def buttonSelection(self):
        XML.Export_Xml().xmlFile()
        print("g")
        self.newroot.destroy()




    # def __init__(self):
    #     self.neWroot = tk.Toplevel()
    #     self.neWroot.geometry("450x250")
    #     self.neWroot.title("HEllo")
    #     btn = Label(self.neWroot, text="Ajouter à la liste", pady=12).grid(row=3, column=1)
    #     btn1 = Button(self.neWroot, text="Exporter", pady=12, command=self.export).grid(row=5, column=1)
    #     btn2 = Button(self.neWroot, text="Annuler", pady=12, command=self.annuler).grid(row=5, column=2)
    # def export(self):
    #     f = open("Toutes_les_parcelles8.xml", "w", encoding="utf-8")
    #     f.write("xml_write")
    #     f.close()
    #     print("hey")
    #     self.neWroot.destroy()
    # def annuler(self):
    #     self.neWroot.destroy()


# root = tk.Tk()
# acc = Confirm(root)
# root.mainloop()



