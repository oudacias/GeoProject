from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from UserAPP import Consistance_BE
from UserAPP import TypeSol_BE
from UserAPP import TypeSpecl_BE
from UserAPP import Parcelle_BE
from UserAPP import Douar_BE
from UserAPP import Personnes_BE
from UserAPP import Cles
from UserAPP import SousZone_BE
from UserAPP import Marche_BE
from UserAPP import Oppostition_BE
from Exceptions import PolygError
from Exceptions import IdError
from tkinter import messagebox
from UserAPP import DetailMap
from UserAPP import Rivrains_BE
from AdminAPP import Point_BE
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
import os
from AdminAPP import DatFile
from AdminAPP import XmlFile
from AdminAPP import Zn1_Word_Pdf
from AdminAPP import Zn2_Word_Pdf
from AdminAPP import Zn3_Word_Pdf
from AdminAPP import ST284_word_pdf
from AdminAPP import TabA_word_pdf
from AdminAPP import PV_word_pdf


# -------------------------------------------------------------------------------------- PLACEHOLDER -------------------------------------------------------------------
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

class ResearchPolyg_Ad(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Rechercher Parcelle")
        self.geometry("1100x620+150+45")
        self.resizable(0, 0)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.polyg = Parcelle_BE.Parcelle()
        self.dr = Douar_BE.Douar()
        self.cs = Consistance_BE.Consistance()
        self.prs = Personnes_BE.Personnes()
        self.tpSol = TypeSol_BE.TypeSol()
        self.specl = TypeSpecl_BE.TypeSpecul()

        self.buttonsFrame()
        self.researchFrame()
        self.canvasFrame()
        self.notebook()


                            # -------------------------- Buttons frame --------------------------------------
    def buttonsFrame(self):
        buttons_frame = Frame(self, bg="#FFFFFF", height=45)
        buttons_frame.pack(side=TOP, fill=X, pady=3)

        datFrm = Frame(buttons_frame, bg="#4EB1FA")
        datFrm.pack(side='left', padx=2, pady=2)
        datBtn = Button(datFrm, text="DAT", bg="#E3F3F3", fg="#0F8ED6", relief=FLAT, activebackground="#4EB1FA", activeforeground="#FFFFFF", command=self.dat)
        datBtn.pack(side='left', padx=1, pady=1)

        xmlFrm = Frame(buttons_frame, bg="#4EB1FA")
        xmlFrm.pack(side='left', padx=2, pady=2)
        xmlBtn = Button(xmlFrm, text="XML", bg="#E3F3F3", fg="#0F8ED6", relief=FLAT, activebackground="#4EB1FA", activeforeground="#FFFFFF", command=self.xml)
        xmlBtn.pack(side='left', padx=1, pady=1)

        zn1Frm = Frame(buttons_frame, bg="#4EB1FA")
        zn1Frm.pack(side='left', padx=2, pady=2)
        zn1Btn = Button(zn1Frm, text="ZN1", bg="#E3F3F3", fg="#0F8ED6", relief=FLAT, activebackground="#4EB1FA", activeforeground="#FFFFFF", command=self.zn1)
        zn1Btn.pack(side='left', padx=1, pady=1)

        zn2Frm = Frame(buttons_frame, bg="#4EB1FA")
        zn2Frm.pack(side='left', padx=2, pady=2)
        zn2Btn = Button(zn2Frm, text="ZN2", bg="#E3F3F3", fg="#0F8ED6", relief=FLAT, activebackground="#4EB1FA", activeforeground="#FFFFFF", command=self.zn2)
        zn2Btn.pack(side='left', padx=1, pady=1)

        zn3Frm = Frame(buttons_frame, bg="#4EB1FA")
        zn3Frm.pack(side='left', padx=2, pady=2)
        zn3Btn = Button(zn3Frm, text="ZN3", bg="#E3F3F3", fg="#0F8ED6", relief=FLAT, activebackground="#4EB1FA", activeforeground="#FFFFFF", command=self.zn3)
        zn3Btn.pack(side='left', padx=1, pady=1)

        zn4Frm = Frame(buttons_frame, bg="#4EB1FA")
        zn4Frm.pack(side='left', padx=2, pady=2)
        zn4Btn = Button(zn4Frm, text="ZN4", bg="#E3F3F3", fg="#0F8ED6", relief=FLAT, activebackground="#4EB1FA", activeforeground="#FFFFFF", command=self.zn4)
        zn4Btn.pack(side='left', padx=1, pady=1)

        pvFrm = Frame(buttons_frame, bg="#4EB1FA")
        pvFrm.pack(side='left', padx=2, pady=2)
        pvBtn = Button(pvFrm, text="PV", bg="#E3F3F3", fg="#0F8ED6", relief=FLAT, activebackground="#4EB1FA", activeforeground="#FFFFFF", command=self.pv)
        pvBtn.pack(side='left', padx=1, pady=1)

        tabAFrm = Frame(buttons_frame, bg="#4EB1FA")
        tabAFrm.pack(side='left', padx=2, pady=2)
        tabAbtn = Button(tabAFrm, text="TAB_A", bg="#E3F3F3", fg="#0F8ED6", relief=FLAT, activebackground="#4EB1FA", activeforeground="#FFFFFF", command=self.tabA)
        tabAbtn.pack(side='left', padx=1, pady=1)

        stFrm = Frame(buttons_frame, bg="#4EB1FA")
        stFrm.pack(side='left', padx=2, pady=2)
        st284 = Button(stFrm, text="ST284", bg="#E3F3F3", fg="#0F8ED6", relief=FLAT, activebackground="#4EB1FA", activeforeground="#FFFFFF", command=self.st284)
        st284.pack(side='left', padx=1, pady=1)


                                # ----------------------------- Frame pour chercher la parcelle ---------------------------------
    def researchFrame(self):
        top_frame = Frame(self, bg="white")
        top_frame.pack(side=TOP, fill=X)

        self.idPlgn = tk.Entry(top_frame, font=("Helvetica", 13), relief=FLAT, bg="#F7F9F9", width=40)
        self.idPlgn.pack(side=LEFT, padx=100, pady=2)
        add_placeholder_to(self.idPlgn, "Id parcelle")

        id_btn = Button(top_frame, text="Rechercher", bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, command=self.researchval)
        id_btn.pack(side=LEFT, padx=2, pady=2)

                                # ----------------------------- CANVAS Pour afficher la parcelle -------------------
    def canvasFrame(self):
        self.canv = Canvas(self, bg="#FFFFFF", width=350, height=547)
        self.canv.place(x=744, y=70)


                                # --------------------- NOTEBOOK Pour Afficher lla Parcelles Recherchée --------------
    def notebook(self):
        note = ttk.Notebook(self, height=520, width=735)
        note.place(x=3, y=70)


## **************************************** -- TAB1 -- INFORMATIONS GÉNÉRALES D'UNE PARCELLE
        self.tab1 = ttk.Frame(note)
        note.add(self.tab1, text='Parcelle')

        idparcel = Label(self.tab1, text="Parcelle Nº:", font=("Helvetica", 14))
        idparcel.place(x=10, y=20)
        self.idPolyg = Label(self.tab1, text="", font=("Helvetica", 14))
        self.idPolyg.place(x=120, y=20)

        label = Label(self.tab1, text="Propriete dite", font=("Helvetica", 12))
        label.place(x=35, y=70)
        self.parcel_Var = StringVar()
        self.parcel = Entry(self.tab1, textvariable=self.parcel_Var, width=22, font=("Helvetica", 12), relief=FLAT,bg="#F7F9F9")
        self.parcel.place(x=180, y=70)

        label = Label(self.tab1, text="الملك المسمى", font=("Helvetica", 12))
        label.place(x=630, y=70)
        self.parcelAr_Var = StringVar()
        self.parcelAr = Entry(self.tab1, textvariable=self.parcelAr_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.parcelAr.place(x=386, y=70)

        douar = Label(self.tab1, text="Douar", font=("Helvetica", 12))
        douar.place(x=62, y=110)
        self.douar_Var = StringVar()
        self.douarFR = Entry(self.tab1, textvariable=self.douar_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.douarFR.place(x=180, y=110)

        douar = Label(self.tab1, text="الدوار", font=("Helvetica", 12))
        douar.place(x=650, y=110)
        self.douarAr_Var = StringVar()
        self.douarAr = Entry(self.tab1, textvariable=self.douarAr_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.douarAr.place(x=386, y=110)

        srf = Label(self.tab1, text="Surface ", font=("Helvetica", 12))
        srf.place(x=56, y=150)
        self.area_Var = StringVar()
        self.areaFr = Entry(self.tab1, textvariable=self.area_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.areaFr.place(x=180, y=150)

        label = Label(self.tab1, text="المساحة", font=("Helvetica", 12))
        label.place(x=645, y=150)
        self.areaAr_Var = StringVar()
        self.areaAr = Entry(self.tab1, textvariable=self.areaAr_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.areaAr.place(x=386, y=150)

        brn = Label(self.tab1, text="Nombre des bornes", font=("Helvetica", 11))
        brn.place(x=40, y=190)
        self.born_Var = StringVar()
        self.born = Entry(self.tab1, textvariable=self.born_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.born.place(x=180, y=190)

        label = Label(self.tab1, text="Consistance", font=("Helvetica", 11))
        label.place(x=40, y=230)
        self.consist_Var = StringVar()
        self.consist = Entry(self.tab1, textvariable=self.consist_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.consist.place(x=180, y=230)

        tpspec = Label(self.tab1, text="Type de spéculation", font=("Helvetica", 12))
        tpspec.place(x=15, y=270)
        self.specul_Var = StringVar()
        self.specul = Entry(self.tab1, textvariable=self.specul_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.specul.place(x=180, y=270)

        tpsol = Label(self.tab1, text="Type de sol", font=("Helvetica", 12))
        tpsol.place(x=36, y=310)
        self.sol_Var = StringVar()
        self.sol = Entry(self.tab1, textvariable=self.sol_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.sol.place(x=180, y=310)

        label = Label(self.tab1, text="Date de l'enquête \n parcellaire", font=("Helvetica", 12))
        label.place(x=25, y=350)
        self.date_Var = StringVar()
        self.date = Entry(self.tab1, textvariable=self.date_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.date.place(x=180, y=350)


## **************************************** -- TAB2 -- PRÉSUMÉ ---------------------------------------------------------
        self.tab2 = ttk.Frame(note)
        note.add(self.tab2, text='Présumé')
        idpresume = Label(self.tab2, text="Présumé Nº:", font=("Helvetica", 14))
        idpresume.place(x=10, y=10)
        self.idprsm = Label(self.tab2, text="", font=("Helvetica", 12))
        self.idprsm.place(x=130, y=10)

        Prenom = Label(self.tab2, text="Prénom", font=("Helvetica", 12))
        Prenom.place(x=46, y=60)
        self.prnmFr_Var = StringVar()
        self.prnmFr = Entry(self.tab2, textvariable=self.prnmFr_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                            bg="#F7F9F9")
        self.prnmFr.place(x=158, y=60)

        PrenomAr = Label(self.tab2, text="الاسم الشخصي", font=("Helvetica", 12))
        PrenomAr.place(x=610, y=60)
        self.prnm_Var = StringVar()
        self.prnmAr = Entry(self.tab2, textvariable=self.prnm_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                            bg="#F7F9F9", justify=RIGHT)
        self.prnmAr.place(x=364, y=60)

        nom = Label(self.tab2, text="Nom", font=("Helvetica", 12))
        nom.place(x=56, y=100)
        self.nom_Var = StringVar()
        self.nomFr = Entry(self.tab2, textvariable=self.nom_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                           bg="#F7F9F9")
        self.nomFr.place(x=158, y=100)

        nomAr = Label(self.tab2, text="الاسم العائلي", font=("Helvetica", 12))
        nomAr.place(x=613, y=100)
        self.nomAr_Var = StringVar()
        self.nomAr = Entry(self.tab2, textvariable=self.nomAr_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                           bg="#F7F9F9", justify=RIGHT)
        self.nomAr.place(x=364, y=100)

        adress = Label(self.tab2, text="L'adresse", font=("Helvetica", 12))
        adress.place(x=40, y=140)
        self.address_Var = StringVar()
        self.address = Entry(self.tab2, textvariable=self.address_Var, width=22, font=("Helvetica", 12),
                             relief=FLAT, bg="#F7F9F9")
        self.address.place(x=158, y=140)

        adressAr = Label(self.tab2, text="العنوان", font=("Helvetica", 12))
        adressAr.place(x=626, y=140)
        self.addrAr_Var = StringVar()
        self.addr_Ar = Entry(self.tab2, textvariable=self.addrAr_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                             bg="#F7F9F9", justify=RIGHT)
        self.addr_Ar.place(x=364, y=140)

        tel = Label(self.tab2, text="Tel", font=("Helvetica", 12))
        tel.place(x=60, y=180)
        self.tel1_Var = StringVar()
        self.tel1 = Entry(self.tab2, textvariable=self.tel1_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                          bg="#F7F9F9")
        self.tel1.place(x=158, y=180)

        tel2 = Label(self.tab2, text="Tel 2", font=("Helvetica", 12))
        tel2.place(x=59, y=220)
        self.tel2_Var = StringVar()
        self.tel2 = Entry(self.tab2, textvariable=self.tel2_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                          bg="#F7F9F9")
        self.tel2.place(x=158, y=220)

        cin = Label(self.tab2, text="CIN", font=("Helvetica", 12))
        cin.place(x=60, y=260)
        self.cin_Var = StringVar()
        self.cin = Entry(self.tab2, textvariable=self.cin_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                         bg="#F7F9F9")
        self.cin.place(x=158, y=260)

        dateNss = Label(self.tab2, text="Date de naissance", font=("Helvetica", 12))
        dateNss.place(x=10, y=300)
        self.datNaiss_Var = StringVar()
        self.datNaiss = Entry(self.tab2, textvariable=self.datNaiss_Var, width=22, font=("Helvetica", 12),
                              relief=FLAT, bg="#F7F9F9")
        self.datNaiss.place(x=158, y=300)
## **************************************** -- TAB3 -- OPPOSANT
        self.tab3 = ttk.Frame(note)
        note.add(self.tab3, text='Opposant')

        self.tree = ttk.Treeview(self.tab3)
        self.tree.place(x=3, y=5, width=742, height=500)

        xsb = ttk.Scrollbar(self.tab3, orient='horizontal', command=self.tree.xview)
        xsb.place(x=3, y=500, width=742)
        self.tree['xscroll'] = xsb.set
        self.tree.configure(yscrollcommand=xsb.set)

        self.col_name = self.prs.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=120)
            self.tree.heading(c, text=self.col_name[c])

            index = iid = 0
            self.tree.insert("", index, iid, values="")
            index = iid = index + 1


## **************************************** -- TAB4 -- RIVRAINS
        self.tab4 = ttk.Frame(note)
        note.add(self.tab4, text='Rivrain')

        self.treev = ttk.Treeview(self.tab4)
        self.treev.place(x=3, y=5, width=742, height=500)

        xsb = ttk.Scrollbar(self.tab4, orient='horizontal', command=self.treev.xview)
        xsb.place(x=3, y=500, width=742)
        self.treev['xscroll'] = xsb.set
        self.treev.configure(yscrollcommand=xsb.set)

        self.rivr = Rivrains_BE.Rivrains()
        col_name = self.rivr.columnName()
        self.treev["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8")
        self.treev['show'] = 'headings'
        for c in range(len(self.treev["columns"])):
            self.treev.column(c, width=120)
            self.treev.heading(c, text=col_name[c])


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------AFFICHAGE DES VALEURS DE PARCELLES RECHÉRCHÉE ------------------------------------------
    def researchval(self):
        try:
            x = self.idPlgn.get()
            if x != '':
                try:
                    idval = self.polyg.verifyPolyg(self.idPlgn.get())
                    values = self.polyg.researchPolyg(self.idPlgn.get())
                    valDr = self.dr.selectDr(self.idPlgn.get())
                    valCons = self.cs.researPoly_Cons(self.idPlgn.get())
                    valSol = self.tpSol.researPoly_Sol(self.idPlgn.get())
                    valSpecul = self.specl.researPoly_Spec(self.idPlgn.get())
                    presVal = self.prs.researPres(self.idPlgn.get())

                    if idval == True:
                        start = DetailMap.DetailMap(self.canv, values[0])

                                            # ------------------------ VIDER LES INPUTS ------------------------
        # TAB 1/PARCELLE
                        self.idPolyg.config(text="")
                        self.parcel.delete(0, 'end')
                        self.parcelAr.delete(0, 'end')
                        self.douarFR.delete(0, 'end')
                        self.douarFR.delete(0, 'end')
                        self.areaFr.delete(0, 'end')
                        self.areaAr.delete(0, 'end')
                        self.born.delete(0, 'end')
                        self.consist.delete(0, 'end')
                        self.specul.delete(0, 'end')
                        self.sol.delete(0, 'end')
                        self.date.delete(0, 'end')
                        # TAB 2

                        self.prnmFr.delete(0, 'end')
                        self.prnmAr.delete(0, 'end')
                        self.nomFr.delete(0, 'end')
                        self.nomAr.delete(0, 'end')
                        self.address.delete(0, 'end')
                        self.addr_Ar.delete(0, 'end')
                        self.tel1.delete(0, 'end')
                        self.tel2.delete(0, 'end')
                        self.cin.delete(0, 'end')
                        self.datNaiss.delete(0, 'end')
        # TAB3
                        self.tree.delete(*self.tree.get_children())

        # TAB 4
                        self.treev.delete(*self.treev.get_children())


                                                            # ------------------------ AFFICHER LES VALEURS ------------------------
        # TAB 1 __ PARCELLE
                        self.idPolyg.config(text=str(values[0]))
                        self.parcel.insert(1, values[1])
                        self.parcelAr.insert(1, values[2])
                        self.douarFR.insert(1, valDr[0][0])
                        self.douarAr.insert(1, valDr[0][1])
                        # -- SURFACE_FR
                        if values[5] == None and values[6] == None and values[7] == None:
                            self.areaFr.insert(1, '0 Ha  ' + '0 a  ' + '0 ca')
                        elif values[5] == None:
                            self.areaFr.insert(1, '0 Ha  ' + str(values[6]) + 'a  ' + str(values[7]) + 'ca')
                        elif values[5] == None and values[6] == None:
                            self.areaFr.insert(1, '0 Ha  ' + '0 a  ' + str(values[7]) + 'ca')
                        elif values[5] == None and values[7] == None:
                            self.areaFr.insert(1, '0 Ha  ' + str(values[6]) + 'a  ' + '0 ca')
                        elif values[6] == None:
                            self.areaFr.insert(1, str(values[5]) + 'Ha  ' + '0 a  ' + str(values[7]) + 'ca')
                        elif values[6] == None and values[7] == None:
                            self.areaFr.insert(1, str(values[5]) + 'Ha  ' + '0 a  ' + '0 ca')
                        elif values[7] == None:
                            self.areaFr.insert(1, str(values[5]) + 'Ha  ' + str(values[6]) + 'a  ' + '0 ca')
                        else:
                            self.areaFr.insert(1,
                                               str(values[5]) + 'Ha  ' + str(values[6]) + 'a  ' + str(values[7]) + 'ca')

                        # -- SURFACE_AR
                        if values[5] == None and values[6] == None and values[7] == None:
                            self.areaAr.insert(1, '0' + ' ه' + '0' + ' ا' + '0' + 'س')
                        elif values[5] == None:
                            self.areaAr.insert(1, '0' + ' ه' + str(values[6]) + 'ا' + str(values[7]) + 'س')
                        elif values[5] == None and values[6] == None:
                            self.areaAr.insert(1, '0' + ' ه' + '0' + 'ا ' + str(values[7]) + 'س')
                        elif values[5] == None and values[7] == None:
                            self.areaAr.insert(1, '0' + ' ه' + str(values[6]) + ' ا' + '0' + ' س ')
                        elif values[6] == None:
                            self.areaAr.insert(1, str(values[5]) + 'ه' + '0' + ' ا' + str(values[7]) + 'س')
                        elif values[6] == None and values[7] == None:
                            self.areaAr.insert(1, str(values[5]) + 'ه' + '0' + ' ا' + '0' + ' س')
                        elif values[7] == None:
                            self.areaAr.insert(1, str(values[5]) + str(values[6]) + 'ا' + '0' + ' س')
                        else:
                            self.areaAr.insert(1, str(values[5]) + 'ه' + str(values[6]) + 'ا' + str(values[7]) + 'س')

                        # self.sfAr.config(text=str(values[5]) + 'ه  ' + str(values[6]) + 'ا  ' + str(values[7]) + 'س')
                        # self.nbrBrn.config(text="" + str(values[4]) + "")
                        self.born.insert(1, "" + str(values[4]) + "")
                        self.consist.insert(1, valCons[0])
                        self.specul.insert(1, valSpecul[0])
                        self.sol.insert(1, valSol[0])
                        self.date.insert(1, values[8])
                        # TAB 2
                        verifyPres = self.prs.verifyPersonne(self.idPlgn.get())
                        if verifyPres == True:
                            self.idprsm.config(text=str(presVal[0]))
                            self.prnmFr.insert(1, presVal[1])
                            self.prnmAr.insert(1, presVal[2])
                            self.nomFr.insert(1, presVal[3])
                            self.nomAr.insert(1, presVal[4])
                            self.address.insert(1, presVal[5])
                            self.addr_Ar.insert(1, presVal[6])

                            if presVal[8] == None or presVal[8] == 'null':
                                self.tel1.insert(1, '')
                            else:
                                self.tel1.insert(1, presVal[8])

                            if presVal[9] == None or presVal[9] == 'null':
                                self.tel2.insert(1, '')
                            else:
                                self.tel2.insert(1, presVal[9])

                            if presVal[7] == None or presVal[7] == 'null':
                                self.cin.insert(1, '')
                            else:
                                self.cin.insert(1, presVal[7])

                            if presVal[10] == None or presVal[10] == 'null':
                                self.datNaiss.insert(1, '')
                            else:
                                self.datNaiss.insert(1, presVal[10])
                        else:
                            msg = messagebox.showerror("Présumé", "Aucun présumé enregistré pour cette parcelle")
        # TAB 3
                        list = self.prs.researOppo(self.idPlgn.get())
                        index = iid = 0
                        # self.tree.tag_configure('RED_TAG', background="#FFFFFF", foreground="#14566D")
                        for item in list:
                            self.tree.insert("", index, iid, values=item)
                            index = iid = index + 1

        # TAB 4
                        list = self.rivr.researRiv(str(values[0]))
                        index = iid = 0
                        for item in list:
                            self.treev.insert("", index, iid, values=item)
                            index = iid = index + 1
                    else:
                        raise PolygError.PolygError
                except PolygError.PolygError:
                    msg = messagebox.showerror("Rechercher une parcelle", "La parcelle que vous avez choisi n'exsiste pas")
            else:
                raise IdError.IdError
        except IdError.IdError:
            msg2 = messagebox.showerror("Parcelles", "Veuillez saisir un ID")


# # -------------------------------------------------------------------------------------------------------------- FILES
# # --------------------------------------------------------------- XML
    def xml(self):
        top_xml = Element('parcelles')
        polyg = Parcelle_BE.Parcelle.polyg_xml(self, self.idPlgn.get())
        dr = Douar_BE.Douar.xmlDr(self, self.idPlgn.get())
        riv = Rivrains_BE.Rivrains.rivXml(self, self.idPlgn.get())
        prsm = Personnes_BE.Personnes.prsm_xml(self, self.idPlgn.get())
        pnt = Point_BE.Point_BE.numPt(self, self.idPlgn.get())
        cnst = Consistance_BE.Consistance.Const_xml(self, self.idPlgn.get())
        sol = TypeSol_BE.TypeSol.sol_xml(self, self.idPlgn.get())
        specl = TypeSpecl_BE.TypeSpecul.spec_xml(self, self.idPlgn.get())


# -- PARCELLE --
        tab = ['numParcelle', 'nomParcelleAR', 'nomParcelleFR', 'nombreBorne', 'surfCalculer', 'surfAdopter','surfaceHA', 'surfaceA', 'surfaceCA', 'adresseFR', 'adresseAR',
               'idSynchronisation', 'idDouar', 'fournisseurDonnee', 'idEnqueteurP', 'idEnqueteurJ', 'idValidateur','numeroOrdre', 'numero', 'Bornes', 'OppositionOpposants']
        middle_xml = SubElement(top_xml, 'parcelle')

        for j in range(len(tab)):
            sub = SubElement(middle_xml, tab[j])
            if tab[j] == 'numParcelle':
                sub.text = str(polyg[0][0])
            if tab[j] == 'nomParcelleAR':
                sub.text = str(polyg[0][2])
            if tab[j] == 'nomParcelleFR':
                sub.text = str(polyg[0][1])
            if tab[j] == 'nombreBorne':
                sub.text = str(polyg[0][14])
            if tab[j] == 'surfCalculer':
                sub.text = '0'
            if tab[j] == 'surfAdopter':
                sub.text = '0'
            if tab[j] == 'surfaceHA':
                if polyg[0][15] == None:
                    sub.text = '0'
                else:
                    sub.text = str(polyg[0][15])
            if tab[j] == 'surfaceA':
                if polyg[0][16] == None:
                    sub.text = '0'
                else:
                    sub.text = str(polyg[0][16])
            if tab[j] == 'surfaceCA':
                if polyg[0][17] == None:
                    sub.text = '0'
                else:
                    sub.text = str(polyg[0][17])
            if tab[j] == 'adresseFR':
                sub.text = str(dr[0][1])
            if tab[j] == 'adresseAR':
                sub.text = str(dr[0][2])
            if tab[j] == 'idSynchronisation':
                sub.text = '0'
            if tab[j] == 'idDouar':
                sub.text = str(dr[0][0])
            if tab[j] == 'idEnqueteurP':
                sub.text = '0'
            if tab[j] == 'idEnqueteurJ':
                sub.text = '0'
            if tab[j] == 'idValidateur':
                sub.text = '0'
            if tab[j] == 'numeroOrdre':
                if polyg[0][6] == None:
                    sub.text = '0'
                else:
                    sub.text = str(polyg[0][6])
            if tab[j] == 'numero':
                sub.text = '0'
            '''if tab[j] == 'Bornes ':
                sub.text = str(lgn[value][1])
            if tab[j] == 'OppositionOpposants ':
                sub.text = str(lgn[value][1])'''
# -- Rivrain --
            rivrn = ['description', 'Direction', 'Id_douar', 'Id_Riverain', 'num_parcelle ', 'pointDebutName', 'pointFinName', 'Type_Riverain', 'Adresse', 'CIN', 'Nom', 'Prenom', 'GSM ']
            pntDF = ['id_douar', 'name', 'num_parcelle', 'type']
        if polyg != '':
            sub = SubElement(middle_xml, 'Rivrains')
            subelmt = SubElement(sub, 'RiverainPersonnePhysiques')
            for r in range(len(riv)):
                prsmRiv = Personnes_BE.Personnes.prsm_xml(self, str(riv[r][1]))
                drPointD = Douar_BE.Douar.drRiv(self, str(riv[r][3]))
                drPointF = Douar_BE.Douar.drRiv(self, str(riv[r][4]))
                numPointD = Point_BE.Point_BE.numPoint(self, str(riv[r][3]))
                numPointF = Point_BE.Point_BE.numPoint(self, str(riv[r][4]))
                drRiv = Douar_BE.Douar.drRivPolyg(self, str(riv[r][1]))
                riv = Rivrains_BE.Rivrains.rivXml(self, self.idPlgn.get())

                subelmt2 = SubElement(subelmt, 'RiverainPersonnePhysiques')
                for rv in range(len(rivrn)):
                    subelmt3 = SubElement(subelmt2, rivrn[rv])
                    if rivrn[rv] == 'description':
                        subelmt3.text = ''
                    if rivrn[rv] == 'Direction':
                        subelmt3.text = str(riv[r][2])
                    if rivrn[rv] == 'Id_douar':
                        subelmt3.text = str(drRiv[0])
                    if rivrn[rv] == 'Id_Riverain':
                        subelmt3.text = str(riv[r][1])
                    if rivrn[rv] == 'num_parcelle':
                        subelmt3.text = '0'
                    if rivrn[rv] == 'pointDebutName':
                        subelmt3.text = numPointD[0]
                    if rivrn[rv] == 'pointFinName':
                        subelmt3.text = numPointF[0]
                    if rivrn[rv] == 'Type_Riverain':
                        subelmt3.text = 'Personne Physique'
                    if rivrn[rv] == 'Adresse':
                        subelmt3.text = prsmRiv[0][5]
                    if rivrn[rv] == 'CIN':
                        if prsmRiv[0][7] == None or prsmRiv[0][7] == 'null':
                            subelmt3.text = ''
                        else:
                            subelmt3.text = prsmRiv[0][7]
                    if rivrn[rv] == 'Nom':
                        subelmt3.text = prsmRiv[0][1]
                    if rivrn[rv] == 'Prenom':
                        subelmt3.text = prsmRiv[0][3]
                    if rivrn[rv] == 'GSM':
                        subelmt3.text = prsmRiv[0][8]
                pntD = SubElement(subelmt2, 'pointDebut')
                pntF = SubElement(subelmt2, 'pointFin')
                for p in range(len(pntDF)):
                    subelmt4 = SubElement(pntD, pntDF[p])
                    subelmt5 = SubElement(pntF, pntDF[p])
                    if pntDF[p] == 'id_douar':
                        subelmt4.text = drPointD[0]
                        subelmt5.text = drPointF[0]
                    if pntDF[p] == 'name':
                        subelmt4.text = numPointD[0]
                        subelmt5.text = numPointF[0]
                    if pntDF[p] == 'num_parcelle':
                        subelmt4.text = ''
                        subelmt5.text = ''
                    if pntDF[p] == 'type':
                        subelmt4.text = 'Personne Physique'
                        subelmt5.text = 'Personne Physique'

# -- Presume --
        prsTab = ['adresse', 'cin', 'nomAR', 'nomFR', 'nomPere', 'nomPereAR', 'prenomAR', 'prenomFR', 'tel']
        prs = SubElement(middle_xml, 'presumeParcelles')
        subPrs = SubElement(prs, 'presumeParcelle')
        subPrsm = SubElement(subPrs, 'presume')
        for pr in range(len(prsTab)):
            prsSubElmnt = SubElement(subPrsm, prsTab[pr])
            if prsTab[pr] == 'adresse':
                prsSubElmnt.text = str(prsm[0][5])
            if prsTab[pr] == 'cin':
                if prsm[0][7] == 'null' or prsm[0][7]== None:
                    prsSubElmnt.text = ''
                else:
                    prsSubElmnt.text = str(prsm[0][7])
            if prsTab[pr] == 'nomAR':
                prsSubElmnt.text = str(prsm[0][2])
            if prsTab[pr] == 'nomFR':
                prsSubElmnt.text = str(prsm[0][1])
            if prsTab[pr] == 'nomPere':
                prsSubElmnt.text = ''
            if prsTab[pr] == 'nomPereAR':
                prsSubElmnt.text = ''
            if prsTab[pr] == 'prenomAR':
                prsSubElmnt.text = str(prsm[0][4])
            if prsTab[pr] == 'prenomFR':
                prsSubElmnt.text = str(prsm[0][3])
            if prsTab[pr] == 'tel':
                if str(prsm[0][8]) == 'null' or str(prsm[0][8]) == None:
                    prsSubElmnt.text = ''
                elif str(prsm[0][8]) != '':
                    prsSubElmnt.text = str(prsm[0][8])
# -- parcelaire --
        prcTab = ['idDouar', 'nombreBorne', 'numParcelle', 'surfAdopter', 'surfCalculer', 'surfaceA',
                  'surfaceCA', 'surfaceHA', 'gId']
        pnts = ['id_douar', 'name', 'num_parcelle', 'partie', 'type']
        coord = ['x', 'y', 'z']
        prcel = SubElement(middle_xml, 'parcelaire')
        for pc in range(len(prcTab)):
            prcelSub = SubElement(prcel, prcTab[pc])
            if prcTab[pc] == 'idDouar':
                prcelSub.text = str(dr[0][0])
            if prcTab[pc] == 'nombreBorne':
                prcelSub.text = str(polyg[0][14])
            if prcTab[pc] == 'numParcelle':
                prcelSub.text = str(polyg[0][0])
            if prcTab[pc] == 'surfAdopter':
                prcelSub.text = '0'
            if prcTab[pc] == 'surfCalculer':
                prcelSub.text = '0'
            if prcTab[pc] == 'surfaceA':
                if polyg[0][13] == None:
                    prcelSub.text = '0'
                else:
                    prcelSub.text = str(polyg[0][13])
            if prcTab[pc] == 'surfaceCA':
                if polyg[0][14] == None:
                    prcelSub.text = '0'
                else:
                    prcelSub.text = str(polyg[0][14])
            if prcTab[pc] == 'surfaceHA':
                if polyg[0][12] == None:
                    prcelSub.text = '0'
                else:
                    prcelSub.text = str(polyg[0][12])
            if prcTab[pc] == 'gId':
                prcelSub.text = '0'
        pntPrcs = SubElement(prcel, 'pointParcellaires')
        for n in range(len(pnt)):
            parceValues = Point_BE.Point_BE.numPoint(self, str(pnt[n][0]))
            drPntParce = Douar_BE.Douar.drRiv(self, str(pnt[n][0]))
            pntPrc = SubElement(pntPrcs, 'pointParcellaire')
            for pn in range(len(pnts)):
                pntPrcElmnt = SubElement(pntPrc, pnts[pn])
                if pnts[pn] == 'id_douar':
                    pntPrcElmnt.text = drPntParce[0]
                if pnts[pn] == 'name':
                    pntPrcElmnt.text = parceValues[0]
                if pnts[pn] == 'num_parcelle':
                    pntPrcElmnt.text = str(polyg[0][0])
                if pnts[pn] == 'partie':
                    pntPrcElmnt.text = 'P1'
                if pnts[pn] == 'type':
                    pntPrcElmnt.text = parceValues[1]
            crdt = SubElement(pntPrc, 'coordinate')
            for crd in range(len(coord)):
                crdtElmnt = SubElement(crdt, coord[crd])
                if coord[crd] == 'x':
                    if parceValues[2] == 'null' or parceValues[2] == None:
                        crdtElmnt.text = ''
                    else:
                        crdtElmnt.text = str(float(parceValues[2]))
                if coord[crd] == 'y':
                    if parceValues[3] == 'null' or parceValues[3] == None:
                        crdtElmnt.text = ''
                    else:
                        crdtElmnt.text = str(float(parceValues[3]))
                if coord[crd] == 'z':
                    crdtElmnt.text = '0'

# -- DocParcelles --
        dcPrcel = SubElement(middle_xml, 'DocParcelles')

# -- Charges --
        chrg = SubElement(middle_xml, 'Charges')

# -- CONSISTANCE --
        consTab = ['codeConsistance', 'idSol', 'idSpeculation', 'libelle', 'libelleSol', 'libelleSpeculation']
        const = SubElement(middle_xml, 'Consistances')
        constElmnt = SubElement(const, 'Consistance')
        for cst in range(len(consTab)):
            constSubElmnt = SubElement(constElmnt, consTab[cst])
            if consTab[cst] == 'codeConsistance':
                constSubElmnt.text = str(cnst[0][0])
            if consTab[cst] == 'idSol':
                constSubElmnt.text = str(sol[0][0])
            if consTab[cst] == 'idSpeculation':
                constSubElmnt.text = str(specl[0][0])
            if consTab[cst] == 'libelle':
                constSubElmnt.text = cnst[0][1]
            if consTab[cst] == 'libelleSol':
                constSubElmnt.text = sol[0][1]
            if consTab[cst] == 'libelleSpeculation':
                constSubElmnt.text = specl[0][1]
        xml_write = minidom.parseString(ElementTree.tostring(top_xml, 'utf-8')).toprettyxml(indent="  ")
        try:
            filename = 'P'+str(polyg[0][0])+'.xml'
            filepath = os.path.join(os.path.join(os.path.expanduser('~')), 'desktop\IFE_PIECES\XML', filename)
            if not os.path.exists(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML')):
                os.makedirs(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML'))
            f = open(filepath, "w", encoding="utf-8")
            f.write(xml_write)
            f.close()
            XmlFile.XmlFile()
        except:
            msg = messagebox.showerror("XML", "Veuillez fermer le fichier")


# # -------------------------------------------------------------------------------------------------------------- FILES
# # --------------------------------------------------------------- DAT
    def dat(self):
        values = self.polyg.researchPolyg(self.idPlgn.get())
        Pnt = Point_BE.Point_BE()
        filename = '/P' +str(values[0])+'.dat'
        path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\DAT')
        fichier = open(path + filename, 'w')

        numPnt = Pnt.numPt(self.idPlgn.get())
        xy = Pnt.coord_XY(self.idPlgn.get())
        fichier.write(str(values[0]))
        fichier.write('\n')
        fichier.write('IFE\n')
        fichier.write('Mappe**\n')
        fichier.write(str(values[4]) + '\n')

        for n in range(len(numPnt)):
            fichier.write(str(xy[n]).replace("(", "").replace(",", "").replace(")", "") + "\n")
        fichier.write("\n"+"\n")
        fichier.close()
        DatFile.Acceueil()


# # -------------------------------------------------------------------------------------------------------------- FILES
# # --------------------------------------------------------------- ZN1
    def zn1(self):
        self.person = Personnes_BE.Personnes.prsm_xml(self, self.idPlgn.get())
        self.sz = SousZone_BE.SousZ.selectSZ(self, self.idPlgn.get())
        self.mrch = Marche_BE.Marche.info_marche(self)
        self.dr = Douar_BE.Douar.xmlDr(self, self.idPlgn.get())
        self.polyg = Parcelle_BE.Parcelle.researchPolyg(self, self.idPlgn.get())
        self.tpSol = TypeSol_BE.TypeSol.sol_xml(self, self.idPlgn.get())
        self.tpSpecl = TypeSpecl_BE.TypeSpecul.spec_xml(self, self.idPlgn.get())
        self.consist = Consistance_BE.Consistance.Const_xml(self, self.idPlgn.get())
        self.oppos = Cles.Cles.opposition_pieces(self, self.idPlgn.get())

        person1 = str(self.person[0][1])
        person3 = str(self.person[0][3])
        mrch1 = str(self.mrch[1])
        sz = str(self.sz[0][1])
        mrch0 = str(self.mrch[0])
        mrch2 = str(self.mrch[2])
        person5 = str(self.person[0][5])
        person7 = str(self.person[0][7])
        person8 = str(self.person[0][8])
        dr = str(self.dr[0][1])
        polyg0 = str(self.polyg[0])
        polyg1 = str(self.polyg[1])
        oppos1 = str(self.oppos[0])
        consis1 = str(self.consist[0][1])
        specul1 = str(self.tpSpecl[0][1])
        sol1 = str(self.tpSol[0][1])
        surf27 = str(self.polyg[5])
        Zn1_Word_Pdf.ZN1.word(self, person1, person3, mrch1, sz, mrch0, mrch2, person5, person7, person8, dr, polyg0, polyg1, oppos1, consis1, specul1, sol1, surf27)


# # -------------------------------------------------------------------------------------------------------------- FILES
# # --------------------------------------------------------------- ZN2
    def zn2(self):
        self.person = Personnes_BE.Personnes.prsm_xml(self, self.idPlgn.get())
        self.sz = SousZone_BE.SousZ.selectSZ(self, self.idPlgn.get())
        self.mrch = Marche_BE.Marche.info_marche(self)
        self.dr = Douar_BE.Douar.xmlDr(self, self.idPlgn.get())
        self.polyg = Parcelle_BE.Parcelle.researchPolyg(self, self.idPlgn.get())
        self.tpSol = TypeSol_BE.TypeSol.sol_xml(self, self.idPlgn.get())
        self.tpSpecl = TypeSpecl_BE.TypeSpecul.spec_xml(self, self.idPlgn.get())
        self.consist = Consistance_BE.Consistance.Const_xml(self, self.idPlgn.get())
        self.oppos = Cles.Cles.opposition_pieces(self, self.idPlgn.get())

        person1 = str(self.person[0][1])
        person3 = str(self.person[0][3])
        mrch1 = str(self.mrch[1])
        sz = str(self.sz[0][1])
        mrch0 = str(self.mrch[0])
        mrch2 = str(self.mrch[2])
        person5 = str(self.person[0][5])
        person7 = str(self.person[0][7])
        person8 = str(self.person[0][8])
        dr = str(self.dr[0][1])
        polyg0 = str(self.polyg[0])
        polyg1 = str(self.polyg[1])
        oppos1 = str(self.oppos[0])
        consis1 = str(self.consist[0][1])
        specul1 = str(self.tpSpecl[0][1])
        sol1 = str(self.tpSol[0][1])
        surf27 = str(self.polyg[5])
        Zn2_Word_Pdf.ZN2.word(self, person1, person3, mrch1, sz, mrch0, mrch2, person5, person7, person8, dr, polyg0, polyg1, oppos1, consis1, specul1, sol1, surf27)


# # -------------------------------------------------------------------------------------------------------------- FILES
# # --------------------------------------------------------------- ZN3
    def zn3(self):
        self.person = Personnes_BE.Personnes.prsm_xml(self, self.idPlgn.get())
        self.sz = SousZone_BE.SousZ.selectSZ(self, self.idPlgn.get())
        self.mrch = Marche_BE.Marche.info_marche(self)
        self.dr = Douar_BE.Douar.xmlDr(self, self.idPlgn.get())
        self.polyg = Parcelle_BE.Parcelle.researchPolyg(self, self.idPlgn.get())
        self.polygon = Parcelle_BE.Parcelle.polyg_xml(self, self.idPlgn.get())
        self.tpSol = TypeSol_BE.TypeSol.sol_xml(self, self.idPlgn.get())
        self.tpSpecl = TypeSpecl_BE.TypeSpecul.spec_xml(self, self.idPlgn.get())
        self.consist = Consistance_BE.Consistance.Const_xml(self, self.idPlgn.get())
        self.oppos = Cles.Cles.opposition_pieces(self, self.idPlgn.get())
        self.motifOpp = Oppostition_BE.TypeOppos.motif_Opp(self, self.idPlgn.get())

        person1 = str(self.person[0][1])
        person3 = str(self.person[0][3])
        mrch1 = str(self.mrch[1])
        sz = str(self.sz[0][1])
        mrch0 = str(self.mrch[0])
        mrch2 = str(self.mrch[2])
        person5 = str(self.person[0][5])
        person7 = str(self.person[0][7])
        person8 = str(self.person[0][8])
        dr = str(self.dr[0][1])
        polyg0 = str(self.polyg[0])
        polyg1 = str(self.polyg[1])
        motifOps = str(self.motifOpp)
        Zn3_Word_Pdf.ZN3.word(self, person1, person3, mrch1, sz, mrch0, mrch2, person5, person7, person8, dr, polyg0, polyg1, motifOps)


# # -------------------------------------------------------------------------------------------------------------- FILES
# # --------------------------------------------------------------- ZN4
    def zn4(self):
        pass


# # -------------------------------------------------------------------------------------------------------------- FILES
# # --------------------------------------------------------------- ST284
    def st284(self):
        nomParcel = str(self.polygon[0][1])
        requis = str(self.polygon[0][10])
        titr = str(self.polygon[0][11])
        numParcel = str(self.polygon[0][0])
        ST284_word_pdf.ST284.word(self, nomParcel, requis, titr, numParcel)



# # -------------------------------------------------------------------------------------------------------------- FILES
# # --------------------------------------------------------------- TAB-A
    def tabA(self):
        nomParcel = str(self.polygon[0][1])
        requis = str(self.polygon[0][10])
        titr = str(self.polygon[0][11])
        numParcel = str(self.polygon[0][0])
        TabA_word_pdf.TabA.word(self, nomParcel, requis, titr, numParcel)


# # -------------------------------------------------------------------------------------------------------------- FILES
# # --------------------------------------------------------------- PV
    def pv(self):
        self.polygon = Parcelle_BE.Parcelle.polyg_xml(self, self.idPlgn.get())
        numParcel = str(self.polygon[0][0])
        PV_word_pdf.PV.word(self, numParcel)


#app = ResearchPolyg_Ad()
#app.mainloop()