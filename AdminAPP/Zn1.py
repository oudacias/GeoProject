import tkinter as tk
from tkinter import *
from UserAPP import Autocompletecombox
from UserAPP import Personnes_BE
from UserAPP import SousZone_BE
from UserAPP import Marche_BE
from UserAPP import Douar_BE
from UserAPP import Parcelle_BE
from UserAPP import TypeSpecl_BE
from UserAPP import TypeSol_BE
from UserAPP import Consistance_BE
from UserAPP import Cles
from AdminAPP import Zn1_Word_Pdf
from tkinter.messagebox import *
#----------------------------------------------------------------- PlaceHolder ---------------------------------------------------------------------------
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
class Zn1(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("ZN1")
        self.geometry("450x240+430+180")
        self.resizable(0, 0)
        self.config(bg="#F7F9F9")

        frmLab = LabelFrame(self, text="ZN1", font=("Times New Roman", 14), bg="#F7F9F9")
        frmLab.place(x=10, y=5, width=430, height=225)

        idPolyg = tk.Label(frmLab, text="Id parcelle", fg="#3B3F42", bg="#F7F9F9", font=("Helvetica", 12))
        idPolyg.place(x=38, y=25)
        frm = Frame(frmLab, bg="#CEE6F3", width=240, height=24)
        frm.place(x=150, y=25)
        self.idEnt = tk.Entry(frm, width=26, relief='flat', bg="#F7F9F9", font=("Helvetica", 12))
        self.idEnt.place(x=1, y=1)
        add_placeholder_to(self.idEnt, 'Id Parcelle')

        idPolyg = tk.Label(frmLab, text="Format", fg="#3B3F42", bg="#F7F9F9", font=("Helvetica", 12))
        idPolyg.place(x=48, y=75)
        vfVal = ['WORD', 'PDF']
        fv_var = StringVar()
        frm2 = Frame(frmLab, bg="#CEE6F3", width=240, height=26)
        frm2.place(x=150, y=75)
        self.fv_box = Autocompletecombox.Autocompletecombox(frm2, textvariable=fv_var, width=24, font=("Helvetica", 12))
        self.fv_box.set_completion_list(vfVal)
        self.fv_box.place(x=1, y=1)

        btn = Button(frmLab, text="Générer", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, activebackground="#4EB1FA", activeforeground="#000000", command=self.generate)
        btn.place(x=200, y=140)

    def generate(self):
        if self.idEnt.get() != '' and self.fv_box.get()!= '':
            self.polyg = Parcelle_BE.Parcelle.researchPolyg(self, self.idEnt.get())
            idval = Parcelle_BE.Parcelle.verifyPolyg(self, self.idEnt.get())
            if idval == True:
                self.person = Personnes_BE.Personnes.prsm_xml(self, self.idEnt.get())
                self.sz = SousZone_BE.SousZ.selectSZ(self, self.idEnt.get())
                self.mrch = Marche_BE.Marche.info_marche(self)
                self.dr = Douar_BE.Douar.xmlDr(self, self.idEnt.get())
                self.tpSol = TypeSol_BE.TypeSol.sol_xml(self, self.idEnt.get())
                self.tpSpecl = TypeSpecl_BE.TypeSpecul.spec_xml(self, self.idEnt.get())
                self.consist = Consistance_BE.Consistance.Const_xml(self, self.idEnt.get())
                self.oppos = Cles.Cles.opposition_pieces(self, self.idEnt.get())
                if self.fv_box.get() == 'WORD':
                    self.word()
                elif self.fv_box.get() == 'PDF':
                    self.pdf()
            else:
                showerror("ZN1", "Id parcelle est invalide")
        else:
            showerror("ZN1", "Veuillez remplir tous les champs ")

    def word(self):
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

    def pdf(self):
        person1 = str(self.person[0][1])
        person3 = str(self.person[0][3])
        mrch1 = str(self.mrch[1])
        sz = str(self.sz[0][1])
        mrch0 = str(self.mrch[0])
        mrch2 = str(self.mrch[2])
        person5 = str(self.person[0][5])
        person7 = str(self.person[0][7])
        if self.person[0][8] == None:
            person8 = ''
        elif self.person[0][8] != '':
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



'''if __name__ == "__main__":
    app = Zn1()
    app.mainloop()'''