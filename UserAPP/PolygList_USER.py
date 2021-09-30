from tkinter import *
from UserAPP import Consistance_BE
from UserAPP import TypeSol_BE
from UserAPP import TypeSpecl_BE
from UserAPP import Parcelle_BE
from UserAPP import Douar_BE
from UserAPP import Marche_BE
from UserAPP import Personnes_BE
from UserAPP import DetailMap
from  UserAPP import Map_Usr
from tkinter import ttk
from UserAPP import Rivrains_BE
from tkinter import messagebox

class PolygList(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #self.controller.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')

        self.parcelle = Parcelle_BE.Parcelle()
        self.mrch = Marche_BE.Marche()

    #ETAT DE BARRE
        etatBar = Frame(self, bg="#FFFFFF", height=22)
        etatBar.grid(row=2, column=0, sticky='nsew', columnspan=2)
        nbrlgn = self.parcelle.lignesNumb()
        mrche = self.mrch.mrchName()
        lgn = Label(etatBar, text="" + str(nbrlgn[0]) + " Lignes ", font=("Helvetica", 10), bg="#FFFFFF")
        lgn.place(x=10)
        mrch = Label(etatBar, text="Marché: " + str(mrche[0]) + "", font=("Helvetica", 10), bg="#FFFFFF")
        mrch.place(x=1200)

# -------------------------------------------------------------TREEVIEW ** La liste des Parcelles **-------------------------------------------------

        self.treeV = ttk.Treeview(self)
        self.treeV.grid(row=0, column=0, sticky='nsew')

        ysb = ttk.Scrollbar(self, orient='vertical', command=self.treeV.yview)
        ysb.grid(row=0, column=1, sticky='ns')
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.treeV.xview)
        xsb.grid(row=1, column=0, sticky='ew', columnspan=2)
        self.treeV['yscroll'] = ysb.set
        self.treeV['xscroll'] = xsb.set

        self.col_name = self.parcelle.columnName()
        self.treeV["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15")
        self.treeV['show'] = 'headings'
        for c in range(len(self.treeV["columns"])):
            self.treeV.column(c, width=100)
            self.treeV.heading(c, text=self.col_name[c])
        list = self.parcelle.listsParcelle()
        index = iid = 0
        self.treeV.tag_configure('RED_TAG', background="#FFFFFF", foreground="#14566D")
        for item in list:
            self.treeV.insert("", index, iid, values=item, tag='RED_TAG')
            index = iid = index + 1

        self.treeV.bind("<Double-1>", self.OnDoubleClick)

    def OnDoubleClick(self, event):
        try:
            self.row_selected = self.treeV.item(self.treeV.selection())
            self.value = self.row_selected['values'][0]
            self.polyg = Parcelle_BE.Parcelle()
            self.dr = Douar_BE.Douar()
            self.cs = Consistance_BE.Consistance()
            self.prs = Personnes_BE.Personnes()
            self.tpSol = TypeSol_BE.TypeSol()
            self.specl = TypeSpecl_BE.TypeSpecul()
            verify = self.polyg.verifyPolyg(str(self.value))
            if verify == True:
                self.root = Toplevel()
                self.root.geometry("1100x545+150+45")
                self.root.resizable(0, 0)
                self.root.title('Parcelle')
                self.canvasFrame()
                self.notebook()
            else:
                messagebox.showerror("Parcelles", "Veuillez sélectionner une parcelle")
        except:
            messagebox.showerror("Parcelles", "Veuillez sélectionner une parcelle")

                    # ----------------------------- CANVAS -------------------
    def canvasFrame(self):
        self.canv = Canvas(self.root, bg="#FFFFFF", width=340, height=546)
        self.canv.place(x=756, y=2)
        start = DetailMap.DetailMap(self.canv, self.value)
        #start = Map_BE.Map_BE.detailMap(self.canv, self.value)

                    # --------------------- NOTEBOOK ---------------------------
    def notebook(self):
        note = ttk.Notebook(self.root, height=515, width=750)
        note.place(x=3, y=2)

                                                            # --------------------- TAB1 -- PARCELLE -------------------
        self.tab1 = ttk.Frame(note)
        note.add(self.tab1, text='Parcelle')

        values = self.polyg.researchPolyg(str(self.value))
        valDr = self.dr.selectDr(str(self.value))
        valCons = self.cs.researPoly_Cons(str(self.value))
        valSol = self.tpSol.researPoly_Sol(str(self.value))
        valSpecl = self.specl.researPoly_Spec(str(self.value))

        idparcel = Label(self.tab1, text="Parcelle Nº:", font=("Helvetica", 14))
        idparcel.place(x=10, y=20)
        idparcel = Label(self.tab1, text="" + str(values[0]) + "", font=("Helvetica", 14))
        idparcel.place(x=120, y=20)

        label = Label(self.tab1, text="Propriete dite", font=("Helvetica", 12))
        label.place(x=35, y=70)
        self.parcel_Var = StringVar()
        self.parcel = Entry(self.tab1, textvariable=self.parcel_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                            bg="#F7F9F9")
        self.parcel.insert(1, values[1])
        self.parcel.place(x=180, y=70)

        nomAr = Label(self.tab1, text="الملك المسمى", font=("Helvetica", 12))
        nomAr.place(x=630, y=70)
        self.parcelAr_Var = StringVar()
        self.parcelAr = Entry(self.tab1, textvariable=self.parcelAr_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                              bg="#F7F9F9", justify='right')
        self.parcelAr.insert(1, values[2])
        self.parcelAr.place(x=386, y=70)

        douar = Label(self.tab1, text="Douar", font=("Helvetica", 12))
        douar.place(x=62, y=110)
        self.douar_Var = StringVar()
        self.douarFR = Entry(self.tab1, textvariable=self.douar_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                             bg="#F7F9F9")
        self.douarFR.insert(1, valDr[0][0])
        self.douarFR.place(x=180, y=110)

        douar = Label(self.tab1, text="الدوار", font=("Helvetica", 12))
        douar.place(x=650, y=110)
        self.douarAr_Var = StringVar()
        self.douarAr = Entry(self.tab1, textvariable=self.douarAr_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                             bg="#F7F9F9", justify='right')
        self.douarAr.insert(1, valDr[0][1])
        self.douarAr.place(x=386, y=110)

        srf = Label(self.tab1, text="Surface ", font=("Helvetica", 12))
        srf.place(x=56, y=150)
        self.area_Var = StringVar()
        self.areaFr = Entry(self.tab1, textvariable=self.area_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                            bg="#F7F9F9")
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
            self.areaFr.insert(1, str(values[5]) + 'Ha  ' + str(values[6]) + 'a  ' + str(values[7]) + 'ca')
        self.areaFr.place(x=180, y=150)

        label = Label(self.tab1, text="المساحة", font=("Helvetica", 12))
        label.place(x=645, y=150)
        self.areaAr_Var = StringVar()
        self.areaAr = Entry(self.tab1, textvariable=self.areaAr_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                            bg="#F7F9F9", justify='right')
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
        self.areaAr.place(x=386, y=150)

        brn = Label(self.tab1, text="Nombre des bornes", font=("Helvetica", 11))
        brn.place(x=40, y=190)
        self.born_Var = StringVar()
        self.born = Entry(self.tab1, textvariable=self.born_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                          bg="#F7F9F9")
        self.born.insert(1, "" + str(values[4]) + "")
        self.born.place(x=180, y=190)

        label = Label(self.tab1, text="Consistance", font=("Helvetica", 11))
        label.place(x=40, y=230)
        self.consist_Var = StringVar()
        self.consist = Entry(self.tab1, textvariable=self.consist_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                             bg="#F7F9F9")
        self.consist.insert(1, valCons[0])
        self.consist.place(x=180, y=230)

        tpspec = Label(self.tab1, text="Type de spéculation", font=("Helvetica", 12))
        tpspec.place(x=15, y=270)
        self.specul_Var = StringVar()
        self.specul = Entry(self.tab1, textvariable=self.specul_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                            bg="#F7F9F9")
        self.specul.insert(1, valSpecl[0])
        self.specul.place(x=180, y=270)

        tpsol = Label(self.tab1, text="Type de sol", font=("Helvetica", 12))
        tpsol.place(x=36, y=310)
        self.sol_Var = StringVar()
        self.sol = Entry(self.tab1, textvariable=self.sol_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                         bg="#F7F9F9")
        self.sol.insert(1, valSol[0])
        self.sol.place(x=180, y=310)

        label = Label(self.tab1, text="Date de l'enquête \n parcellaire", font=("Helvetica", 12))
        label.place(x=25, y=350)
        self.date_Var = StringVar()
        self.date = Entry(self.tab1, textvariable=self.date_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                          bg="#F7F9F9")
        self.date.insert(1, values[8])
        self.date.place(x=180, y=350)

                                                              # --------------------- TAB2 --Présumé -------------------
        self.tab2 = ttk.Frame(note)
        note.add(self.tab2, text='Présumé')
        verifyPres = self.prs.verifyPersonne(str(self.value))
        if verifyPres == True:
            presVal = self.prs.researPres(str(self.value))

            idpresume = Label(self.tab2, text="Présumé Nº:", font=("Helvetica", 14))
            idpresume.place(x=10, y=10)
            self.idprsm = Label(self.tab2, text=str(presVal[0]), font=("Helvetica", 12))
            self.idprsm.place(x=130, y=10)

            Prenom = Label(self.tab2, text="Prénom", font=("Helvetica", 12))
            Prenom.place(x=46, y=60)
            self.prnmFr_Var = StringVar()
            self.prnmFr = Entry(self.tab2, textvariable=self.prnmFr_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
            self.prnmFr.insert(1, presVal[1])
            self.prnmFr.place(x=158, y=60)

            PrenomAr = Label(self.tab2, text="الاسم الشخصي", font=("Helvetica", 12))
            PrenomAr.place(x=610, y=60)
            self.prnm_Var = StringVar()
            self.prnmAr = Entry(self.tab2, textvariable=self.prnm_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify=RIGHT)
            self.prnmAr.insert(1, presVal[2])
            self.prnmAr.place(x=364, y=60)

            nom = Label(self.tab2, text="Nom", font=("Helvetica", 12))
            nom.place(x=56, y=100)
            self.nom_Var = StringVar()
            self.nomFr = Entry(self.tab2, textvariable=self.nom_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
            self.nomFr.insert(1, presVal[3])
            self.nomFr.place(x=158, y=100)

            nomAr = Label(self.tab2, text="الاسم العائلي", font=("Helvetica", 12))
            nomAr.place(x=613, y=100)
            self.nomAr_Var = StringVar()
            self.nomAr = Entry(self.tab2, textvariable=self.nomAr_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify=RIGHT)
            self.nomAr.insert(1, presVal[4])
            self.nomAr.place(x=364, y=100)

            adress = Label(self.tab2, text="L'adresse", font=("Helvetica", 12))
            adress.place(x=40, y=140)
            self.address_Var = StringVar()
            self.address = Entry(self.tab2, textvariable=self.address_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
            self.address.insert(1, presVal[5])
            self.address.place(x=158, y=140)

            adressAr = Label(self.tab2, text="العنوان", font=("Helvetica", 12))
            adressAr.place(x=626, y=140)
            self.addrAr_Var = StringVar()
            self.addr_Ar = Entry(self.tab2, textvariable=self.addrAr_Var, width=22, font=("Helvetica", 12), relief=FLAT,  bg="#F7F9F9", justify=RIGHT)
            self.addr_Ar.insert(1, presVal[6])
            self.addr_Ar.place(x=364, y=140)

            tel = Label(self.tab2, text="Tel", font=("Helvetica", 12))
            tel.place(x=60, y=180)
            self.tel1_Var = StringVar()
            self.tel1 = Entry(self.tab2, textvariable=self.tel1_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
            if presVal[8] == None or presVal[8] == 'null':
                self.tel1.insert(1, '')
            else:
                self.tel1.insert(1, presVal[8])
            self.tel1.place(x=158, y=180)

            tel2 = Label(self.tab2, text="Tel 2", font=("Helvetica", 12))
            tel2.place(x=59, y=220)
            self.tel2_Var = StringVar()
            self.tel2 = Entry(self.tab2, textvariable=self.tel2_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
            if presVal[9] == None or presVal[9] == 'null':
                self.tel2.insert(1, '')
            else:
                self.tel2.insert(1, presVal[9])
            self.tel2.place(x=158, y=220)

            cin = Label(self.tab2, text="CIN", font=("Helvetica", 12))
            cin.place(x=60, y=260)
            self.cin_Var = StringVar()
            self.cin = Entry(self.tab2, textvariable=self.cin_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
            if presVal[7] == None or presVal[7] == 'null':
                self.cin.insert(1, '')
            else:
                self.cin.insert(1, presVal[7])
            self.cin.place(x=158, y=260)

            dateNss = Label(self.tab2, text="Date de naissance", font=("Helvetica", 12))
            dateNss.place(x=10, y=300)
            self.datNaiss_Var = StringVar()
            self.datNaiss = Entry(self.tab2, textvariable=self.datNaiss_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
            if presVal[10] == None or presVal[10] == 'null':
                self.datNaiss.insert(1, '')
            else:
                self.datNaiss.insert(1, presVal[10])
            self.datNaiss.place(x=158, y=300)
        else:
            msg = messagebox.showerror("Présumé", "Aucun présumé enregistré pour cette parcelle")
                                                        # ----------------------- TAB3 -- Opposants --------------------
        tab3 = ttk.Frame(note)
        note.add(tab3, text='Opposant')

        tree = ttk.Treeview(tab3)
        tree.place(x=3, y=5, width=742, height=500)

        xsb = ttk.Scrollbar(tab3, orient='horizontal', command=tree.xview)
        xsb.place(x=3, y=500, width=742)
        tree['xscroll'] = xsb.set
        tree.configure(yscrollcommand=xsb.set)

        self.col_name = self.prs.columnName()
        tree["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        tree['show'] = 'headings'
        for c in range(len(tree["columns"])):
            tree.column(c, width=120)
            tree.heading(c, text=self.col_name[c])

        list = self.prs.researOppo(str(self.value))
        index = iid = 0
        for item in list:
            tree.insert("", index, iid, values=item)
            index = iid = index + 1

                                                        # ----------------------- TAB4 -- Rivrains --------------------
        tab4 = ttk.Frame(note)
        note.add(tab4, text='Rivrains')
        rivr = Rivrains_BE.Rivrains()

        tree = ttk.Treeview(tab4)
        tree.place(x=3, y=5, width=742, height=500)

        xsb = ttk.Scrollbar(tab4, orient='horizontal', command=tree.xview)
        xsb.place(x=3, y=500, width=742)
        tree['xscroll'] = xsb.set
        tree.configure(yscrollcommand=xsb.set)

        self.col_name = rivr.columnName()
        tree["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8")
        tree['show'] = 'headings'
        for c in range(len(tree["columns"])):
            tree.column(c, width=120)
            tree.heading(c, text=self.col_name[c])

        list = rivr.researRiv(str(self.value))
        index = iid = 0
        for item in list:
            tree.insert("", index, iid, values=item)
            index = iid = index + 1

