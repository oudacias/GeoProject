import time
from tkinter import *
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter import ttk

from tkcalendar import DateEntry

from AdminAPP import User_BE
from Exceptions import LastPolygError
from UserAPP import Autocompletecombox
from UserAPP import Cles
from UserAPP import Consistance_BE, Interval
from UserAPP import DetailMap
from UserAPP import Douar_BE
from UserAPP import Interval_BE
from UserAPP import Marche_BE
from UserAPP import Oppostition_BE
from UserAPP import Parcelle_BE
from UserAPP import Personnes_BE
from UserAPP import SousZone_BE
from UserAPP import TypeSol_BE
from UserAPP import TypeSpecl_BE
from UserAPP import Zone_BE


class Lastpolygon(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        try:
            self.polyg = Parcelle_BE.Parcelle()
            self.const = Consistance_BE.Consistance()
            self.tpSol = TypeSol_BE.TypeSol()
            self.TpSpecl = TypeSpecl_BE.TypeSpecul()
            self.dr = Douar_BE.Douar()
            self.sz = SousZone_BE.SousZ()
            self.zn = Zone_BE.Zone()
            self.mr = Marche_BE.Marche()
            self.prs = Personnes_BE.Personnes()
            self.cle = Cles.Cles()
            self.oppTp = Oppostition_BE.TypeOppos()
            self.usr = User_BE.User()
            self.verify = self.polyg.verify_lastPoly()
            if self.verify[0] == 1:
                #self.changeInterv()
                self.lastPolyg()
            elif self.verify[0] == 0:
                raise LastPolygError.LastPolygError
        except LastPolygError.LastPolygError:
            msg = messagebox.showerror("Dernière Parcelle", "Aucune parcelle trouvée")

    def lastPolyg(self):
        self.title("Dérniere Parcelle")
        self.geometry("1100x535+150+70")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.canv = Canvas(self, bg="white", width=337, height=526)
        self.canv.place(x=757, y=3)
        lastP = self.polyg.lastPolyInfo()
        start = DetailMap.DetailMap(self.canv, lastP[0][0])


        style = ttk.Style(self)
        style.theme_create("style", parent="clam", settings={
            "TFrame": {"configure": {"background": "#E3F3F3"}},
            "TNotebook": {
                "configure": {"background": "#E3F3F3", "tabmargins": [1, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"background": "#D2D5D5", "padding": [5, 2]},
                "map": {"background": [("selected", "#E3F3F3")],
                        "expand": [("selected", [2, 4, 1, 0])]
                        }}})
        style.theme_use("style")

        self.tabControl = ttk.Notebook(self, height=495, width=749)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="Parcelle")

        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="Présumé")

        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text="Opposant")
        self.tabControl.place(x=4, y=5)
        self.notTab1()
        self.notTab2()
        self.notTab3()

                                    # ----------------------------------TAB1 ------------------------------------ #
    def notTab1(self):

        polygVal = self.polyg.lastPolyInfo()
        idPrcel = Label(self.tab1, text="Parcelle Nº: ", font=("Helvetica", 14), bg="#E3F3F3")
        idPrcel.place(x=20, y=20)
        self.idPrcel_Val = Label(self.tab1, text="" + str(polygVal[0][0]) + "", font=("Helvetica", 14), bg="#E3F3F3")
        self.idPrcel_Val.place(x=124, y=20)

        znVal = self.zn.lastPolyZn()
        secteur = Label(self.tab1, text="Zone:", font=("Helvetica", 12), bg="#E3F3F3")
        secteur.place(x=18, y=60)
        self.zone = Label(self.tab1, text="" + str(znVal[0]) + "", font=("Helvetica", 12), bg="#E3F3F3")
        self.zone.place(x=59, y=60)

        szVal = self.sz.lastPolySZ()
        sous_sec = Label(self.tab1, text="Sous Zone:", font=("Helvetica", 12), bg="#E3F3F3")
        sous_sec.place(x=254, y=60)
        self.ssZone = Label(self.tab1, text="" + str(szVal[0][0]) + "", font=("Helvetica", 12), bg="#E3F3F3")
        self.ssZone.place(x=341, y=60)

        drVal = self.dr.lastPolyDr()
        douar = Label(self.tab1, text="Douar:", font=("Helvetica", 12), bg="#E3F3F3")
        douar.place(x=485, y=60)
        self.idPrcel_Val = Label(self.tab1, text="" + str(drVal[0][0]) + "", font=("Helvetica", 12), bg="#E3F3F3")
        self.idPrcel_Val.place(x=538, y=60)


    #LABEL FRAME
        labelFrame = LabelFrame(self.tab1, text = "Autres Informations à Ajouter", font=("Helvetica", 13), bg="#E3F3F3")
        labelFrame.place(x=15, y=100, width=719, height=380)

        nomFr = Label(labelFrame, text="Propriete dite", font=("Helvetica", 12), bg="#E3F3F3")
        nomFr.place(x=23, y=9)
        nomFr_Var = StringVar()
        nomFr_Var.set(str(polygVal[0][1]))
        self.nomFr_ent = Entry(labelFrame, textvariable=nomFr_Var, font=("Helvetica", 12), bg="#F7F9F9", relief=FLAT, width=24)
        self.nomFr_ent.place(x=157, y=10)

        nomAr = Label(labelFrame, text="الملك المسمى", font=("Helvetica", 12), bg="#E3F3F3")
        nomAr.place(x=625, y=9)
        nomAr_Var = StringVar()
        nomAr_Var.set(str(polygVal[0][2]))
        self.nomAr_ent = Entry(labelFrame, textvariable=nomAr_Var, font=("Helvetica", 12), justify='right', bg="#F7F9F9", relief=FLAT, width=24)
        self.nomAr_ent.place(x=380, y=10)

    #CONSISTANCE
        consistance = Label(labelFrame, text="Consistance", font=("Helvetica", 12), bg="#E3F3F3")
        consistance.place(x=30, y=50)
        constVal = self.const.combxConst()
        consistance_var = StringVar()
        self.consComb = Autocompletecombox.Autocompletecombox(labelFrame, textvariable=consistance_var, width=22,font=("Helvetica", 12))
        self.consComb.set_completion_list(constVal)
        self.consComb.place(x=155, y=50)

    # TYPE SOL
        sol = Label(labelFrame, text="Type de sol ", font=("Helvetica", 12), bg="#E3F3F3")
        sol.place(x=30, y=90)
        value = self.tpSol.combxTpsol()
        typesol_var = StringVar()
        self.sol_box = Autocompletecombox.Autocompletecombox(labelFrame, textvariable=typesol_var, width=22,font=("Helvetica", 12))
        self.sol_box.set_completion_list(value)
        self.sol_box.place(x=155, y=90)

    #TYPE SPÉCULATION
        spec = Label(labelFrame, text="Type de spéculation", font=("Helvetica", 11), bg="#E3F3F3")
        spec.place(x=10, y=130)
        valspec = self.TpSpecl.combxTpSpecl()
        spec_var = StringVar()
        self.spec_box = Autocompletecombox.Autocompletecombox(labelFrame, textvariable=spec_var, width=22,font=("Helvetica", 12))
        self.spec_box.set_completion_list(valspec)
        self.spec_box.place(x=155, y=130)

    #FAIR VALOIR
        fv = Label(labelFrame, text="Mode faire valoir", font=("Helvetica", 12), bg="#E3F3F3")
        fv.place(x=17, y=170)
        vfVal = ['D', 'IND']
        fv_var = StringVar()
        self.fv_box = Autocompletecombox.Autocompletecombox(labelFrame, textvariable=fv_var, width=22, font=("Helvetica", 12))
        self.fv_box.set_completion_list(vfVal)
        self.fv_box.place(x=155, y=170)

    #LIVRET
        livret = Label(labelFrame, text="Livret remis à", font=("Helvetica", 12), bg="#E3F3F3")
        livret.place(x=26, y=210)
        lvrt = ['Propriétaire', 'Présumé']
        livret_var = StringVar()
        self.lv_box = Autocompletecombox.Autocompletecombox(labelFrame, textvariable=livret_var, width=22, font=("Helvetica", 12))
        self.lv_box.set_completion_list(lvrt)
        self.lv_box.place(x=155, y=210)

    #PERSONNEL
        livret = Label(labelFrame, text="Personnel", font=("Helvetica", 12), bg="#E3F3F3")
        livret.place(x=40, y=250)
        prsn = self.usr.usersList()
        prsn_var = StringVar()
        self.usr_box = Autocompletecombox.Autocompletecombox(labelFrame, textvariable=prsn_var, width=22, font=("Helvetica", 12))
        self.usr_box.set_completion_list(prsn)
        self.usr_box.place(x=155, y=250)

        modifier = Button(labelFrame, text="Modifier", font=("Helvetica", 13), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, command=self.update)
        modifier.place(x=315, y=300)

    def update(self):
        updt = self.polyg.updateLastPoly2(self.nomFr_ent.get(), self.nomAr_ent.get(), self.consComb.get(), self.sol_box.get(), self.spec_box.get(), self.fv_box.get(), self.lv_box.get(), self.usr_box.get())
        msgbox = messagebox.showinfo("Parcelle", "Modification effectuée avec succès")

                              # ----------------------------------TAB2 // PRÉSUMÉ ------------------------------------ #
    def notTab2(self):

# FRAME1
        lf = LabelFrame(self.tab2, text="Séléctionner Un Présumé Existant", font=("Helvetica", 13), bg="#E3F3F3")
        lf.place(x=20, y=15, width=708, height=90)

        prs = Label(lf, text="Nom et Prénom", font=("Helvetica", 12), bg="#E3F3F3")
        prs.place(x=8, y=18)
        prs_varb = StringVar()
        nmPrenm = self.prs.personList()
        self.prs_box = Autocompletecombox.Autocompletecombox(lf, textvariable=prs_varb, font=("Times New Roman", 12))
        self.prs_box.set_completion_list(nmPrenm)
        self.prs_box.place(x=130, y=18)

        cin = Label(lf, text="CIN", font=("Helvetica", 12), bg="#E3F3F3")
        cin.place(x=340, y=18)
        cinVar = StringVar()
        cinPres = self.prs.combboxcCIN()
        self.cinBox = Autocompletecombox.Autocompletecombox(lf, textvariable=cinVar, font=("Times New Roman", 12))
        self.cinBox.set_completion_list(cinPres)
        self.cinBox.place(x=380, y=18)

        prs_btn = Button(lf, text="Sélectionner", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, command=self.updtPres)
        prs_btn.place(x=608, y=16)


# FRAME2
        lf = LabelFrame(self.tab2, text="Ajouter un Nouveau Présumé", font=("Helvetica", 13), bg="#E3F3F3")
        lf.place(x=20, y=115, width=708, height=360)

        Prenom = Label(lf, text="Prénom ", font=("Helvetica", 12), bg="#E3F3F3")
        Prenom.place(x=46, y=20)
        self.prenP = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.prenP.place(x=158, y=20)
        PrenomAr = Label(lf, text="الاسم الشخصي", font=("Helvetica", 12), bg="#E3F3F3")
        PrenomAr.place(x=585, y=20)
        self.prenPA = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, justify='right', bg="#F7F9F9")
        self.prenPA.place(x=354, y=20)

        nom = Label(lf, text="Nom", font=("Helvetica", 12), bg="#E3F3F3")
        nom.place(x=56, y=60)
        self.nmP = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.nmP.place(x=158, y=60)
        nomAr = Label(lf, text="الاسم العائلي", font=("Helvetica", 12), bg="#E3F3F3")
        nomAr.place(x=600, y=60)
        self.nmPA = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, justify='right', bg="#F7F9F9")
        self.nmPA.place(x=354, y=60)

        adress = Label(lf, text="L'adresse", font=("Helvetica", 12), bg="#E3F3F3")
        adress.place(x=55, y=100)
        self.addP = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.addP.place(x=158, y=100)
        adressAr = Label(lf, text="العنوان", font=("Helvetica", 12), bg="#E3F3F3")
        adressAr.place(x=605, y=100)
        self.addAP = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, justify='right', bg="#F7F9F9")
        self.addAP.place(x=354, y=100)

        cin = Label(lf, text="CIN", font=("Helvetica", 12), bg="#E3F3F3")
        cin.place(x=60, y=140)
        self.cinP = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.cinP.place(x=158, y=140)

        tel = Label(lf, text="Tel 1", font=("Helvetica", 12), bg="#E3F3F3")
        tel.place(x=58, y=180)
        self.telP = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.telP.place(x=158, y=180)

        tel2 = Label(lf, text="Tel 2", font=("Helvetica", 12), bg="#E3F3F3")
        tel2.place(x=60, y=220)
        self.telP2 = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.telP2.place(x=158, y=220)

        dateNss = Label(lf, text="Date de naissance", font=("Helvetica", 12), bg="#E3F3F3")
        dateNss.place(x=10, y=260)
        dateNss_var = StringVar()
        self.dtP = DateEntry(lf, textvariable=dateNss_var, date_pattern='dd-mm-yyyy', width=19, font=("Helvetica", 12))
        self.dtP.place(x=158, y=260)
        self.dtP.config(selectbackground='gray80',
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

        prsBtn = Button(lf, text="Ajouter", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#9FE5D7", activeforeground="#E8B24D", command=self.addPres)
        prsBtn.place(x=320, y=300)

    def updtPres(self):
        clsP = self.cle.addPersonCle(self.prs_box.get(), self.cinBox.get())
        msgbox = messagebox.showinfo("Présumé", "Un nouveau présumé a été bien ajouté")

    def addPres(self):
        insrt = self.prs.insertPerson(self.prenP.get(), self.prenPA.get(), self.nmP.get(), self.nmPA.get(),
                                      self.addP.get(), self.addAP.get(), self.cinP.get(),
                                      self.telP.get(), self.telP2.get(), self.dtP.get())
        addId = self.cle.insertPres()
        msgbox = messagebox.showinfo("Présumé", "Un nouveau présumé a été bien ajouté")

    # ----------------------------------TAB3 ------------------------------------ #
    def notTab3(self):

        btn = Button(self.tab3, text="Séléctionner Un Opposant Existant", bg="#E3F3F3", font=("Helvetica", 13), command=self.selectOpp, relief=FLAT)
        btn.place(x=20, y=18)

        btn = Button(self.tab3, text="Ajouter un Nouveau Opposant", bg="#E3F3F3", font=("Helvetica", 13), command=self.newOpp, relief=FLAT)
        btn.place(x=350, y=18)

# FRAME2
    def newOpp(self):
        lf = LabelFrame(self.tab3, text="Ajouter un Nouveau Opposant", font=("Helvetica", 13), bg="#E3F3F3")
        lf.place(x=20, y=65, width=708, height=420)

        Prenom = Label(lf, text="Prénom ", font=("Helvetica", 12), bg="#E3F3F3")
        Prenom.place(x=46, y=20)
        self.pren_Ent = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.pren_Ent.place(x=158, y=20)
        PrenomAr = Label(lf, text="الاسم الشخصي", font=("Helvetica", 12), bg="#E3F3F3")
        PrenomAr.place(x=585, y=20)
        self.prenAEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, justify='right', bg="#F7F9F9")
        self.prenAEnt.place(x=354, y=20)

        nom = Label(lf, text="Nom", font=("Helvetica", 12), bg="#E3F3F3")
        nom.place(x=56, y=60)
        self.nmEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.nmEnt.place(x=158, y=60)
        nomAr = Label(lf, text="الاسم العائلي", font=("Helvetica", 12), bg="#E3F3F3")
        nomAr.place(x=600, y=60)
        self.nmA_ent = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, justify='right', bg="#F7F9F9")
        self.nmA_ent.place(x=354, y=60)

        adress = Label(lf, text="L'adresse", font=("Helvetica", 12), bg="#E3F3F3")
        adress.place(x=55, y=100)
        self.adrEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.adrEnt.place(x=158, y=100)
        adressAr = Label(lf, text="العنوان", font=("Helvetica", 12), bg="#E3F3F3")
        adressAr.place(x=605, y=100)
        self.adA_ent = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, justify='right', bg="#F7F9F9")
        self.adA_ent.place(x=354, y=100)

        cin = Label(lf, text="CIN", font=("Helvetica", 12), bg="#E3F3F3")
        cin.place(x=60, y=140)
        self.cinEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.cinEnt.place(x=158, y=140)

        tel = Label(lf, text="Tel 1", font=("Helvetica", 12), bg="#E3F3F3")
        tel.place(x=60, y=180)
        self.telEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.telEnt.place(x=158, y=180)

        tel2 = Label(lf, text="Tel 2", font=("Helvetica", 12), bg="#E3F3F3")
        tel2.place(x=58, y=220)
        self.telEnt2 = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.telEnt2.place(x=158, y=220)

        dateNss = Label(lf, text="Date de naissance", font=("Helvetica", 12), bg="#E3F3F3")
        dateNss.place(x=10, y=260)
        dateNss_var = StringVar()
        self.dt_Ent = DateEntry(lf, date_pattern='dd-mm-yyyy', width=19, font=("Helvetica", 12))
        self.dt_Ent.place(x=158, y=260)
        self.dt_Ent.config(selectbackground='gray80',
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

        tpOpp = Label(lf, text="Type d'opposition", font=("Helvetica", 12), bg="#E3F3F3")
        tpOpp.place(x=12, y=300)
        tpOpp_varb = StringVar()
        oppVal = self.oppTp.combxTpOpp()
        self.tpOpp_box = Autocompletecombox.Autocompletecombox(lf, textvariable=tpOpp_varb, font=("Times New Roman", 12), width=21)
        self.tpOpp_box.set_completion_list(oppVal)
        self.tpOpp_box.place(x=160, y=300)

        oppBtn = Button(lf, text="Ajouter", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#9FE5D7", activeforeground="#E8B24D", command=self.addOpp)
        oppBtn.place(x=320, y=350)

    def addOpp(self):


        prsn = self.prs.insertPerson(self.pren_Ent.get(), self.prenAEnt.get(), self.nmEnt.get(), self.nmA_ent.get(),
                                     self.adrEnt.get(), self.adA_ent.get(), self.cinEnt.get(), self.telEnt.get(),
                                     self.telEnt2.get(), self.dt_Ent.get())
        cls = self.cle.insertOpp(self.tpOpp_box.get())
        msg = messagebox.showinfo("Opposant", "Un nouveau opposant a été bien ajouté")

                                        # --------------------- Vider les inputs ------------------------
        self.pren_Ent.delete(0, 'end')
        self.prenAEnt.delete(0, 'end')
        self.nmEnt.delete(0, 'end')
        self.nmA_ent.delete(0, 'end')
        self.adrEnt.delete(0, 'end')
        self.adA_ent.delete(0, 'end')
        self.cinEnt.delete(0, 'end')
        self.telEnt.delete(0, 'end')
        self.telEnt2.delete(0, 'end')
        self.dt_Ent.delete(0, 'end')
        self.usr_box.delete(0, 'end')

    def selectOpp(self):

        self.newroot = Toplevel()
        self.newroot.title('Opposant')
        self.newroot.geometry("370x230+450+200")
        self.newroot.config(bg="#F7F9F9")
        self.newroot.resizable(0, 0)

# SELECT OPPOSANT
        lFrm = LabelFrame(self.newroot, text="Séléctionner Un Opposant Existant", font=("Helvetica", 13), bg="#F7F9F9")
        lFrm.place(x=10, y=8, width=350, height=210)

        prs = Label(lFrm, text="Nom et Prénom", font=("Helvetica", 12), bg="#F7F9F9")
        prs.place(x=14, y=18)
        prs_var = StringVar()
        npOpp = self.prs.personList()
        self.opp_box = Autocompletecombox.Autocompletecombox(lFrm, textvariable=prs_var, font=("Times New Roman", 12))
        self.opp_box.set_completion_list(npOpp)
        self.opp_box.place(x=150, y=20)

        cin = Label(lFrm, text="CIN", font=("Helvetica", 12), bg="#F7F9F9")
        cin.place(x=55, y=60)
        cinVar = StringVar()
        cinPresm = self.prs.combboxcCIN()
        self.cinBoxOpp = Autocompletecombox.Autocompletecombox(lFrm, textvariable=cinVar, font=("Times New Roman", 12))
        self.cinBoxOpp.set_completion_list(cinPresm)
        self.cinBoxOpp.place(x=150, y=60)

# ADD TYPE OPPOSITION
        tpOpp = Label(lFrm, text="Type d'opposition", font=("Helvetica", 12), bg="#F7F9F9")
        tpOpp.place(x=8, y=100)
        tpOpp_varb = StringVar()
        oppVal = self.oppTp.combxTpOpp()
        self.tpOpp_box = Autocompletecombox.Autocompletecombox(lFrm, textvariable=tpOpp_varb, font=("Times New Roman", 12))
        self.tpOpp_box.set_completion_list(oppVal)
        self.tpOpp_box.place(x=150, y=100)

        opp_btn = Button(lFrm, text="Sélectionner", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, command=self.updtOpp)
        opp_btn.place(x=140, y=145)

    def updtOpp(self):
        # prsn = self.prs.addOpps(self.opp_box.get(), self.cinBoxOpp.get())
        cls = self.cle.addOpposCle(self.opp_box.get(), self.cinBoxOpp.get())
        p = self.cle.updatcles(self.tpOpp_box.get(), self.opp_box.get(), self.cinBoxOpp.get())
        msg = messagebox.showinfo("Opposant", "Un nouveau opposant a été bien ajouté")
        self.newroot.destroy()

#app = Lastpolygon()
#app.mainloop()