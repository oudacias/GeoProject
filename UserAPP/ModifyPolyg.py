from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkcalendar import Calendar, DateEntry
from UserAPP import Consistance_BE
from UserAPP import TypeSol_BE
from UserAPP import TypeSpecl_BE
from UserAPP import Parcelle_BE
from UserAPP import Douar_BE
from UserAPP import SousZone_BE
from UserAPP import Marche_BE
from UserAPP import Personnes_BE
from UserAPP import Autocompletecombox
from UserAPP import Cles
from UserAPP import Oppostition_BE
from UserAPP import Zone_BE
from Exceptions import PolygError
from Exceptions import IdError
from tkinter import messagebox
from UserAPP import DetailMap



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

class ModifyPolyg(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Modifier Parcelle")
        self.geometry("1100x535+150+70")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.prs = Personnes_BE.Personnes()
        self.polg = Parcelle_BE.Parcelle()
        self.oppTp = Oppostition_BE.TypeOppos()
        self.consist = Consistance_BE.Consistance()
        self.specl = TypeSpecl_BE.TypeSpecul()
        self.sol = TypeSol_BE.TypeSol()
        self.cle = Cles.Cles()

        self.researchFrame()
        self.canvasFrame()
        self.notebook()

# -------------------------------------------------------------------------------------- Research Polyg -------------------------------------------------------------------
    def researchFrame(self):
        top_frame = Frame(self, bg="white")
        top_frame.pack(side=TOP, fill=X, pady=2)

        self.idparcelle = tk.Entry(top_frame, font=("Helvetica", 13), relief=FLAT, bg="#F7F9F9", width=40)
        self.idparcelle.pack(side=LEFT, padx=100, pady=2)
        add_placeholder_to(self.idparcelle, "Id parcelle")

        id_btn = Button(top_frame, text="Rechercher", bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, command=self.values)
        id_btn.pack(side=LEFT, padx=2, pady=2)


# -------------------------------------------------------------------------------------- Canvas Polyg -------------------------------------------------------------------
    def canvasFrame(self):
        self.canv = Canvas(self, bg="#FFFFFF", width=340, height=546)
        self.canv.place(x=755, y=36)
        #start = DetailMap.DetailMap(self.canvas, self.idparcelle.get())


# -------------------------------------------------------------------------------------- NoteBook Polyg -------------------------------------------------------------------
    def notebook(self):

        self.nBk = ttk.Notebook(self, height=470, width=743)
        self.nBk.place(x=4, y=35)

                                    # *************** -- TAB1 -- INFORMATIONS GÉNÉRALES ************
        self.tab1 = ttk.Frame(self.nBk)
        self.nBk.add(self.tab1, text="Parcelle")
        idPrcel = Label(self.tab1, text="Parcelle Nº: ", font=("Helvetica", 14))
        idPrcel.place(x=20, y=20)
        self.idP = Label(self.tab1, text="", font=("Helvetica", 14))
        self.idP.place(x=130, y=20)

        secteur = Label(self.tab1, text="Zone:", font=("Helvetica", 12))
        secteur.place(x=18, y=60)
        self.zn = Label(self.tab1, text="", font=("Helvetica", 12))
        self.zn.place(x=59, y=60)

        sous_sec = Label(self.tab1, text="Sous Zone:", font=("Helvetica", 12))
        sous_sec.place(x=254, y=60)
        self.sz = Label(self.tab1, text="", font=("Helvetica", 12))
        self.sz.place(x=341, y=60)

        douar = Label(self.tab1, text="Douar:", font=("Helvetica", 12))
        douar.place(x=485, y=60)
        self.drLabel = Label(self.tab1, text="", font=("Helvetica", 12))
        self.drLabel.place(x=538, y=60)

# LABEL FRAME
        self.lbf = LabelFrame(self.tab1, text="Informations à Modifier", font=("Helvetica", 13))
        self.lbf.place(x=10, y=110, width=719, height=170)

        nomFr = Label(self.lbf, text="Propriete dite", font=("Helvetica", 12))
        nomFr.place(x=23, y=20)
        self.nomFr_Var = StringVar()
        self.nomFr_ent = Entry(self.lbf, textvariable=self.nomFr_Var, font=("Helvetica", 12), bg="#F7F9F9", relief=FLAT,width=24)
        self.nomFr_ent.place(x=157, y=18)

        nomAr = Label(self.lbf, text="الملك المسمى", font=("Helvetica", 12))
        nomAr.place(x=625, y=20)
        self.nomAr_Var = StringVar()
        self.nomAr_ent = Entry(self.lbf, textvariable=self.nomAr_Var, font=("Helvetica", 12), bg="#F7F9F9", relief=FLAT,width=24, justify='right')
        self.nomAr_ent.place(x=380, y=18)


# CONSISTANCE
        '''consistance = Label(self.lbf, text="Consistance", font=("Helvetica", 12))
        consistance.place(x=30, y=50)
        const = Consistance_BE.Consistance()
        constVal = const.combxConst()
        consistance_var = StringVar()
        self.consComb = ttk.Combobox(self.lbf, values=constVal, textvariable=consistance_var, width=22, font=("Helvetica", 12))
        self.consComb.place(x=155, y=50)


# TYPE SOL
        sol = Label(self.lbf, text="Type de sol ", font=("Helvetica", 12))
        sol.place(x=30, y=90)
        tpsol = TypeSol_BE.TypeSol()
        value = tpsol.combxTpsol()
        typesol_var = StringVar()
        self.sol_box = ttk.Combobox(self.lbf, values=value, textvariable=typesol_var, width=22, font=("Helvetica", 12))
        self.sol_box.place(x=155, y=90)

# TYPE SPÉCULATION
        spec = Label(self.lbf, text="Type de spéculation", font=("Helvetica", 11))
        spec.place(x=10, y=130)
        self.Spec_var = StringVar()
        specl = TypeSpecl_BE.TypeSpecul()
        valSpec = specl.combxTpSpecl()
        self.specBox = ttk.Combobox(self.lbf, values=valSpec, textvariable=self.Spec_var, width=22, font=("Helvetica", 12))
        self.specBox.place(x=155, y=130)'''

# Button
        modifier = Button(self.lbf, text="Modifier", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#9FE5D7", activeforeground="#E8B24D", command=self.updtPolyg)
        modifier.place(x=315, y=80)

                                                 # *************** -- TAB2 -- Consistance  ************
        self.tab2 = ttk.Frame(self.nBk)
        self.nBk.add(self.tab2, text="Consistance")
        self.fr_const = LabelFrame(self.tab2, text="Consistance", font=("Helvetica", 13))
        self.fr_const.place(x=17, y=10, width=708, height=170)

        consist = Label(self.fr_const, text="Consistance Actuelle", font=("Helvetica", 12))
        consist.place(x=80, y=25)
        self.consistVal = Label(self.fr_const, text="", font=("Helvetica", 12))
        self.consistVal.place(x=265, y=25)

        consist = Label(self.fr_const, text="Nouvelle Consistance ", font=("Helvetica", 12))
        consist.place(x=80, y=65)
        const = Consistance_BE.Consistance()
        constVal = const.combxConst()
        consistance_var = StringVar()
        self.consComb= Autocompletecombox.Autocompletecombox(self.fr_const, textvariable=consistance_var, width=22, font=("Helvetica", 12))
        self.consComb.set_completion_list(constVal)
        self.consComb.place(x=265, y=65)

        modifier = Button(self.fr_const, text="Modifier", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF",relief=FLAT, activebackground="#9FE5D7", activeforeground="#E8B24D", command=self.updateConsist)
        modifier.place(x=530, y=60)

                                                 # *************** -- TAB3 -- Type de sol  ************
        self.tab3 = ttk.Frame(self.nBk)
        self.nBk.add(self.tab3, text="Type de sol")
        self.fr_sol = LabelFrame(self.tab3, text="Type de sol", font=("Helvetica", 13))
        self.fr_sol.place(x=17, y=10, width=708, height=170)

        typeSol = Label(self.fr_sol, text="Type de sol", font=("Helvetica", 12))
        typeSol.place(x=80, y=25)
        self.solVal = Label(self.fr_sol, text="", font=("Helvetica", 12))
        self.solVal.place(x=265, y=25)

        sol = Label(self.fr_sol, text="Nouveau type de sol ", font=("Helvetica", 12))
        sol.place(x=80, y=65)
        tpsol = TypeSol_BE.TypeSol()
        value = tpsol.combxTpsol()
        typesol_var = StringVar()
        self.sol_box = Autocompletecombox.Autocompletecombox(self.fr_sol, textvariable=typesol_var, width=22, font=("Helvetica", 12))
        self.sol_box.set_completion_list(value)
        self.sol_box.place(x=265, y=65)

        modifier = Button(self.fr_sol, text="Modifier", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#9FE5D7", activeforeground="#E8B24D", command=self.updateSol)
        modifier.place(x=530, y=60)

                                                 # *************** -- TAB4 -- Type de spéculation  ************
        self.tab4 = ttk.Frame(self.nBk)
        self.nBk.add(self.tab4, text="Type de spéculation")
        self.fr_specul = LabelFrame(self.tab4, text="Type de spéculation", font=("Helvetica", 13))
        self.fr_specul.place(x=17, y=10, width=708, height=170)

        typeSol = Label(self.fr_specul, text="Type de spéculation", font=("Helvetica", 12))
        typeSol.place(x=70, y=25)
        self.speclVal = Label(self.fr_specul, text="", font=("Helvetica", 12))
        self.speclVal.place(x=275, y=25)

        spec = Label(self.fr_specul, text="Nouveau type de spéculation", font=("Helvetica", 11))
        spec.place(x=70, y=65)
        self.Spec_var = StringVar()
        specl = TypeSpecl_BE.TypeSpecul()
        value = specl.combxTpSpecl()
        self.specBox = Autocompletecombox.Autocompletecombox(self.fr_specul, textvariable=self.Spec_var, width=22, font=("Helvetica", 12))
        self.specBox.set_completion_list(value)
        self.specBox.place(x=275, y=65)

        modifier = Button(self.fr_specul, text="Modifier", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#9FE5D7", activeforeground="#E8B24D", command=self.updateSpecul)
        modifier.place(x=540, y=60)

                                                                    # *************** -- TAB5 -- PRÉSUME  ************
        self.tab5 = ttk.Frame(self.nBk)
        self.nBk.add(self.tab5, text="Présumé")

        self.lf2 = LabelFrame(self.tab5, text="Modifier les informations de Présumé", font=("Helvetica", 13))
        self.lf2.place(x=20, y=10, width=708, height=370)

        Prenom = Label(self.lf2, text="Prénom", font=("Helvetica", 12))
        Prenom.place(x=46, y=20)
        self.prnm_Var = StringVar()
        self.prnm = Entry(self.lf2, textvariable=self.prnm_Var, width=21, font=("Helvetica", 12), relief=FLAT,  bg="#F7F9F9")
        self.prnm.place(x=159, y=20)

        PrenomAr = Label(self.lf2, text="الاسم الشخصي", font=("Helvetica", 12))
        PrenomAr.place(x=584, y=20)
        self.prnmAr_var = StringVar()
        self.prnm_Ent = Entry(self.lf2, textvariable=self.prnmAr_var, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.prnm_Ent.place(x=355, y=20)

        nom = Label(self.lf2, text="Nom", font=("Helvetica", 12))
        nom.place(x=56, y=60)
        self.nm_var = StringVar()
        self.nm = Entry(self.lf2, textvariable=self.nm_var, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.nm.place(x=159, y=60)

        nomAr = Label(self.lf2, text="الاسم العائلي", font=("Helvetica", 12))
        nomAr.place(x=597, y=60)
        self.nmAr_var = StringVar()
        self.nm_Ent = Entry(self.lf2, textvariable=self.nmAr_var, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.nm_Ent.place(x=355, y=60)

        adress = Label(self.lf2, text="L'adresse", font=("Helvetica", 12))
        adress.place(x=40, y=100)
        self.add_var = StringVar()
        self.add_Ent = Entry(self.lf2, textvariable=self.add_var, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.add_Ent.place(x=159, y=100)

        adressAr = Label(self.lf2, text="العنوان", font=("Helvetica", 12))
        adressAr.place(x=608, y=100)
        self.addAr_var = StringVar()
        self.addAr_Ent = Entry(self.lf2, textvariable=self.addAr_var, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.addAr_Ent.place(x=355, y=100)

        cin = Label(self.lf2, text="CIN", font=("Helvetica", 12))
        cin.place(x=60, y=140)
        self.cin_Var = StringVar()
        self.cin_Ent = Entry(self.lf2, textvariable=self.cin_Var, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.cin_Ent.place(x=159, y=140)

        tel = Label(self.lf2, text="Tel", font=("Helvetica", 12))
        tel.place(x=60, y=180)
        self.tel_Var = StringVar()
        self.tel_Ent = Entry(self.lf2, textvariable=self.tel_Var, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.tel_Ent.place(x=159, y=180)

        tel2 = Label(self.lf2, text="Tel 2", font=("Helvetica", 12))
        tel2.place(x=59, y=220)
        self.tel2_Var = StringVar()
        self.tel2_Ent = Entry(self.lf2, textvariable=self.tel2_Var, width=21, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.tel2_Ent.place(x=159, y=220)

        dateNss = Label(self.lf2, text="Date de naissance", font=("Helvetica", 12))
        dateNss.place(x=10, y=260)
        self.dt_var = StringVar()
        self.dNss_Ent = DateEntry(self.lf2, textvariable=self.dt_var, date_pattern='dd-mm-yyyy', width=20, font=("Helvetica", 12))
        self.dNss_Ent.place(x=159, y=260)
        self.dNss_Ent.config(selectbackground='gray80',
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



                                                            # *************** -- TAB6 -- OPPOSANT  ************
        self.tab6 = ttk.Frame(self.nBk)
        self.nBk.add(self.tab6, text="Opposants")
        '''sty_tree = ttk.Style(self)
        sty_tree.theme_use('clam')
        sty_tree.configure("Treeview", background="#FFFFFF", foreground="#14566D")
        sty_tree.configure("Treeview.Heading", background="#8CC7DC", foreground="#0D4EA2")'''

        self.tree = ttk.Treeview(self.tab6)
        self.tree.place(x=3, y=5, width=725, height=417)

        xsb = ttk.Scrollbar(self.tab6, orient='horizontal', command=self.tree.xview)
        xsb.place(x=3, y=412, width=722)
        self.tree['xscroll'] = xsb.set
        self.tree.configure(yscrollcommand=xsb.set)

        ysb = ttk.Scrollbar(self.tab6, orient='vertical', command=self.tree.yview)
        ysb.place(x=725, y=5, height=421)
        self.tree['yscroll'] = ysb.set
        self.tree.configure(yscrollcommand=ysb.set)

        self.col_name = self.prs.columnName()
        self.tree["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        self.tree['show'] = 'headings'
        for c in range(len(self.tree["columns"])):
            self.tree.column(c, width=120)
            self.tree.heading(c, text=self.col_name[c])
            index = iid = 0
            self.tree.insert("", index, iid, values="")
            index = iid = index + 1
        self.tree.bind("<Double-1>", self.OnDoubleClick)


                                                        # *************** -- TAB7 -- ajouter opposant  ************
        self.tab7 = ttk.Frame(self.nBk)
        self.nBk.add(self.tab7, text="Ajouter un opposant")

        btn = Button(self.tab7, text="Séléctionner Un Opposant Existant",font=("Helvetica", 13), command=self.selectOpp, relief=FLAT)
        btn.place(x=20, y=18)

        btn = Button(self.tab7, text="Ajouter un Nouveau Opposant",  font=("Helvetica", 13), command=self.newOpp, relief=FLAT)
        btn.place(x=350, y=18)


    def newOpp(self):
        # FRAME2
        lf = LabelFrame(self.tab7, text="Ajouter un Nouveau Opposant", font=("Helvetica", 13))
        lf.place(x=20, y=65, width=708, height=400)

        Prenom = Label(lf, text="Prénom ", font=("Helvetica", 12))
        Prenom.place(x=46, y=20)
        self.pren_Ent = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT)
        self.pren_Ent.place(x=158, y=20)
        PrenomAr = Label(lf, text="الاسم الشخصي", font=("Helvetica", 12))
        PrenomAr.place(x=585, y=20)
        self.prenAEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, justify='right')
        self.prenAEnt.place(x=354, y=20)

        nom = Label(lf, text="Nom", font=("Helvetica", 12))
        nom.place(x=56, y=60)
        self.nmEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT)
        self.nmEnt.place(x=158, y=60)
        nomAr = Label(lf, text="الاسم العائلي", font=("Helvetica", 12))
        nomAr.place(x=600, y=60)
        self.nmA_ent = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, justify='right')
        self.nmA_ent.place(x=354, y=60)

        adress = Label(lf, text="L'adresse", font=("Helvetica", 12))
        adress.place(x=55, y=100)
        self.adrEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT)
        self.adrEnt.place(x=158, y=100)
        adressAr = Label(lf, text="العنوان", font=("Helvetica", 12))
        adressAr.place(x=605, y=100)
        self.adA_ent = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT, justify='right')
        self.adA_ent.place(x=354, y=100)

        cin = Label(lf, text="CIN", font=("Helvetica", 12))
        cin.place(x=60, y=140)
        self.cinEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT)
        self.cinEnt.place(x=158, y=140)

        tel = Label(lf, text="Tel 1", font=("Helvetica", 12))
        tel.place(x=60, y=180)
        self.telEnt = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT)
        self.telEnt.place(x=158, y=180)

        tel2 = Label(lf, text="Tel 2", font=("Helvetica", 12))
        tel2.place(x=58, y=220)
        self.telEnt2 = Entry(lf, width=21, font=("Helvetica", 12), relief=FLAT)
        self.telEnt2.place(x=158, y=220)

        dateNss = Label(lf, text="Date de naissance", font=("Helvetica", 12))
        dateNss.place(x=10, y=260)
        dateNss_var = StringVar()
        self.dt_Ent = DateEntry(lf, textvariable=dateNss_var, date_pattern='dd-mm-yyyy', width=19, font=("Helvetica", 12))
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

        tpOpp = Label(lf, text="Type d'opposition", font=("Helvetica", 12))
        tpOpp.place(x=12, y=300)
        tpOpp_varb = StringVar()
        oppVal = self.oppTp.combxTpOpp()
        self.tpOpp_box = Autocompletecombox.Autocompletecombox(lf, textvariable=tpOpp_varb, font=("Times New Roman", 12), width=21)
        self.tpOpp_box.set_completion_list(oppVal)
        self.tpOpp_box.place(x=160, y=300)

        oppBtn = Button(lf, text="Ajouter", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#9FE5D7", activeforeground="#E8B24D", command=self.addOpp)
        oppBtn.place(x=320, y=340)


    def addOpp(self):
        prsn = self.prs.insertPerson(self.pren_Ent.get(), self.prenAEnt.get(), self.nmEnt.get(), self.nmA_ent.get(),
                                     self.adrEnt.get(), self.adA_ent.get(), self.cinEnt.get(), self.telEnt.get(),
                                     self.telEnt2.get(), self.dt_Ent.get())
        cls = self.cle.insertNew_CleOppo(self.tpOpp_box.get(), self.idparcelle.get())
        msg = messagebox.showinfo("Opposant", "Un nouveau opposant a été bien ajouté")


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
        cls = self.cle.add_NewOpposCle(self.opp_box.get(), self.cinBoxOpp.get(), self.idparcelle.get())
        typOpps = self.cle.updat_NewCleOppos(self.tpOpp_box.get(), self.opp_box.get(), self.cinBoxOpp.get(), self.idparcelle.get())
        msg = messagebox.showinfo("Opposant", "Un nouveau opposant a été bien ajouté")
        self.newroot.destroy()

    def OnDoubleClick(self, event):
        try:
            self.row_selected = self.tree.item(self.tree.selection())
            self.value = self.row_selected['values'][0]
            self.oppVal = self.prs.selectOppo(self.idparcelle.get(), self.value)
            self.motif = self.oppTp.motif_Opp(self.idparcelle.get())
            verify = self.prs.verifyPerson(str(self.value))

            if verify == True:
                self.root = Toplevel()
                self.root.title("Opposant")
                self.root.resizable(0, 0)
                self.root.geometry("684x445+277+150")
                self.root.config(bg="#F7F9F9")
                self.frameDoubleClick()

        except:
            messagebox.showerror("Sélectionner un opposant", "Veuillez sélectionner un opposant")

    def frameDoubleClick(self):
        lf2 = LabelFrame(self.root, text="Modifier Un Opposant", font=("Helvetica", 12), bg="#E3F3F3")
        lf2.place(x=7, y=8, width=670, height=430)

        Prenom = Label(lf2, text="Prénom", font=("Helvetica", 12), bg="#E3F3F3")
        Prenom.grid(row=1, column=0, padx=30)
        self.Prenom_entry = Entry(lf2, width=20, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.Prenom_entry.insert(1, self.oppVal[0][1])
        self.Prenom_entry.grid(row=1, column=1)

        PrenomAr = Label(lf2, text="الاسم الشخصي", font=("Helvetica", 12), bg="#E3F3F3")
        PrenomAr.grid(row=1, column=4, pady=15, padx=30)
        pnmAr_Var = StringVar()
        self.PrenomAr_entry = Entry(lf2, width=20, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.PrenomAr_entry.insert(1, self.oppVal[0][2])
        self.PrenomAr_entry.grid(row=1, column=3)

        nom = Label(lf2, text="Nom", font=("Helvetica", 12), bg="#E3F3F3")
        nom.grid(row=2, column=0)
        nom_Var = StringVar()
        self.nom_entry = Entry(lf2, width=20, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.nom_entry.insert(1, self.oppVal[0][3])
        self.nom_entry.grid(row=2, column=1)

        nomAr = Label(lf2, text="الاسم العائلي", font=("Helvetica", 12), bg="#E3F3F3")
        nomAr.grid(row=2, column=4)
        nomAr_Var = StringVar()
        self.nomAr_entry = Entry(lf2, width=20, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.nomAr_entry.insert(1, self.oppVal[0][4])
        self.nomAr_entry.grid(row=2, column=3)

        adress = Label(lf2, text="L'adresse", font=("Helvetica", 12), bg="#E3F3F3")
        adress.grid(row=3, column=0, pady=15)
        self.adress_entry = Entry(lf2, width=20, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.adress_entry.insert(1, self.oppVal[0][5])
        self.adress_entry.grid(row=3, column=1)

        adressAr = Label(lf2, text="العنوان", font=("Helvetica", 12), bg="#E3F3F3")
        adressAr.grid(row=3, column=4)
        self.adressAr_entry = Entry(lf2, width=20, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.adressAr_entry.insert(1, self.oppVal[0][6])
        self.adressAr_entry.grid(row=3, column=3)

        cin = Label(lf2, text="CIN", font=("Helvetica", 12), bg="#E3F3F3")
        cin.grid(row=4, column=0)
        self.cin_entry = Entry(lf2, width=20, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.cin_entry.insert(1, self.oppVal[0][7])
        self.cin_entry.grid(row=4, column=1)

        tel = Label(lf2, text="Tel", font=("Helvetica", 12), bg="#E3F3F3")
        tel.grid(row=5, column=0, pady=15)
        self.tel_entry = Entry(lf2, width=20, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.tel_entry.grid(row=5, column=1)
        if self.oppVal[0][8] == None:
            self.tel_entry.insert(1, '')
        elif self.oppVal[0][8] != '':
            self.tel_entry.insert(1, self.oppVal[0][8])

        tel2 = Label(lf2, text="Tel 2", font=("Helvetica", 12), bg="#E3F3F3")
        tel2.grid(row=6, column=0)
        self.tel2_entry = Entry(lf2, width=20, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9")
        self.tel2_entry.grid(row=6, column=1)
        if self.oppVal[0][9] == None:
            self.tel2_entry.insert(1, '')
        elif self.oppVal[0][9] != '':
            self.tel2_entry.insert(1, self.oppVal[0][9])

        dateNss = Label(lf2, text="Date de naissance", font=("Helvetica", 12), bg="#E3F3F3")
        dateNss.grid(row=7, column=0, pady=15)
        dateNss_var = StringVar()
        self.dateNss_entry = DateEntry(lf2, textvariable=dateNss_var, date_pattern='yyyy-mm-dd', width=19, font=("Helvetica", 12))
        self.dateNss_entry.grid(row=7, column=1)
        self.dateNss_entry.config(selectbackground='gray80',
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

        if self.oppVal[0][10] == None:
            self.dateNss_entry.insert(1, 'null')
        elif self.oppVal[0][10] != '':
            self.dateNss_entry.insert(1, self.oppVal[0][10])



        tpOpp = Label(lf2, text="Type d'opposition", font=("Helvetica", 12), bg="#E3F3F3")
        tpOpp.grid(row=8, column=0)
        tpOpp_varb = StringVar()
        oppVal = self.oppTp.combxTpOpp()
        self.row_selected = self.tree.item(self.tree.selection())
        self.tpOpp_box = Autocompletecombox.Autocompletecombox(lf2,  textvariable=tpOpp_varb,font=("Times New Roman", 12), width=20)
        self.tpOpp_box.set_completion_list(oppVal)
        self.tpOpp_box.grid(row=8, column=1)

        frm = Frame(lf2, bg="#379BF3", width=78, height=28)
        frm.place(x=215, y=350)
        btnUpdt = tk.Button(frm, text="Modifier", bg="#CEE6F3", font=("Times New Roman", 13), fg="#379BF3", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.updtOppos)
        btnUpdt.place(x=1, y=1, height=26)

        frm2 = Frame(lf2, bg="#F9983F", width=87, height=28)
        frm2.place(x=350, y=350)
        btnUpdt = tk.Button(frm2, text="Supprimer", bg="#CEE6F3", font=("Times New Roman", 13), fg="#F9983F", relief='flat', activebackground="#CEE6F3", activeforeground="#379BF3", command=self.noo)
        btnUpdt.place(x=1, y=1, height=26)


    def updtOppos(self):
        oppVal = self.prs.modifyOpp(self.dateNss_entry.get(), self.Prenom_entry.get(), self.PrenomAr_entry.get(), self.nom_entry.get(), self.nomAr_entry.get(), self.adress_entry.get(), self.adressAr_entry.get(), self.cin_entry.get(), self.tel_entry.get(), self.tel2_entry.get(), self.dateNss_entry.get(), self.value)
        cles = self.cle.updat_ClesOppos(self.tpOpp_box.get(), self.value, self.idparcelle.get())
        self.tree.delete(*self.tree.get_children())

        list = self.prs.researOppo(self.idparcelle.get())
        index = iid = 0
        for item in list:
            self.tree.insert("", index, iid, values=item)
            index = iid = index + 1
        msg = messagebox.showinfo("Modifier l'opposant", "Modification effectuée avec succès")

        self.root.destroy()

    def noo(self):
        deletCle = self.cle.delet_CleOppo(self.idparcelle.get(), self.value)
        x = self.tree.selection()[0]
        self.tree.delete(x)
        msg = messagebox.showinfo("Supprimer", "Suppression effectuée avec succès")

 #------------------------------------------------------------------------------------------------------------------------------
 #------------------------------------------------------------------------------------------------------------------------------


    def values(self):
                                                        # --------------------- Vider les inputs ------------------------
        try:
            x = self.idparcelle.get()
            if x != '':
                try:
                    idval = self.polg.verifyPolyg(self.idparcelle.get())
                    valPolg = self.polg.researchPolyg(self.idparcelle.get())
                    start = DetailMap.DetailMap(self.canv, valPolg[0])

                    if idval == True:
# TAB 1
                        self.idP.config(text="")
                        self.zn.config(text="")
                        self.sz.config(text="")
                        self.drLabel.config(text="")
                        self.nomFr_ent.delete(0, 'end')
                        self.nomAr_ent.delete(0, 'end')

# TAB 2
                        self.consistVal.config(text="")

# TAB 3
                        self.solVal.config(text="")

# TAB 4
                        self.speclVal.config(text="")

# TAB 5
                        self.prnm.delete(0, 'end')
                        self.prnm_Ent.delete(0, 'end')
                        self.nm.delete(0, 'end')
                        self.nm_Ent.delete(0, 'end')
                        self.add_Ent.delete(0, 'end')
                        self.addAr_Ent.delete(0, 'end')
                        self.cin_Ent.delete(0, 'end')
                        self.tel_Ent.delete(0, 'end')
                        self.tel2_Ent.delete(0, 'end')
                        self.dNss_Ent.delete(0, 'end')

# TAB 6
                        self.tree.delete(*self.tree.get_children())

                                                    # ---------------------- AFFICHER LES VALEURS ------------------
# TAB 1
                        zn = Zone_BE.Zone()
                        znVal = zn.selectZn(self.idparcelle.get())
                        sz = SousZone_BE.SousZ()
                        szVal = sz.selectSZ(self.idparcelle.get())
                        dr = Douar_BE.Douar()
                        drVal = dr.selectDr(self.idparcelle.get())
                        self.idP.config(text=str(valPolg[0]))
                        self.zn.config(text=str(znVal[0][0]))
                        self.sz.config(text=str(szVal[0][0]))
                        self.drLabel.config(text=str(drVal[0][0]))
                        self.nomFr_ent.insert(1, valPolg[1])
                        self.nomAr_ent.insert(1, valPolg[2])
                        # const = Consistance_BE.Consistance()
                        # val = const.constVal(self.idparcelle.get())
                        # print(val[0])
                        # self.consComb.current(val[0])

# TAB 2
                        const = self.consist.researPoly_Cons(self.idparcelle.get())
                        self.consistVal.config(text=str(const[0]))

# TAB 3
                        sol_value = self.sol.researPoly_Sol(self.idparcelle.get())
                        self.solVal.config(text=sol_value[0])

# TAB 4
                        specl_value = self.specl.researPoly_Spec(self.idparcelle.get())
                        self.speclVal.config(text=specl_value[0])

# tab 5
                        updtBtn = Button(self.lf2, text="Modifier", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT,activebackground="#9FE5D7", activeforeground="#E8B24D", command = self.updtPres)
                        updtBtn.place(x=320, y=310)
                        prsVal = self.prs.researPres(self.idparcelle.get())

                        #if prsVal[0] != '' or prsVal[0] == None:
                        self.prnm.insert(1, prsVal[1])
                        self.prnm_Ent.insert(1, prsVal[2])
                        self.nm.insert(1, prsVal[3])
                        self.nm_Ent.insert(1, prsVal[4])
                        self.add_Ent.insert(1, prsVal[5])
                        self.addAr_Ent.insert(1, prsVal[6])
                        self.cin_Ent.insert(1, prsVal[7])

                        if prsVal[8] == None:
                            self.tel_Ent.insert(1, '')
                        elif prsVal[8] != '':
                            self.tel_Ent.insert(1, prsVal[8])

                        if prsVal[9] == None:
                            self.tel2_Ent.insert(1, '')
                        elif prsVal[9] != '':
                            self.tel2_Ent.insert(1, prsVal[9])

                        if prsVal[10] == None:
                            self.dNss_Ent.insert(1, '')
                        elif prsVal[10] != '':
                            self.dNss_Ent.insert(1, prsVal[10])

# TAB 6
                        list = self.prs.researOppo(self.idparcelle.get())
                        index = iid = 0
                        for item in list:
                            self.tree.insert("", index, iid, values=item)
                            index = iid = index + 1
                    else:
                        raise PolygError.PolygError
                except PolygError.PolygError:
                    msg = messagebox.showerror("Parcelle", "La parcelle que vous avez choisi n'exsiste pas")
            else:
                raise IdError.IdError
        except IdError.IdError:
            msg2 = messagebox.showerror("Parcelle", "Veuillez saisir un ID")

    def updtPolyg(self):
        updtPoly = self.polg.updatPoly(self.nomFr_ent.get(), self.nomAr_ent.get(),self.idparcelle.get())

    def updtPres(self):
        prsVal = self.prs.researPres(self.idparcelle.get())
        upPrm = self.prs.modifyPresm(self.tel_Ent.get(), self.tel2_Ent.get(), self.dNss_Ent.get(), self.prnm.get(), self.prnm_Ent.get(), self.nm.get(), self.nm_Ent.get(), self.add_Ent.get(), self.addAr_Ent.get(), self.cin_Ent.get(), self.tel_Ent.get(), self.tel2_Ent.get(), self.dNss_Ent.get(), prsVal[0])
        msg = messagebox.showinfo("Modifier le présumé", "Modification effectuée avec succès")

    def updateConsist(self):
        self.polg.modify_const(self.consComb.get(), self.idparcelle.get())
        const = self.consist.researPoly_Cons(self.idparcelle.get())
        self.consistVal.config(text=str(const[0]))
        msg = messagebox.showinfo("Modifier la consistance", "Modification effectuée avec succès")

    def updateSol(self):
        self.polg.modify_Tpsol(self.sol_box .get(), self.idparcelle.get())
        msg = messagebox.showinfo("Modifier le type de sol", "Modification effectuée avec succès")
        sol_value = self.sol.researPoly_Sol(self.idparcelle.get())
        self.solVal.config(text=sol_value[0])

    def updateSpecul(self):
        self.polg.modify_specul(self.specBox.get(), self.idparcelle.get())
        msg = messagebox.showinfo("Modifier le type de spéculation", "Modification effectuée avec succès")
        specl_value = self.specl.researPoly_Spec(self.idparcelle.get())
        self.speclVal.config(text=specl_value[0])

#app = ModifyPolyg()
#app.mainloop()