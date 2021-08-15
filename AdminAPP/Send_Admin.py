from tkinter import *
from UserAPP import Marche_BE
from UserAPP import Autocompletecombox
from AdminAPP import Machines_BE
from UserAPP import SynchClient_JR
from UserAPP import SynchClient_Gnr
from tkinter.messagebox import *

class SendDB(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Envoie")
        self.geometry("410x230+450+200")
        self.resizable(0, 0)
        self.config(bg="#F7F9F9")
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.mrch = Marche_BE.Marche()
        self.machin = Machines_BE.NewMachin()


# SELECT Machine
        lFrm = LabelFrame(self, text="L'envoie des données", font=("Helvetica", 13), bg="#F7F9F9")
        lFrm.place(x=10, y=8, width=390, height=210)

        mrche = self.mrch.mrchName()
        prs = Label(lFrm, text="Veuillez sélectionner :", font=("Helvetica", 13), bg="#F7F9F9")
        prs.place(x=120, y=18)
    #select machine
        machin = Label(lFrm, text="Nom du machine", font=("Helvetica", 12), bg="#F7F9F9")
        machin.place(x=40, y=60)
        machinVar = StringVar()
        mchine = self.machin.combboxcMachin()
        self.machinBox = Autocompletecombox.Autocompletecombox(lFrm, textvariable=machinVar, font=("Times New Roman", 12))
        self.machinBox.set_completion_list(mchine)
        self.machinBox.place(x=190, y=60)
    # select type de synchronisation
        tpSynch = Label(lFrm, text="Type de synchronisation", font=("Helvetica", 12), bg="#F7F9F9")
        tpSynch.place(x=7, y=100)
        tpSynchVal = ['du jour', 'générale']
        tpSynchVar = StringVar()
        self.tpSynchBox = Autocompletecombox.Autocompletecombox(lFrm, textvariable=tpSynchVar, font=("Times New Roman", 12))
        self.tpSynchBox.set_completion_list(tpSynchVal)
        self.tpSynchBox.place(x=190, y=100)

        opp_btn = Button(lFrm, text="Envoyer", font=("Times New Roman", 11), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, command=self.sendData)
        opp_btn.place(x=160, y=145)

    def sendData(self):
        if self.machinBox.get()!= '' and self.tpSynchBox.get()!= '':
            tp = self.tpSynchBox.get()
            if tp == 'du jour':
                synchJr = SynchClient_JR.SynchClientJr()
                synchJr.selectIp(self.machinBox.get())
            elif tp == 'générale':
                synchGnr = SynchClient_Gnr.SynchClientGnr()
                synchGnr.sockets(self.machinBox.get())
        else:
            showerror("Envoie", "Veuillez sélectionner Une machine et Type de synchronisation")

#app = SendDB()
#app.mainloop()