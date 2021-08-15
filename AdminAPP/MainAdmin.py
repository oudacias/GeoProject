import os
import tkinter as tk
from tkinter import *

from AdminAPP import AccountManag
from AdminAPP import DAT
from AdminAPP import DatFile
from AdminAPP import EtatParce
from AdminAPP import ExcelFile
from AdminAPP import ExportDat
from AdminAPP import ExportEXCEL
from AdminAPP import ExportXml
from AdminAPP import GererBrigades
from AdminAPP import ImporTitres
from AdminAPP import ImportCoord
from AdminAPP import Marche_Info
from AdminAPP import NewMachine
from AdminAPP import NewProject
from AdminAPP import PH1
from AdminAPP import PH8
from AdminAPP import ParcellaireFile
from AdminAPP import Ph1File
from AdminAPP import Ph8File
from AdminAPP import PolygList_AD
from AdminAPP import Pv
from AdminAPP import ResearchPolyg_Ad, Map
from AdminAPP import ST284
from AdminAPP import TabA
from AdminAPP import XL
from AdminAPP import XML
from AdminAPP import XmlFile
from AdminAPP import Zn1
from AdminAPP import Zn2
from AdminAPP import Zn3
from AdminAPP import Zn4
from Synchronisation import FromClt_Server
from UserAPP import Change
from UserAPP import Consistance
from UserAPP import Deconnecte
from UserAPP import DeletePolyg
from UserAPP import Douar
from UserAPP import Lastpolygon
from UserAPP import Marche_BE
from UserAPP import ModifyPolyg
from UserAPP import Opposition
from UserAPP import SousZone
from UserAPP import TypeSol
from UserAPP import TypeSpecl
from AdminAPP import Send_Admin

class MainAdmin(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Admin")
        self.wm_state(newstate="zoomed")
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        container = tk.Frame(self)
        container.pack(side=BOTTOM, fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

                                            # ******************* TOOLBAR ***********************
        toolbar = Frame(self, bg="#FFFFFF")
        toolbar.pack(fill=X, side=TOP)
        project_directory = os.path.abspath(os.curdir)

        lst = project_directory + "/icons/list.png"
        self.lstImg = PhotoImage(file=lst)
        lstBtn = Button(toolbar, image=self.lstImg, relief=FLAT, bg="#FFFFFF", activebackground="#FFFFFF", command=lambda: self.show_frame('PolygList'))
        lstBtn.pack(side=LEFT, padx=2, pady=2)

        map = project_directory + "/icons/map-location.png"
        self.mapImg = PhotoImage(file=map)
        mapBtn = Button(toolbar, image=self.mapImg, relief=FLAT, bg="#FFFFFF", activebackground="#FFFFFF", command=lambda: self.show_frame('Map'))
        mapBtn.pack(side=LEFT, padx=2, pady=2)

        self.ltck = project_directory + "/icons/last-track.png"
        self.lasttrack = PhotoImage(file=self.ltck)
        lstP = tk.Button(toolbar, image=self.lasttrack, relief='flat', bg="#FFFFFF", activebackground="#FFFFFF", command= Lastpolygon.Lastpolygon)
        lstP.pack(side='left', padx=2, pady=2)
        xml = project_directory + "/icons/xml.png"
        self.xmlImg = PhotoImage(file=xml)
        xmlBtn = Button(toolbar, image=self.xmlImg, relief=FLAT, bg="#FFFFFF", activebackground="#FFFFFF", command=self.xmlFile)
        xmlBtn.pack(side=LEFT, padx=2, pady=2)

        datF = project_directory + "/icons/dat-format.png"
        self.datImg = PhotoImage(file=datF)
        datBtn = Button(toolbar, image=self.datImg, relief=FLAT, bg="#FFFFFF", activebackground="#FFFFFF", command=self.datFile)
        datBtn.pack(side=LEFT, padx=2, pady=2)

        xlsFl = project_directory + "/icons/xls.png"
        self.xlsImg = PhotoImage(file=xlsFl)
        xlsBtn = Button(toolbar, image=self.xlsImg, relief=FLAT, bg="#FFFFFF", activebackground="#FFFFFF", command=self.excelFile)
        xlsBtn.pack(side=LEFT, padx=2, pady=2)


                                                # ************************* MENUBAR ***************************
        menuBar = Menu(self)
        self.config(menu=menuBar)

        self.mrch = Marche_BE.Marche()
        dbVal = self.mrch.dbCombbx()

        Marche_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        Marche_menu.add_command(label="Marché", command=Marche_Info.Info_Marche)
        Marche_menu.add_command(label="Nouveau marché", command=NewProject.NewProject)
        #Marche_menu.add_command(label="Nouveau marché", command=trialRestart.RestartApp)
        #Marche_menu.add_command(label="Nouveau marché", command=lambda: os.execv(sys.executable, [sys.executable, os.path.join(sys.path[0], " __ExportXml__")] + sys.argv[1:]))
        '''self.sub1 = Menu(Marche_menu, tearoff=0)
        Marche_menu.add_cascade(label='Changer le marché', menu=self.sub1)
        self.radio = StringVar()
        for db in dbVal:
            self.sub1.add_radiobutton(label=db, variable=self.radio, command=self.OnDoubleClick)'''

        Marche_menu.add_command(label="Se déconnecter", command=Deconnecte.Deconnecte)
        menuBar.add_cascade(label='March'+chr(233), menu=Marche_menu)

        Parcelle_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        Parcelle_menu.add_command(label="Liste parcelles", command=lambda: self.show_frame('PolygList'))
        Parcelle_menu.add_command(label="Mappe", command=lambda: self.show_frame('Map'))
        Parcelle_menu.add_command(label="Dernière parcelle", command=Lastpolygon.Lastpolygon)
        Parcelle_menu.add_command(label="Recherche parcelle", command=ResearchPolyg_Ad.ResearchPolyg_Ad)
        Parcelle_menu.add_command(label="Modifier", command=ModifyPolyg.ModifyPolyg)
        Parcelle_menu.add_command(label="Supprimer", command=DeletePolyg.DeletePolyg)
        menuBar.add_cascade(label="Parcelle", menu=Parcelle_menu)

        import_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        import_menu.add_command(label="Cordonnées définitives", command=ImportCoord.ImportCoord)
        import_menu.add_command(label="Titre/Réquisition", command=ImporTitres.ImporTitres)
        menuBar.add_cascade(label="Importer", menu=import_menu)

        export_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        export_menu.add_command(label="XLS", command=ExportEXCEL.ExportXls)
        export_menu.add_command(label="XML", command=ExportXml.ExportXml)
        export_menu.add_command(label="DAT", command=ExportDat.ExportDat)
        menuBar.add_cascade(label="Exporter", menu=export_menu)

        generer_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        generer_menu.add_command(label="ZN1", command=Zn1.Zn1)
        generer_menu.add_command(label="ZN2", command=Zn2.Zn2)
        generer_menu.add_command(label="ZN3", command=Zn3.Zn3)
        generer_menu.add_command(label="ZN4", command=Zn4.Zn4)
        generer_menu.add_command(label="PV", command=Pv.Pv)
        generer_menu.add_command(label="TAB_A", command=TabA.TAB_A)
        generer_menu.add_command(label="ST_284", command=ST284.ST284)
        generer_menu.add_command(label="ETAT PARCELLAIRE", command=self.etatParcellaire)
        generer_menu.add_command(label="PH_1", command=self.ph1)
        generer_menu.add_command(label="PH_8", command=self.ph8)
        menuBar.add_cascade(label="Générer", menu=generer_menu)

        synch_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        synch_menu.add_command(label="Ajouter une machine", command=NewMachine.AddMachine)
        synch_menu.add_command(label="Envoyer", command=Send_Admin.SendDB)
        synch_menu.add_command(label="Recevoir", command=FromClt_Server.SynchClientJr.receiveData)
        menuBar.add_cascade(label="Synchroniser", menu=synch_menu)

        options_menu = Menu(menuBar, tearoff=0, background='#CEE6F3', foreground='#0D3F59', activebackground='#1399E4', activeforeground='#FFFFFF')
        options_menu.add_command(label="Gérer les utilisateurs", command=AccountManag.AddAccount)
        options_menu.add_command(label="Gérer les brigades", command=GererBrigades.GererBrigd)
        options_menu.add_command(label="Sous-Zone", command=SousZone.AddSousZone)
        options_menu.add_command(label="Douar", command=Douar.AddDouar)
        options_menu.add_command(label="Consistance", command=Consistance.AddConsistance)
        options_menu.add_command(label="Type sol", command=TypeSol.Addtypesol)
        options_menu.add_command(label="Type spéculation", command=TypeSpecl.Addspeculation)
        options_menu.add_command(label="Type d'opposition", command=Opposition.AddOppostition)
        menuBar.add_cascade(label="Autres options", menu=options_menu)

        self.frames = {}

        for F in (Map.Map, PolygList_AD.PolygList):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Map")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def OnDoubleClick(self):
        command = self.mrch.connect_marche(self.radio.get())
        x = self.title()
        self.p = Change.ChangerMarche(x)
        self.destroy()

    '''def xmlConfim(self):
        root = tk.Tk()
        acc = XmlConfirmation.Confirm(root)
        root.mainloop()'''

    def datFile(self):
        DAT.Dat_Polygs().dat_file()
        DatFile.Acceueil()

    def xmlFile(self):
        XML.Export_Xml().xmlFile()
        XmlFile.XmlFile()

    def excelFile(self):
        XL.Exl_Polygs().exl()
        ExcelFile.XL_File()

    def ph1(self):
        PH1.Reper_Ph1().ph1()
        p1 = Ph1File.Acceueil()

    def ph8(self):
        PH8.Reper_Ph8().ph8()
        p8 = Ph8File.Acceueil()

    def etatParcellaire(self):
        EtatParce.EtatParcellaire().etat_parce()
        x = ParcellaireFile.Acceueil()


'''
python = sys.executable
os.execl(python, python, *sys.argv)
'''

if __name__ == "__main__":
    m = MainAdmin()
    m.mainloop()
