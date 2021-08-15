import os
import tkinter as tk
from tkinter import *
from Synchronisation import FromClt_Client
from UserAPP import Consistance
from UserAPP import Deconnecte
from UserAPP import DeletePolyg
from UserAPP import Douar
from UserAPP import Lastpolygon
from UserAPP import Map_Usr
from UserAPP import ModifyPolyg
from UserAPP import PolygList_USER
from UserAPP import Receive_User
from UserAPP import ResearchPolyg
from UserAPP import SousZone
from UserAPP import TypeSol
from UserAPP import TypeSpecl

class MainUser(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("User")
        self.wm_state(newstate="zoomed")
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        container = tk.Frame(self)
        container.pack(side="bottom", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

# ******************* TOOLBAR ***********************
        toolbar = Frame(self, bg="#FFFFFF")
        toolbar.pack(fill=X)
        project_directory = os.path.abspath(os.curdir)

        lst = project_directory + "/icons/list.png"
        self.lstImg = PhotoImage(file=lst)
        lstBtn = Button(toolbar, image=self.lstImg, relief=FLAT, bg="#FFFFFF", activebackground="#FFFFFF",
                        command=lambda: self.show_frame('PolygList'))
        lstBtn.pack(side=LEFT, padx=2, pady=2)

        map = project_directory + "/icons/map-location.png"
        self.mapImg = PhotoImage(file=map)
        mapBtn = Button(toolbar, image=self.mapImg, relief=FLAT, bg="#FFFFFF", activebackground="#FFFFFF",
                        command=lambda: self.show_frame('Map'))
        mapBtn.pack(side=LEFT, padx=2, pady=2)

        self.ltck = project_directory + "/icons/last-track.png"
        self.lasttrack = PhotoImage(file=self.ltck)
        lstP = tk.Button(toolbar, image=self.lasttrack, relief='flat', bg="#FFFFFF", activebackground="#FFFFFF",
                         command=Lastpolygon.Lastpolygon)
        lstP.pack(side='left', padx=2, pady=2)
                                                # ************************* MENUBAR ***************************
        menuBar = Menu(self)
        self.config(menu=menuBar)

        Marche_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        #Marche_menu.add_command(label="Changer le marché", command=ChangeProject.Change_Project)
        Marche_menu.add_command(label="Se déconnecter", command=Deconnecte.Deconnecte)
        menuBar.add_cascade(label="Marché", menu=Marche_menu)

        Parcelle_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        Parcelle_menu.add_command(label="Liste parcelles", command=lambda: self.show_frame('PolygList'))
        Parcelle_menu.add_command(label="Mappe", command=lambda: self.show_frame('Map'))
        Parcelle_menu.add_command(label="Dernière parcelle", command=Lastpolygon.Lastpolygon)
        Parcelle_menu.add_command(label="Recherche parcelle", command=ResearchPolyg.ResearchPolyg)
        Parcelle_menu.add_command(label="Modifier", command=ModifyPolyg.ModifyPolyg)
        Parcelle_menu.add_command(label="Supprimer", command=DeletePolyg.DeletePolyg)
        menuBar.add_cascade(label="Parcelle", menu=Parcelle_menu)

        synch_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        synch_menu.add_command(label="Envoyer", command=FromClt_Client.SynchClientJr.sendData)
        synch_menu.add_command(label="Recevoir", command=Receive_User.ReceiveDB)
        menuBar.add_cascade(label="Synchroniser", menu=synch_menu)

        options_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        options_menu.add_command(label="Sous-Zone", command=SousZone.AddSousZone)
        options_menu.add_command(label="Douar", command=Douar.AddDouar)
        options_menu.add_command(label="Consistance", command=Consistance.AddConsistance)
        options_menu.add_command(label="Type sol", command=TypeSol.Addtypesol)
        options_menu.add_command(label="Type spéculation", command=TypeSpecl.Addspeculation)
        menuBar.add_cascade(label="Autres options", menu=options_menu)

        self.frames = {}

        for F in (Map_Usr.Map, PolygList_USER.PolygList):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Map")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    m = MainUser()
    m.mainloop()


