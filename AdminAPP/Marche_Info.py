from tkinter import *
import tkinter as tk
from  tkinter import messagebox
from UserAPP import Marche_BE

class Info_Marche(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('790x470+310+80')
        self.config(bg="#F7F9F9")
        self.resizable(0, 0)
        self.title("EpGIS")

        marche = Marche_BE.Marche()
        x = marche.selectValues()
        lbFrm = LabelFrame(self, text="Modifier le Marché", font=("Times New Roman", 18),  bg="#F7F9F9", width=770, height=450)
        lbFrm.place(x=10, y=10)
        if x[1] != '':
            marche = Label(lbFrm, text="Marché", font=("Times New Roman", 13), bg="#F7F9F9")
            marche.place(x=76, y=20)
            self.marche_entr = Entry(lbFrm, width=53, relief='flat', font=("Times New Roman", 11))
            self.marche_entr.insert(1, x[1])
            self.marche_entr.place(x=210, y=20)

            sectr = Label(lbFrm, text="Secteur", font=("Helvetica", 13), bg="#F7F9F9")
            sectr.place(x=75, y=60)
            self.secteur_entr = Entry(lbFrm, width=53, relief='flat', font=("Times New Roman", 11))
            self.secteur_entr.insert(1, x[2])
            self.secteur_entr.place(x=210, y=60)

            cercle = Label(lbFrm, text="Cercle", font=("Helvetica", 13), bg="#F7F9F9")
            cercle.place(x=76, y=100)
            self.cercle_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
            self.cercle_entr.insert(1, x[3])
            self.cercle_entr.place(x=210, y=100)

            cercle_ar = tk.Label(lbFrm, text="الدائرة", font=("Times New Roman", 13), bg="#F7F9F9")
            cercle_ar.place(x=664, y=100)
            self.cercleAr_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11), justify=RIGHT)
            self.cercleAr_entr.insert(1, x[4])
            self.cercleAr_entr.place(x=400, y=100)

            province = tk.Label(lbFrm, text="Province", font=("Times New Roman", 13), bg="#F7F9F9")
            province.place(x=74, y=140)
            self.province_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
            self.province_entr.insert(1, x[5])
            self.province_entr.place(x=210, y=140)

            province_ar = tk.Label(lbFrm, text="الاقليم", font=("Times New Roman", 13), bg="#F7F9F9")
            province_ar.place(x=666, y=140)
            self.provinceAR_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11), justify=RIGHT)
            self.provinceAR_entr.insert(1, x[6])
            self.provinceAR_entr.place(x=400, y=140)

            commune = tk.Label(lbFrm, text="Commune", font=("Times New Roman", 13), bg="#F7F9F9")
            commune.place(x=75, y=180)
            self.commune_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
            self.commune_entr.insert(1, x[7])
            self.commune_entr.place(x=210, y=180)

            commune = tk.Label(lbFrm, text="الجماعة", font=("Times New Roman", 13), bg="#F7F9F9")
            commune.place(x=665, y=180)
            self.communeAr_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11), justify=RIGHT)
            self.communeAr_entr.insert(1, x[8])
            self.communeAr_entr.place(x=400, y=180)

            consr_fonc = Label(lbFrm, text="Conservation foncière", font=("Times New Roman", 13), bg="#F7F9F9")
            consr_fonc.place(x=25, y=220)
            self.consFonc_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11), justify=RIGHT)
            self.consFonc_entr.insert(1, x[9])
            self.consFonc_entr.place(x=210, y=220)

            consr_fonc = Label(lbFrm, text="المحافظة العقارية", font=("Times New Roman", 13), bg="#F7F9F9")
            consr_fonc.place(x=640, y=220)
            self.consFonc_entr_Ar = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11), justify=RIGHT)
            self.consFonc_entr_Ar.insert(1, x[10])
            self.consFonc_entr_Ar.place(x=400, y=220)

            geom = tk.Label(lbFrm, text="Géomètre", font=("Times New Roman", 13), bg="#F7F9F9")
            geom.place(x=72, y=260)
            self.geom_entr = Entry(lbFrm, width=53, relief='flat', font=("Times New Roman", 11))
            self.geom_entr.insert(1, x[11])
            self.geom_entr.place(x=210, y=260)

            bul_off = tk.Label(lbFrm, text="Bulltin oficiel", font=("Times New Roman", 13), bg="#F7F9F9")
            bul_off.place(x=56, y=300)
            self.bulOff_entr = Entry(lbFrm, width=53, relief='flat', font=("Times New Roman", 11))
            self.bulOff_entr.insert(1, x[12])
            self.bulOff_entr.place(x=210, y=300)

            create_btn = Button(lbFrm, text="Modifier", width=8, relief='flat', font=("Times New Roman", 12), fg="#FFFFFF", bg="#379BF3", command=self.modify)
            create_btn.place(x=360, y=360)
        else:
            messagebox.showerror("Marché", "Aucun marché trouvé")

    def modify(self):
        if(self.marche_entr.get() != ''):
            marche = Marche_BE.Marche()
            marche.modifyValues(self.marche_entr.get(), self.secteur_entr.get(), self.cercle_entr.get(), self.cercleAr_entr.get(), self.province_entr.get(), self.provinceAR_entr.get(),
            self.commune_entr.get(), self.communeAr_entr.get(), self.consFonc_entr.get(), self.consFonc_entr_Ar.get(), self.geom_entr.get(), self.bulOff_entr.get())
            msg = messagebox.showinfo("Informations de marché", "Modification effectuée avec succès")
            #self.destroy()
        else:
            messagebox.showinfo("Erreur", "Veuillez entrer le nom du marche")

    def quiter(self):
        self.controller.destroy()

#app = Info_Marche()
#app.mainloop()