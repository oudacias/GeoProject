import matplotlib
matplotlib.use('TkAgg')
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from UserAPP import DetailMap
from UserAPP import Map_BE
from UserAPP import Consistance_BE
from UserAPP import TypeSol_BE
from UserAPP import TypeSpecl_BE
from UserAPP import Parcelle_BE
from UserAPP import Douar_BE
from UserAPP import Personnes_BE
from tkinter import ttk
from UserAPP import Rivrains_BE
from tkinter import messagebox

class Map(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        canv = Canvas(self, bg="#FFFFFF")
        canv.pack(side=TOP, fill="both", expand=True)
        canv.grid_rowconfigure(0, weight=1)
        canv.grid_columnconfigure(0, weight=1)

        fig = plt.figure(figsize=(11, 6))
        ax = fig.add_subplot(111)
        map = Map_BE.Map_BE.plotPolyg(self)
        ax = plt.gca()
        ax.set_facecolor('xkcd:cream')
        canvas = FigureCanvasTkAgg(fig, canv)
        toolbar = NavigationToolbar2Tk(canvas,  canv)
        toolbar.config(bg="#FFFFFF")
        toolbar.update()
        toolbar.pack(side=BOTTOM, fill=X)
        canvas.get_tk_widget().pack()
        canvas.draw()

        def onpick(event):
            if event.dblclick:
                try:
                    polyg = Map_BE.Map_BE.selectPolyg(event)
                    if (polyg != None):
                        window1 = Tk()
                        window1.geometry("1100x545+150+45")
                        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
                        window1.title("Parcelle")
                        window1.resizable(0, 0)

                        polygn = Parcelle_BE.Parcelle()
                        dr = Douar_BE.Douar()
                        cs = Consistance_BE.Consistance()
                        prs = Personnes_BE.Personnes()
                        tpSol = TypeSol_BE.TypeSol()
                        specl = TypeSpecl_BE.TypeSpecul()

    # Notebook
                        note = ttk.Notebook(window1, height=515, width=750)
                        note.place(x=3, y=2)

                        tab1 = ttk.Frame(note)
                        note.add(tab1, text='Parcelle')

                        values = polygn.researchPolyg(str(polyg[0]))
                        valDr = dr.select_colValue(str(polyg[0]))
                        valCons = cs.researPoly_Cons(str(polyg[0]))
                        valSol = tpSol.researPoly_Sol(str(polyg[0]))
                        valSpecl = specl.researPoly_Spec(str(polyg[0]))

                        idparcel = Label(tab1, text="Parcelle Nº:", font=("Helvetica", 14))
                        idparcel.place(x=10, y=20)
                        idparcel = Label(tab1, text="" + str(values[0]) + "", font=("Helvetica", 14))
                        idparcel.place(x=120, y=20)

                        label = Label(tab1, text="Propriete dite", font=("Helvetica", 12))
                        label.place(x=35, y=70)
                        self.parcel_Var = StringVar()
                        self.parcel = Entry(tab1, textvariable=self.parcel_Var, width=22, font=("Helvetica", 12),
                                            relief=FLAT, bg="#F7F9F9")
                        self.parcel.insert(1, values[1])
                        self.parcel.place(x=180, y=70)

                        nomAr = Label(tab1, text="الملك المسمى", font=("Helvetica", 12))
                        nomAr.place(x=630, y=70)
                        self.parcelAr_Var = StringVar()
                        self.parcelAr = Entry(tab1, textvariable=self.parcelAr_Var, width=22, font=("Helvetica", 12),
                                              relief=FLAT, bg="#F7F9F9", justify='right')
                        self.parcelAr.insert(1, values[2])
                        self.parcelAr.place(x=386, y=70)

                        douar = Label(tab1, text="Douar", font=("Helvetica", 12))
                        douar.place(x=62, y=110)
                        self.douar_Var = StringVar()
                        self.douarFR = Entry(tab1, textvariable=self.douar_Var, width=22, font=("Helvetica", 12),
                                             relief=FLAT, bg="#F7F9F9")
                        self.douarFR.insert(1, valDr[0][0])
                        self.douarFR.place(x=180, y=110)

                        douar = Label(tab1, text="الدوار", font=("Helvetica", 12))
                        douar.place(x=650, y=110)
                        self.douarAr_Var = StringVar()
                        self.douarAr = Entry(tab1, textvariable=self.douarAr_Var, width=22, font=("Helvetica", 12),
                                             relief=FLAT, bg="#F7F9F9", justify='right')
                        self.douarAr.insert(1, valDr[0][1])
                        self.douarAr.place(x=386, y=110)

                        srf = Label(tab1, text="Surface ", font=("Helvetica", 12))
                        srf.place(x=56, y=150)
                        self.area_Var = StringVar()
                        self.areaFr = Entry(tab1, textvariable=self.area_Var, width=22, font=("Helvetica", 12),
                                            relief=FLAT, bg="#F7F9F9")
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
                        self.areaFr.place(x=180, y=150)

                        label = Label(tab1, text="المساحة", font=("Helvetica", 12))
                        label.place(x=645, y=150)
                        self.areaAr_Var = StringVar()
                        self.areaAr = Entry(tab1, textvariable=self.areaAr_Var, width=22, font=("Helvetica", 12),
                                            relief=FLAT, bg="#F7F9F9", justify='right')
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

                        brn = Label(tab1, text="Nombre des bornes", font=("Helvetica", 11))
                        brn.place(x=40, y=190)
                        self.born_Var = StringVar()
                        self.born = Entry(tab1, textvariable=self.born_Var, width=22, font=("Helvetica", 12),
                                          relief=FLAT, bg="#F7F9F9")
                        self.born.insert(1, "" + str(values[4]) + "")
                        self.born.place(x=180, y=190)

                        label = Label(tab1, text="Consistance", font=("Helvetica", 11))
                        label.place(x=40, y=230)
                        self.consist_Var = StringVar()
                        self.consist = Entry(tab1, textvariable=self.consist_Var, width=22, font=("Helvetica", 12),
                                             relief=FLAT, bg="#F7F9F9")
                        self.consist.insert(1, valCons[0])
                        self.consist.place(x=180, y=230)

                        tpspec = Label(tab1, text="Type de spéculation", font=("Helvetica", 12))
                        tpspec.place(x=15, y=270)
                        self.specul_Var = StringVar()
                        self.specul = Entry(tab1, textvariable=self.specul_Var, width=22, font=("Helvetica", 12),
                                            relief=FLAT, bg="#F7F9F9")
                        self.specul.insert(1, valSpecl[0])
                        self.specul.place(x=180, y=270)

                        tpsol = Label(tab1, text="Type de sol", font=("Helvetica", 12))
                        tpsol.place(x=36, y=310)
                        self.sol_Var = StringVar()
                        self.sol = Entry(tab1, textvariable=self.sol_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                                         bg="#F7F9F9")
                        self.sol.insert(1, valSol[0])
                        self.sol.place(x=180, y=310)

                        label = Label(tab1, text="Date de l'enquête \n parcellaire", font=("Helvetica", 12))
                        label.place(x=25, y=350)
                        self.date_Var = StringVar()
                        self.date = Entry(tab1, textvariable=self.date_Var, width=22, font=("Helvetica", 12),
                                          relief=FLAT, bg="#F7F9F9")
                        self.date.insert(1, values[8])
                        self.date.place(x=180, y=350)

                        # --------------------- TAB2 --Présumé -------------------
                        tab2 = ttk.Frame(note)
                        note.add(tab2, text='Présumé')

                        verifyPres = prs.verifyPersonne(str(polyg[0]))
                        if verifyPres == True:
                            presVal = prs.researPres(str(polyg[0]))

                            idpresume = Label(tab2, text="Présumé Nº:", font=("Helvetica", 14))
                            idpresume.place(x=10, y=10)
                            self.idprsm = Label(tab2, text=str(presVal[0]), font=("Helvetica", 12))
                            self.idprsm.place(x=130, y=10)

                            Prenom = Label(tab2, text="Prénom", font=("Helvetica", 12))
                            Prenom.place(x=46, y=60)
                            self.prnmFr_Var = StringVar()
                            self.prnmFr = Entry(tab2, textvariable=self.prnmFr_Var, width=22, font=("Helvetica", 12),
                                                relief=FLAT, bg="#F7F9F9")
                            self.prnmFr.insert(1, presVal[1])
                            self.prnmFr.place(x=158, y=60)

                            PrenomAr = Label(tab2, text="الاسم الشخصي", font=("Helvetica", 12))
                            PrenomAr.place(x=610, y=60)
                            self.prnm_Var = StringVar()
                            self.prnmAr = Entry(tab2, textvariable=self.prnm_Var, width=22, font=("Helvetica", 12),
                                                relief=FLAT, bg="#F7F9F9", justify=RIGHT)
                            self.prnmAr.insert(1, presVal[2])
                            self.prnmAr.place(x=364, y=60)

                            nom = Label(tab2, text="Nom", font=("Helvetica", 12))
                            nom.place(x=56, y=100)
                            self.nom_Var = StringVar()
                            self.nomFr = Entry(tab2, textvariable=self.nom_Var, width=22, font=("Helvetica", 12),
                                               relief=FLAT, bg="#F7F9F9")
                            self.nomFr.insert(1, presVal[3])
                            self.nomFr.place(x=158, y=100)

                            nomAr = Label(tab2, text="الاسم العائلي", font=("Helvetica", 12))
                            nomAr.place(x=613, y=100)
                            self.nomAr_Var = StringVar()
                            self.nomAr = Entry(tab2, textvariable=self.nomAr_Var, width=22, font=("Helvetica", 12),
                                               relief=FLAT, bg="#F7F9F9", justify=RIGHT)
                            self.nomAr.insert(1, presVal[4])
                            self.nomAr.place(x=364, y=100)

                            adress = Label(tab2, text="L'adresse", font=("Helvetica", 12))
                            adress.place(x=40, y=140)
                            self.address_Var = StringVar()
                            self.address = Entry(tab2, textvariable=self.address_Var, width=22, font=("Helvetica", 12),
                                                 relief=FLAT, bg="#F7F9F9")
                            self.address.insert(1, presVal[5])
                            self.address.place(x=158, y=140)

                            adressAr = Label(tab2, text="العنوان", font=("Helvetica", 12))
                            adressAr.place(x=626, y=140)
                            self.addrAr_Var = StringVar()
                            self.addr_Ar = Entry(tab2, textvariable=self.addrAr_Var, width=22, font=("Helvetica", 12),
                                                 relief=FLAT, bg="#F7F9F9", justify=RIGHT)
                            self.addr_Ar.insert(1, presVal[6])
                            self.addr_Ar.place(x=364, y=140)

                            tel = Label(tab2, text="Tel", font=("Helvetica", 12))
                            tel.place(x=60, y=180)
                            self.tel1_Var = StringVar()
                            self.tel1 = Entry(tab2, textvariable=self.tel1_Var, width=22, font=("Helvetica", 12),
                                              relief=FLAT, bg="#F7F9F9")
                            if presVal[8] == None or presVal[8] == 'null':
                                self.tel1.insert(1, '')
                            else:
                                self.tel1.insert(1, presVal[8])
                            self.tel1.place(x=158, y=180)

                            tel2 = Label(tab2, text="Tel 2", font=("Helvetica", 12))
                            tel2.place(x=59, y=220)
                            self.tel2_Var = StringVar()
                            self.tel2 = Entry(tab2, textvariable=self.tel2_Var, width=22, font=("Helvetica", 12),
                                              relief=FLAT, bg="#F7F9F9")
                            if presVal[9] == None or presVal[9] == 'null':
                                self.tel2.insert(1, '')
                            else:
                                self.tel2.insert(1, presVal[9])
                            self.tel2.place(x=158, y=220)

                            cin = Label(tab2, text="CIN", font=("Helvetica", 12))
                            cin.place(x=60, y=260)
                            self.cin_Var = StringVar()
                            self.cin = Entry(tab2, textvariable=self.cin_Var, width=22, font=("Helvetica", 12),
                                             relief=FLAT, bg="#F7F9F9")
                            if presVal[7] == None or presVal[7] == 'null':
                                self.cin.insert(1, '')
                            else:
                                self.cin.insert(1, presVal[7])
                            self.cin.place(x=158, y=260)

                            dateNss = Label(tab2, text="Date de naissance", font=("Helvetica", 12))
                            dateNss.place(x=10, y=300)
                            self.datNaiss_Var = StringVar()
                            self.datNaiss = Entry(tab2, textvariable=self.datNaiss_Var, width=22,
                                                  font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
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

                        '''sty_tree = ttk.Style(self)
                        sty_tree.theme_use('clam')
                        sty_tree.configure("Treeview", background="#FFFFFF", foreground="#14566D")
                        sty_tree.configure("Treeview.Heading", background="#8CC7DC", foreground="#0D4EA2")'''

                        self.tree = ttk.Treeview(tab3)
                        self.tree.place(x=3, y=5, width=742, height=500)

                        xsb = ttk.Scrollbar(tab3, orient='horizontal', command=self.tree.xview)
                        xsb.place(x=3, y=500, width=742)
                        self.tree['xscroll'] = xsb.set
                        self.tree.configure(yscrollcommand=xsb.set)

                        self.col_name = prs.columnName()
                        self.tree["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
                        self.tree['show'] = 'headings'
                        for c in range(len(self.tree["columns"])):
                            self.tree.column(c, width=120)
                            self.tree.heading(c, text=self.col_name[c])

                        list = prs.researOppo(str(polyg[0]))
                        index = iid = 0
                        for item in list:
                            self.tree.insert("", index, iid, values=item)
                            index = iid = index + 1

    # ----------------------- TAB4 -- Rivrains --------------------
                        tab4 = ttk.Frame(note)
                        note.add(tab4, text='Rivrains')
                        rivr = Rivrains_BE.Rivrains()

                        '''sty_tree = ttk.Style(self)
                        sty_tree.theme_use('clam')
                        sty_tree.configure("Treeview", background="#FFFFFF", foreground="#14566D")
                        sty_tree.configure("Treeview.Heading", background="#8CC7DC", foreground="#0D4EA2")'''

                        self.tree = ttk.Treeview(tab4)
                        self.tree.place(x=3, y=5, width=742, height=500)

                        xsb = ttk.Scrollbar(tab4, orient='horizontal', command=self.tree.xview)
                        xsb.place(x=3, y=500, width=742)
                        self.tree['xscroll'] = xsb.set
                        self.tree.configure(yscrollcommand=xsb.set)

                        self.col_name = rivr.columnName()
                        self.tree["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
                        self.tree['show'] = 'headings'
                        for c in range(len(self.tree["columns"])):
                            self.tree.column(c, width=120)
                            self.tree.heading(c, text=self.col_name[c])

                        list = rivr.researRiv(str(polyg[0]))
                        index = iid = 0
                        for item in list:
                            self.tree.insert("", index, iid, values=item)
                            index = iid = index + 1

    # ----------------------------------------- Mappe
                        frm = Frame(window1, bg="#FFFFFF")
                        frm.place(x=755, y=2, width=340, height=665)
                        start = DetailMap.DetailMap(frm, polyg[0])
                        window1.mainloop()
                    else:
                        messagebox.showerror("Parcelles", "Veuillez sélectionner une parcelle")
                except:
                    messagebox.showerror("Parcelles", "Veuillez sélectionner une parcelle")

        fig.canvas.mpl_connect('button_press_event', onpick)
