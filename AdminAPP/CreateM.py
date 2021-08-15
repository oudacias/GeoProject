from tkinter import *
import tkinter as tk
from  tkinter import messagebox
from UserAPP import Marche_BE
from UserAPP import OpenM
from AdminAPP import MainAdmin

class Creatproject(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('790x500+310+80')
        self.config(bg="#F7F9F9")
        self.resizable(0, 0)
        self.title("EpGIS")
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        page_name = Creer_projet.__name__
        frame = Creer_projet(parent=container, controller= self)
        #frame.config(bg="#EDF1FC")
        frame.config(bg="#F7F9F9")
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky= "nsew")
        self.show_frame("Creer_projet")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Creer_projet(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        quit_button = Button(self, text="X", relief='flat', font=("Arial"), bg="#F7F9F9", activebackground="#F7F9F9",command=self.quiter)
        quit_button.place(x=760)

        lbFrm = LabelFrame(self, text="Créer un nouveau Marché", font=("Times New Roman", 18),  bg="#F7F9F9", width=770, height=480)
        lbFrm.place(x=10, y=10)

        marche = Label(lbFrm, text="Marché", font=("Times New Roman", 13), bg="#F7F9F9")
        marche.place(x=76, y=20)
        self.marche_entr = Entry(lbFrm, width=53, relief='flat', font=("Times New Roman", 11))
        self.marche_entr.place(x=210, y=20)

        sectr = Label(lbFrm, text="Secteur", font=("Helvetica", 13), bg="#F7F9F9")
        sectr.place(x=75, y=60)
        self.secteur_entr = Entry(lbFrm, width=53, relief='flat', font=("Times New Roman", 11))
        self.secteur_entr.place(x=210, y=60)

        cercle = Label(lbFrm, text="Cercle", font=("Helvetica", 13), bg="#F7F9F9")
        cercle.place(x=76, y=100)
        self.cercle_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
        self.cercle_entr.place(x=210, y=100)

        cercle_ar = tk.Label(lbFrm, text="الدائرة", font=("Times New Roman", 13), bg="#F7F9F9")
        cercle_ar.place(x=664, y=100)
        self.cercleAr_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
        self.cercleAr_entr.place(x=400, y=100)

        province = tk.Label(lbFrm, text="Province", font=("Times New Roman", 13), bg="#F7F9F9")
        province.place(x=74, y=140)
        self.province_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
        self.province_entr.place(x=210, y=140)

        province_ar = tk.Label(lbFrm, text="الاقليم", font=("Times New Roman", 13), bg="#F7F9F9")
        province_ar.place(x=666, y=140)
        self.provinceAR_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
        self.provinceAR_entr.place(x=400, y=140)

        commune = tk.Label(lbFrm, text="Commune", font=("Times New Roman", 13), bg="#F7F9F9")
        commune.place(x=75, y=180)
        self.commune_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
        self.commune_entr.place(x=210, y=180)

        commune = tk.Label(lbFrm, text="الجماعة", font=("Times New Roman", 13), bg="#F7F9F9")
        commune.place(x=665, y=180)
        self.communeAr_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
        self.communeAr_entr.place(x=400, y=180)

        consr_fonc = Label(lbFrm, text="Conservation foncière", font=("Times New Roman", 13), bg="#F7F9F9")
        consr_fonc.place(x=25, y=220)
        self.consFonc_entr = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
        self.consFonc_entr.place(x=210, y=220)

        consr_fonc = Label(lbFrm, text="المحافظة العقارية", font=("Times New Roman", 13), bg="#F7F9F9")
        consr_fonc.place(x=640, y=220)
        self.consFonc_entr_Ar = Entry(lbFrm, width=26, relief='flat', font=("Times New Roman", 11))
        self.consFonc_entr_Ar.place(x=400, y=220)

        geom = tk.Label(lbFrm, text="Géomètre", font=("Times New Roman", 13), bg="#F7F9F9")
        geom.place(x=72, y=260)
        self.geom_entr = Entry(lbFrm, width=53, relief='flat', font=("Times New Roman", 11))
        self.geom_entr.place(x=210, y=260)

        bul_off = tk.Label(lbFrm, text="Bulltin oficiel", font=("Times New Roman", 13), bg="#F7F9F9")
        bul_off.place(x=56, y=300)
        self.bulOff_entr = Entry(lbFrm, width=53, relief='flat', font=("Times New Roman", 11))
        self.bulOff_entr.place(x=210, y=300)

        date = tk.Label(lbFrm, text="Date", font=("Times New Roman", 13), bg="#F7F9F9")
        date.place(x=85, y=340)
        self.date_entr = Entry(lbFrm, width=53, relief='flat', font=("Times New Roman", 11))
        self.date_entr.place(x=210, y=340)

        create_btn = Button(lbFrm, text="Créer", width=8, relief='flat', font=("Times New Roman", 12), fg="#FFFFFF", bg="#379BF3", command=self.creat)
        create_btn.place(x=360, y=400)

    def creat(self):
        if(self.marche_entr.get()):
            marche = Marche_BE.Marche()
            m = marche.create_projct(self.date_entr.get(), self.marche_entr.get(), self.secteur_entr.get(), self.cercle_entr.get(), self.cercleAr_entr.get(), self.province_entr.get(), self.provinceAR_entr.get() ,self.commune_entr.get(), self.communeAr_entr.get(), self.consFonc_entr.get(),  self.consFonc_entr_Ar.get(), self.geom_entr.get(), self.bulOff_entr.get(), self.date_entr.get())
            self.open()
        else:
            msg = messagebox.showerror("Ouvrir le Marché", "Veuillez entrer le nom du marche")


    def open(self):
        result = messagebox.askquestion("Ouvrir le Marché", "Le projet a été créé avec succès \n Voulez-vous l'ouvrir maintenant?")
        if result == 'yes':
            self.controller.destroy()
            p = MainAdmin.MainAdmin()
        else:
            self.controller.destroy()
    def quiter(self):
        self.controller.destroy()


#app = Creatproject()
#app.mainloop()