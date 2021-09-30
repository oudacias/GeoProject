from tkinter import *
from UserAPP import Marche_BE
from AdminAPP import Machines_BE
from Synchronisation import FromServ_Client
from Synchronisation import Gnr_Client

class ReceiveDB(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Réception")
        self.geometry("360x180+450+200")
        self.resizable(0, 0)
        self.config(bg="#F7F9F9")
        self.mrch = Marche_BE.Marche()
        self.machin = Machines_BE.NewMachin()

        # SELECT Machine
        lFrm = LabelFrame(self, text="Réception des données", font=("Helvetica", 13), bg="#F7F9F9")
        lFrm.place(x=10, y=8, width=340, height=160)

        mrche = self.mrch.mrchName()
        txt = Label(lFrm, text="recevoir les données du jour ou génerale ", font=("Helvetica", 13), bg="#F7F9F9")
        txt.place(x=15, y=20)

        opp_btn = Button(lFrm, text="Du jour", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT,command=FromServ_Client.SynchServerJr.receiveData(self))
        opp_btn.place(x=100, y=80)

        opp_btn = Button(lFrm, text="Génerale", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT,command=Gnr_Client.SynchServerGnr.receiveData(self))
        opp_btn.place(x=180, y=80)


#app = ReceiveDB()
#app.mainloop()
