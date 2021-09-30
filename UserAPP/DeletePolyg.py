from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkcalendar import Calendar, DateEntry
from tkinter.messagebox import *
from UserAPP.Parcelle_BE import Parcelle
from UserAPP import Douar_BE
from UserAPP import SousZone_BE
from UserAPP import Zone_BE
from UserAPP import Marche_BE
from UserAPP import Personnes_BE
from UserAPP import Cles
from Exceptions import PolygError
from Exceptions import IdError
from tkinter import messagebox
from UserAPP import DetailMap
from AdminAPP import Rivrain_BE

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

class DeletePolyg(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Suppression")
        self.geometry("980x480+220+110")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.polyg = Parcelle()
        self.dr = Douar_BE.Douar()
        self.sz = SousZone_BE.SousZ()
        self.zn = Zone_BE.Zone()
        self.mr = Marche_BE.Marche()
        self.prs = Personnes_BE.Personnes()
        self.cls = Cles.Cles()

        self.researchFrame()
        self.canvasFrame()
        self.infoFrame()


                                # ----------------------------- Frame pour chercher la parcelle ---------------------------------
    def researchFrame(self):

        top_frame = Frame(self, bg="white")
        top_frame.pack(side=TOP, fill=X, pady=2)

        self.idparcelle = tk.Entry(top_frame, font=("Helvetica", 13), relief=FLAT, bg="#F7F9F9", width=40)
        self.idparcelle.pack(side=LEFT, padx=100, pady=2)
        add_placeholder_to(self.idparcelle, "Id parcelle")

        id_btn = Button(top_frame, text="Rechercher", bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, command=self.polygVal)
        id_btn.pack(side=LEFT, padx=2, pady=2)


                                # ----------------------------- CANVAS Pour afficher la parcelle -------------------
    def canvasFrame(self):
        self.canv = Canvas(self, bg="#FFFFFF", width=340, height=500)
        self.canv.place(x=635, y=33)


        # ----------------------------- Frame informations ----------------------
    def infoFrame(self):
        self.frm = Frame(self, bg="black", width=630, height=443)
        self.frm.place(x=2, y=34)
        self.frm2 = Frame(self.frm, bg="#E3F3F3", width=628, height=441)
        self.frm2.place(x=1, y=1)
        idPrcel = Label(self.frm2, text="Parcelle Nº: ", font=("Helvetica", 15), bg="#E3F3F3")
        idPrcel.place(x=20, y=30)
        self.idparcel = Label(self.frm2, text="", font=("Helvetica", 15), bg="#E3F3F3")
        self.idparcel.place(x=130, y=30)

        sec = Label(self.frm2, text="Zone:", font=("Helvetica", 12), bg="#E3F3F3")
        sec.place(x=125, y=75)
        self.znLbl = Label(self.frm2, text="", font=("Helvetica", 12), bg="#E3F3F3")
        self.znLbl.place(x=172, y=75)

        ssec = Label(self.frm2, text="Sous Zone:", font=("Helvetica", 12), bg="#E3F3F3")
        ssec.place(x=330, y=75)
        self.szLbl = Label(self.frm2, text="", font=("Helvetica", 12), bg="#E3F3F3")
        self.szLbl.place(x=420, y=75)

        label = Label(self.frm2, text="Propriete dite", font=("Helvetica", 12), bg="#E3F3F3")
        label.place(x=15, y=120)
        self.parcel_Var = StringVar()
        self.parcel = Entry(self.frm2, textvariable=self.parcel_Var, width=22, font=("Helvetica", 12), relief=FLAT,bg="#F7F9F9")
        self.parcel.place(x=124, y=120)

        label = Label(self.frm2, text="الملك المسمى", font=("Helvetica", 12), bg="#E3F3F3")
        label.place(x=541, y=120)
        self.parcelAr_Var = StringVar()
        self.parcelAr = Entry(self.frm2, textvariable=self.parcelAr_Var, width=22, font=("Helvetica", 12), relief=FLAT, bg="#F7F9F9", justify='right')
        self.parcelAr.place(x=331, y=120)

        douar = Label(self.frm2, text="Douar", font=("Helvetica", 12), bg="#E3F3F3")
        douar.place(x=38, y=160)
        self.douar_Var = StringVar()
        self.douarFR = Entry(self.frm2, textvariable=self.douar_Var, width=22, font=("Helvetica", 12), relief=FLAT,bg="#F7F9F9")
        self.douarFR.place(x=125, y=160)

        douar = Label(self.frm2, text="الدوار", font=("Helvetica", 12), bg="#E3F3F3")
        douar.place(x=558, y=160)
        self.douarAr_Var = StringVar()
        self.douarAr = Entry(self.frm2, textvariable=self.douarAr_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                             bg="#F7F9F9", justify='right')
        self.douarAr.place(x=330, y=160)

        srf = Label(self.frm2, text="Surface ", font=("Helvetica", 12), bg="#E3F3F3")
        srf.place(x=32, y=200)
        self.area_Var = StringVar()
        self.areaFr = Entry(self.frm2, textvariable=self.area_Var, width=22, font=("Helvetica", 12), relief=FLAT,bg="#F7F9F9")
        self.areaFr.place(x=125, y=200)

        label = Label(self.frm2, text="المساحة", font=("Helvetica", 12), bg="#E3F3F3")
        label.place(x=555, y=200)
        self.areaAr_Var = StringVar()
        self.areaAr = Entry(self.frm2, textvariable=self.areaAr_Var, width=22, font=("Helvetica", 12), relief=FLAT,
                            bg="#F7F9F9", justify='right')
        self.areaAr.place(x=330, y=200)

        nomFr = Label(self.frm2, text="Présumé", font=("Helvetica", 12), bg="#E3F3F3")
        nomFr.place(x=30, y=240)
        self.prnmFr_Var = StringVar()
        self.prnmFr = Entry(self.frm2, textvariable=self.prnmFr_Var, width=45, font=("Helvetica", 12), relief=FLAT,  bg="#F7F9F9")
        self.prnmFr.place(x=125, y=240)

        nomAr = Label(self.frm2, text="المالك", font=("Helvetica", 12), bg="#E3F3F3")
        nomAr.place(x=561, y=280)
        self.prnm_Var = StringVar()
        self.prnmAr = Entry(self.frm2, textvariable=self.prnm_Var, width=45, font=("Helvetica", 12), relief=FLAT,  bg="#F7F9F9", justify=RIGHT)
        self.prnmAr.place(x=125, y=280)

    def polygVal(self):
        try:
            x = self.idparcelle.get()
            if x != '':
                try:
                    values = self.polyg.researchPolyg(self.idparcelle.get())
                    dr = self.dr.selectDr(self.idparcelle.get())
                    sz = self.sz.selectSZ(self.idparcelle.get())
                    zn = self.zn.selectZn(self.idparcelle.get())
                    self.person = Personnes_BE.Personnes.prsm_xml(self, self.idparcelle.get())
                    idval = self.polyg.verifyPolyg(self.idparcelle.get())
                    if idval == True:
                        start = DetailMap.DetailMap(self.canv, values[0])

# VIDER LES LABLES
                        self.idparcel.config(text="")
                        self.znLbl.config(text="")
                        self.szLbl.config(text="")
                        self.parcel.delete(0, 'end')
                        self.parcelAr.delete(0, 'end')
                        self.douarFR.delete(0, 'end')
                        self.douarAr.delete(0, 'end')
                        self.areaFr.delete(0, 'end')
                        self.areaAr.delete(0, 'end')
                        self.prnmFr.delete(0, 'end')
                        self.prnmAr.delete(0, 'end')

# AFFICHER LES VALEURS
                        self.idparcel.config(text=str(values[0]))
                        self.znLbl.config(text=str(zn[0][0]))
                        self.szLbl.config(text=str(sz[0][0]))
                        self.parcel.insert(1, values[1])
                        self.parcelAr.insert(1, values[2])
                        self.douarFR.insert(1, dr[0][0])
                        self.douarAr.insert(1, dr[0][1])
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
                        verifyPres = self.prs.verifyPersonne(self.idparcelle.get())
                        if verifyPres == True:
                            presumFR = self.person[0][1] + ' ' + self.person[0][3]
                            presumeAr = self.person[0][2] + ' ' + self.person[0][4]
                            self.prnmFr.insert(1, presumFR)
                            self.prnmAr.insert(1, presumeAr)
                        else:
                            msg = messagebox.showerror("Présumé", "Aucun présumé enregistré pour cette parcelle")
                        delBtn = Button(self.frm2, text="Supprimer", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#9FE5D7", activeforeground="#E8B24D", command=self.delete)
                        delBtn.place(x=280, y=350)

                    else:
                        raise PolygError.PolygError

                except PolygError.PolygError:
                    msg = messagebox.showerror("Parcelles", "La parcelle que vous avez choisi n'exsiste pas")
            else:
                raise IdError.IdError
        except IdError.IdError:
            msg2 = messagebox.showerror("Parcelles", "Veuillez saisir un ID")

    def delete(self):
        self.popinfos = tk.Toplevel()
        self.popinfos.title('Supression')
        self.popinfos.resizable(0, 0)
        self.popinfos.config(bg="#F7F9F9")
        self.popinfos.geometry("368x120+500+300")
        label = tk.Label(self.popinfos, text="Voulez-vous supprimer cette parcelle ?",
                         font=("Helvetica", 12), pady=13, padx=20, bg="#F7F9F9").grid(row=0, column=0)
        btn1 = tk.Button(self.popinfos, text='Oui', command=self.supprimer, font=("Times New Roman", 11),
                         bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA",
                         activeforeground="#000000")
        btn1.place(x=148, y=70)
        btn2 = tk.Button(self.popinfos, text='Non', command=self.annuler, font=("Times New Roman", 11),
                         fg="#FFFFFF", bg="#FF862E", relief=FLAT, activebackground="#FF8A02", activeforeground="#000000")
        btn2.place(x=200, y=70)

    def supprimer(self):
        dd = self.cls.delete(self.idparcelle.get())
        d = self.polyg.delete(self.idparcelle.get())
        r = Rivrain_BE.Rivrains.delete(self.idparcelle.get(), self.idparcelle.get())
        self.popinfos.destroy()
        showinfo("Parcelles", "Suppression effectuée avec succès")

        self.idparcel.config(text="")
        self.znLbl.config(text="")
        self.szLbl.config(text="")
        self.parcel.delete(0, 'end')
        self.parcelAr.delete(0, 'end')
        self.douarFR.delete(0, 'end')
        self.douarAr.delete(0, 'end')
        self.areaFr.delete(0, 'end')
        self.areaAr.delete(0, 'end')
        self.prnmFr.delete(0, 'end')
        self.prnmAr.delete(0, 'end')
    def annuler(self):
        self.popinfos.destroy()


#app = DeletePolyg()
#app.mainloop()