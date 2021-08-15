from tkinter import *
import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog
from AdminAPP import Exportation_BE
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from tkinter import messagebox
from UserAPP import Cles
from tkcalendar import Calendar, DateEntry
from UserAPP import Parcelle_BE
from UserAPP import SousZone_BE
from UserAPP import Personnes_BE
from UserAPP import Douar_BE
from AdminAPP import User_BE
from AdminAPP import Rivrain_BE
from AdminAPP import Point_BE
from UserAPP import Consistance_BE
from UserAPP import TypeSol_BE
from UserAPP import TypeSpecl_BE
from UserAPP import Autocompletecombox
from AdminAPP import XmlFile

class ExportXml(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Exporter XML")
        self.polyg = Parcelle_BE.Parcelle()
        self.cls = Cles.Cles()
        self.geometry("1040x580+160+50")
        self.resizable(0, 0)
        self.config(bg="#F7F9F9")
        self.polyg = Parcelle_BE.Parcelle()
        self.cls = Cles.Cles()

# FILTRER LES PARCELLES
        lf = LabelFrame(self, text="Filtrer les parcelles", width=348, height=502, font=("Helvetica", 12), bg="#F7F9F9")
        lf.place(x=4, y=4)

        super_id = Label(lf, text="Id supérieur ou égal à ", bg="#F7F9F9", font=("Helvetica", 11))
        super_id.place(x=10, y=15)
        polyg = Parcelle_BE.Parcelle()
        idPolyg = polyg.combboxID()
        self.super_id_box = ttk.Combobox(lf, values=idPolyg, width=25)
        self.super_id_box.place(x=160, y=15)

        infr_id = Label(lf, text="Id inférieur ou égal à ", bg="#F7F9F9", font=("Helvetica", 11))
        infr_id.place(x=10, y=55)
        self.infrId_box = ttk.Combobox(lf, values=idPolyg, width=25)
        self.infrId_box.place(x=160, y=55)

        date_inferieur = Label(lf, text="Date _De", bg="#F7F9F9", font=("Helvetica", 11))
        date_inferieur.place(x=47, y=95)
        self.infrDt = DateEntry(lf, date_pattern='dd-mm-yyyy', width=25)
        self.infrDt.place(x=160, y=95)

        self.infrDt.config(selectbackground='gray80',
                           selectforeground='black',
                           normalbackground='white',
                           normalforeground='black',
                           background='gray90',
                           foreground='black',
                           bordercolor='gray90',
                           othermonthforeground='gray50',
                           othermonthbackground='white',
                           othermonthweforeground='gray50',
                           othermonthwebackground='white',
                           weekendbackground='white',
                           weekendforeground='black',
                           headersbackground='white',
                           headersforeground='gray70')
        self.infrDt.delete(0, 'end')

        date_superieur = Label(lf, text="Date _A:", bg="#F7F9F9", font=("Helvetica", 11))
        date_superieur.place(x=47, y=135)
        self.superDt = DateEntry(lf, date_pattern='dd-mm-yyyy', width=25)
        self.superDt.place(x=160, y=135)
        self.superDt.config(selectbackground='gray80',
                            selectforeground='black',
                            normalbackground='white',
                            normalforeground='black',
                            background='gray90',
                            foreground='black',
                            bordercolor='gray90',
                            othermonthforeground='gray50',
                            othermonthbackground='white',
                            othermonthweforeground='gray50',
                            othermonthwebackground='white',
                            weekendbackground='white',
                            weekendforeground='black',
                            headersbackground='white',
                            headersforeground='gray70')
        self.superDt.delete(0, 'end')

        ss_zone = Label(lf, text="Sous-zone ", bg="#F7F9F9", font=("Helvetica", 11))
        ss_zone.place(x=46, y=175)
        sz = SousZone_BE.SousZ()
        szval = sz.combboxSZ()
        self.sZn_box = Autocompletecombox.Autocompletecombox(lf, values=szval, width=25)
        self.sZn_box.set_completion_list(szval)
        self.sZn_box.place(x=160, y=175)

        idDouar = Label(lf, text="Douar ", bg="#F7F9F9", font=("Helvetica", 11))
        idDouar.place(x=49, y=215)
        dr = Douar_BE.Douar()
        drVal = dr.combboxcDr()
        self.dr_box = Autocompletecombox.Autocompletecombox(lf, values=drVal, width=25)
        self.dr_box.set_completion_list(drVal)
        self.dr_box.place(x=160, y=215)

        cin = Label(lf, text="CIN ", bg="#F7F9F9", font=("Helvetica", 11))
        cin.place(x=58, y=255)
        self.prs = Personnes_BE.Personnes()
        cinVal = self.prs.combboxcCIN()
        self.cin_box = Autocompletecombox.Autocompletecombox(lf, values=cinVal, width=25)
        self.cin_box.set_completion_list(cinVal)
        self.cin_box.place(x=160, y=255)

        nmUsr = Label(lf, text="Utilisateur ", bg="#F7F9F9", font=("Helvetica", 11))
        nmUsr.place(x=45, y=295)
        usr = User_BE.User()
        usrVal = usr.usersList()
        self.nmUsr_box = Autocompletecombox.Autocompletecombox(lf, values=usrVal, width=25)
        self.nmUsr_box.set_completion_list(usrVal)
        self.nmUsr_box.place(x=160, y=295)

        listP = Label(lf, text="Parcelles Nº ", bg="#F7F9F9", font=("Helvetica", 11))
        listP.place(x=32, y=335)
        self.lst = Text(lf, relief=FLAT)
        self.lst.place(x=160, y=335, width=170, height=80)

        filterButton = Button(lf, text="Filtrer", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT,
                              activebackground="#9FE5D7", activeforeground="#E8B24D", command=self.filter)
        filterButton.place(x=150, y=440)

# LA LISTE A EXPORTER
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview", background="#FFFFFF", foreground="#14566D")
        style.configure("Treeview.Heading", background="#B0D9E8", foreground="#14566D")

        lf = LabelFrame(self, text="La liste a exporter", font=("Helvetica", 12), bg="#F7F9F9", width=682, height=502)
        lf.place(x=355, y=4)

        self.tree = ttk.Treeview(lf)
        self.tree.place(x=3, y=6, width=657, height=468)

        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        ysb.place(x=1017, y=32, height=468)

        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        xsb.place(x=360, y=486, width=657)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        self.parcelle = Parcelle_BE.Parcelle()
        self.col_name = self.parcelle.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=100)
            self.tree.heading(c, text=self.col_name[c])

# EXPORTER
        lfBtn = LabelFrame(self, text="Exporter", font=("Helvetica", 12), bg="#F7F9F9", width=1031, height=70)
        lfBtn.place(x=5, y=505)
        frm2 = Frame(lfBtn, bg="#379BF3", width=153, height=26)
        frm2.place(x=420, y=8)
        self.btn1 = tk.Button(frm2, text="Exporter Vers XML", bg="#CEE6F3", font=("Times New Roman", 13), fg="#379BF3",
                              relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3",
                              command=self.export)
        self.btn1.place(x=1, y=1, height=24)

    def filter(self):

        filtr = Exportation_BE.Filtrage()
        self.list = filtr.filtrage(self.super_id_box.get(), self.infrId_box.get(), self.infrDt.get(), self.superDt.get(), self.sZn_box.get(), self.dr_box.get(), self.cin_box.get(), self.nmUsr_box.get(), self.lst.get('1.0', 'end-1c'))
# vider les champs
        self.super_id_box.delete(0, 'end')
        self.infrId_box.delete(0, 'end')
        self.infrDt.delete(0, 'end')
        self.superDt.delete(0, 'end')
        self.sZn_box.delete(0, 'end')
        self.dr_box.delete(0, 'end')
        self.cin_box.delete(0, 'end')
        self.nmUsr_box.delete(0, 'end')
        self.lst.delete(1.0, 'end')

# insert values
        self.tree.delete(*self.tree.get_children())
        index = iid = 0
        for item in self.list:
            self.tree.insert("", index, iid, values=item)
            index = iid = index + 1

        self.tree.bind("<Double-1>", self.OnDoubleClick)

    def OnDoubleClick(self, event):
        self.root = Toplevel()
        self.root.geometry("240x140+600+260")
        self.root.resizable(0, 0)
        self.root.config(bg="#F7F9F9")
        self.root.title("XML")
        lbl = Label(self.root, text="Voulez-Vous retirer cette ligne \n de la liste?", font="Helvetica", bg="#F7F9F9")
        lbl.place(x=11, y=18)
        btn = Button(self.root, text="Retirer", command=self.retirer, bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000")
        btn.place(x=70, y=80)
        btn2 = Button(self.root, text="Annuler", command=self.annuler, fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
        btn2.place(x=135, y=80)

    def Retirer(self):
        x = self.tree.selection()[0]
        self.tree.delete(x)
        self.root.destroy()

    def annuler(self):
        self.root.destroy()

    def export(self):
        top_xml = Element('parcelles')
        tab = ['numParcelle', 'nomParcelleAR', 'nomParcelleFR', 'nombreBorne', 'surfCalculer', 'surfAdopter','surfaceHA', 'surfaceA', 'surfaceCA', 'adresseFR', 'adresseAR',
               'idSynchronisation', 'idDouar', 'fournisseurDonnee', 'idEnqueteurP', 'idEnqueteurJ', 'idValidateur','numeroOrdre', 'numero', 'Bornes', 'OppositionOpposants']
        polygn = self.polyg.listsParcelle()
        for i in range(len(self.list)):
            dr = Douar_BE.Douar.xmlDr(self, str(polygn[i][0]))
            riv = Rivrain_BE.Rivrains.rivXml(self,str(polygn[i][0]))
            prsm = self.prs.prsm_xml(str(polygn[i][0]))
            pnt = Point_BE.Point_BE.numPt(self,str(polygn[i][0]))
            cnst = Consistance_BE.Consistance.Const_xml(self,str(polygn[i][0]))
            sol = TypeSol_BE.TypeSol.sol_xml(self,str(polygn[i][0]))
            specl = TypeSpecl_BE.TypeSpecul.spec_xml(self,str(polygn[i][0]))

# -- Parcelle --
            middle_xml = SubElement(top_xml, 'parcelle')
            for j in range(len(tab)):
                sub = SubElement(middle_xml, tab[j])
                if tab[j] == 'numParcelle':
                    sub.text = str(polygn[i][0])
                if tab[j] == 'nomParcelleAR':
                    sub.text = str(polygn[i][2])
                if tab[j] == 'nomParcelleFR':
                    sub.text = str(polygn[i][1])
                if tab[j] == 'nombreBorne':
                    sub.text = str(polygn[i][16])
                if tab[j] == 'surfCalculer':
                    sub.text = '0'
                if tab[j] == 'surfAdopter':
                    sub.text = '0'
                if tab[j] == 'surfaceHA':
                    if polygn[i][12] == None:
                        sub.text = '0'
                    else:
                        sub.text = str(polygn[i][12])
                if tab[j] == 'surfaceA':
                    if polygn[i][13] == None:
                        sub.text = '0'
                    else:
                        sub.text = str(polygn[i][13])
                if tab[j] == 'surfaceCA':
                    if polygn[i][14] == None:
                        sub.text = '0'
                    else:
                        sub.text = str(polygn[i][14])
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
                    if polygn[i][6] == None:
                        sub.text = '0'
                    else:
                        sub.text = str(polygn[i][6])
                if tab[j] == 'numero':
                    sub.text = '0'
                if tab[j] == 'Bornes':
                    sub.text = ''
                if tab[j] == 'OppositionOpposants':
                    sub.text = ''

# -- Rivrain --
            rivrn = ['description', 'Direction', 'Id_douar', 'Id_Riverain', 'pointDebutName', 'pointFinName','Type_Riverain', 'Adresse', 'CIN', 'Nom', 'Prenom', 'GSM ']
            pntDF = ['id_douar', 'name', 'num_parcelle', 'type']
            if polygn != '':
                sub = SubElement(middle_xml, 'Rivrains')
                subelmt = SubElement(sub, 'RiverainPersonnePhysiques')
                for r in range(len(riv)):
                    presm = self.prs.prsm_xml(str(riv[r][1]))


                    drRiv = Douar_BE.Douar.drRivPolyg(self, str(riv[r][1]))
                    numPointD = Point_BE.Point_BE.numPoint(self, str(riv[r][3]))
                    numPointF = Point_BE.Point_BE.numPoint(self, str(riv[r][4]))
                    drPointD = Douar_BE.Douar.drRiv(self, str(riv[r][3]))
                    drPointF = Douar_BE.Douar.drRiv(self, str(riv[r][4]))
                    #print(presm[r][2])
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
                        if rivrn[rv] == 'pointDebutName':
                            subelmt3.text = numPointD[0]
                        if rivrn[rv] == 'pointFinName':
                            subelmt3.text = numPointF[0]
                        if rivrn[rv] == 'Type_Riverain':
                            subelmt3.text = 'Personne Physique'
                        if rivrn[rv] == 'Adresse':
                            subelmt3.text = str(presm[0][5])
                        if rivrn[rv] == 'CIN':
                            subelmt3.text = str(presm[0][7])
                        if rivrn[rv] == 'Nom':
                            subelmt3.text = str(presm[0][1])
                        if rivrn[rv] == 'Prenom':
                            subelmt3.text =str(presm[0][3])
                        if rivrn[rv] == 'GSM':
                            subelmt3.text = str(presm[0][8])
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
                    prcelSub.text = str(polygn[i][16])
                if prcTab[pc] == 'numParcelle':
                    prcelSub.text = str(polygn[i][0])
                if prcTab[pc] == 'surfAdopter':
                    prcelSub.text = '0'
                if prcTab[pc] == 'surfCalculer':
                    prcelSub.text = '0'
                if prcTab[pc] == 'surfaceA':
                    if polygn[i][13] == None:
                        prcelSub.text = '0'
                    else:
                        prcelSub.text = str(polygn[i][13])
                if prcTab[pc] == 'surfaceCA':
                    if polygn[i][14] == None:
                        prcelSub.text = '0'
                    else:
                        prcelSub.text = str(polygn[i][14])
                if prcTab[pc] == 'surfaceHA':
                    if polygn[i][12] == None:
                        prcelSub.text = '0'
                    else:
                        prcelSub.text = str(polygn[i][12])
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
                        pntPrcElmnt.text = 'num_point'
                    if pnts[pn] == 'num_parcelle':
                        pntPrcElmnt.text = str(polygn[i][0])
                    if pnts[pn] == 'partie':
                        pntPrcElmnt.text = 'P1'
                    if pnts[pn] == 'type':
                        pntPrcElmnt.text = parceValues[1]
                crdt = SubElement(pntPrc, 'coordinate')
                for crd in range(len(coord)):
                    crdtElmnt = SubElement(crdt, coord[crd])
                    if coord[crd] == 'x':
                        if parceValues[2] == None:
                            crdtElmnt.text = ''
                        else :
                            crdtElmnt.text = str(float(parceValues[2]))
                    if coord[crd] == 'y':
                        if parceValues[3] == None:
                            crdtElmnt.text = ''
                        else :
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
                    constSubElmnt.text = str(cnst[0][1])
                if consTab[cst] == 'libelleSol':
                    constSubElmnt.text = str(sol[0][1])
                if consTab[cst] == 'libelleSpeculation':
                    constSubElmnt.text = str(specl[0][1])

        xml_write = minidom.parseString(ElementTree.tostring(top_xml, 'utf-8')).toprettyxml(indent="  ")
        try:
            x = len(self.list)
            id1 = str(self.list[0][0])
            id2 = str(self.list[x - 1][0])
            if x == 1:
                filename = 'P' + id1 +'.xml'
                filepath = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML', filename)
                if not os.path.exists(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML')):
                    os.makedirs(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML'))
                fichier = open(filepath, 'w', encoding="utf-8")
                fichier.write(xml_write)
                fichier.close()
                self.tree.delete(*self.tree.get_children())
                XmlFile.XmlFile()

            elif x > 1:
                filename = 'P'+id1+'...P'+id2+'.xml'
                filepath = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML', filename)
                if not os.path.exists(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML')):
                    os.makedirs(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML'))
                fichier = open(filepath, 'w', encoding="utf-8")
                fichier.write(xml_write)
                fichier.close()
                self.tree.delete(*self.tree.get_children())
                XmlFile.XmlFile()
        except:
            msg = messagebox.showerror("XML", "Veuillez fermer le fichier")


'''if __name__ == "__main__":
    app = ExportXml()
    app.mainloop()'''