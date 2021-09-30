from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from tkcalendar import Calendar, DateEntry
from UserAPP import Parcelle_BE
from UserAPP import Personnes_BE
from UserAPP import Interval_BE
from AdminAPP import Point_BE
from AdminAPP import Brigades_BE
from UserAPP import Autocompletecombox
from tkinter import messagebox

class Intervalle(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Intervalles")
        self.geometry("534x339+400+120")
        self.resizable(0, 0)
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\IFE_GIS\icons\iconlogo.ico')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.polyg = Parcelle_BE.Parcelle()
        self.prs = Personnes_BE.Personnes()
        self.pnt = Point_BE.Point_BE()
        self.interv = Interval_BE.Intervalle()
        self.brigad = Brigades_BE.Brigades()
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

        self.tabControl = ttk.Notebook(self, height=298, width=522)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="Parcelles")

        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="Personnes")

        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text="Points")
        self.tabControl.place(x=4, y=5)
        self.notTab1()
        self.notTab2()
        self.notTab3()

                                    # ----------------------------------Parcelles ------------------------------------ #
    def notTab1(self):
        lastId = self.polyg.lastPolyInfo()
        inter = self.interv.polygInterv(str(lastId[0][3]))
        labelFrame = LabelFrame(self.tab1, text="Intervalle des parcelles", font=("Helvetica", 13), bg="#E3F3F3")
        labelFrame.place(x=15, y=10, width=490, height=270)

        idP = Label(labelFrame, text="id_dernière_parcelle", font=("Helvetica", 12), bg="#E3F3F3")
        idP.place(x=23, y=10)
        self.idValue = Label(labelFrame, text=lastId[0][0], font=("Helvetica", 12), bg="#F7F9F9", width=6)
        self.idValue.place(x=196, y=10)

        interv = Label(labelFrame, text="intervalle actuel", font=("Helvetica", 12), bg="#E3F3F3")
        interv.place(x=45, y=50)

        de = Label(labelFrame, text="De:", font=("Helvetica", 12), bg="#E3F3F3")
        de.place(x=195, y=50)
        self.deValue = Label(labelFrame, text=inter[0][0], font=("Helvetica", 12), bg="#F7F9F9", width=6)
        self.deValue.place(x=235, y=50)

        a = Label(labelFrame, text="A:", font=("Helvetica", 12), bg="#E3F3F3")
        a.place(x=315, y=50)
        self.aValue = Label(labelFrame, text=inter[0][1], font=("Helvetica", 12), bg="#F7F9F9", width=6)
        self.aValue.place(x=350, y=50)

        idBrigd = Label(labelFrame, text="id_brigade", font=("Helvetica", 12), bg="#E3F3F3")
        idBrigd.place(x=57, y=90)
        self.idEnt = Entry(labelFrame, width=22, font=("Helvetica", 12))
        self.idEnt.place(x=195, y=90)

        modifier = Button(labelFrame, text="Modifier", font=("Helvetica", 13), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, command=self.update)
        modifier.place(x=215, y=200)

    def update(self):
        intervPolyg = Interval_BE.Intervalle()
        #intervPolyg.changeInterv_Polyg(self.idEnt.get())
# ----- mise a jour
        inter = self.interv.polygInterv(self.idEnt.get())
        self.deValue.config(text="")
        self.aValue.config(text="")
        self.deValue.config(text=inter[0][0])
        self.aValue.config(text=inter[0][1])
        print(inter[0][0])
        print(inter[0][1])

                            # ----------------------------------TAB2 // Personnes ------------------------------------ #
    def notTab2(self):

        labelFrame = LabelFrame(self.tab2, text="Intervalle de personnes", font=("Helvetica", 13), bg="#E3F3F3")
        labelFrame.place(x=15, y=10, width=490, height=270)

        idP = Label(labelFrame, text="id_dernière_personne", font=("Helvetica", 12), bg="#E3F3F3")
        idP.place(x=18, y=10)
        self.idValue = Label(labelFrame, text='2000', font=("Helvetica", 12), bg="#F7F9F9", width=6)
        self.idValue.place(x=196, y=10)

        interv = Label(labelFrame, text="intervalle actuel", font=("Helvetica", 12), bg="#E3F3F3")
        interv.place(x=40, y=50)

        de = Label(labelFrame, text="De:", font=("Helvetica", 12), bg="#E3F3F3")
        de.place(x=195, y=50)
        self.deValue = Label(labelFrame, text='10', font=("Helvetica", 12), bg="#F7F9F9", width=6)
        self.deValue.place(x=235, y=50)

        a = Label(labelFrame, text="A:", font=("Helvetica", 12), bg="#E3F3F3")
        a.place(x=315, y=50)
        self.aValue = Label(labelFrame, text='2000', font=("Helvetica", 12), bg="#F7F9F9", width=6)
        self.aValue.place(x=350, y=50)

        consistance = Label(labelFrame, text="id_brigade", font=("Helvetica", 12), bg="#E3F3F3")
        consistance.place(x=55, y=90)
        self.consComb = Entry(labelFrame, width=22,font=("Helvetica", 12))
        self.consComb.place(x=195, y=90)


        modifier = Button(labelFrame, text="Modifier", font=("Helvetica", 13), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT, command=self.intervPoint)
        modifier.place(x=215, y=200)

    def intervPoint(self):
        print('oui')
        msgbox = messagebox.showinfo("Parcelle", "Modification effectuée avec succès")



                                        # ----------------------------------POINTS ------------------------------------ #
    def notTab3(self):
        labelFrame = LabelFrame(self.tab3, text="Intervalle des points", font=("Helvetica", 13), bg="#E3F3F3")
        labelFrame.place(x=15, y=10, width=490, height=270)

        idP = Label(labelFrame, text="id_dernière_point", font=("Helvetica", 12), bg="#E3F3F3")
        idP.place(x=23, y=10)
        self.idValue = Label(labelFrame, text='2000', font=("Helvetica", 12), bg="#F7F9F9", width=6)
        self.idValue.place(x=196, y=10)

        interv = Label(labelFrame, text="intervalle actuel", font=("Helvetica", 12), bg="#E3F3F3")
        interv.place(x=40, y=50)

        de = Label(labelFrame, text="De:", font=("Helvetica", 12), bg="#E3F3F3")
        de.place(x=195, y=50)
        self.deValue = Label(labelFrame, text='10', font=("Helvetica", 12), bg="#F7F9F9", width=6)
        self.deValue.place(x=235, y=50)

        a = Label(labelFrame, text="A:", font=("Helvetica", 12), bg="#E3F3F3")
        a.place(x=315, y=50)
        self.aValue = Label(labelFrame, text='2000', font=("Helvetica", 12), bg="#F7F9F9", width=6)
        self.aValue.place(x=350, y=50)

        consistance = Label(labelFrame, text="id_brigade", font=("Helvetica", 12), bg="#E3F3F3")
        consistance.place(x=55, y=90)

        self.consComb = Entry(labelFrame, width=22,font=("Helvetica", 12))
        self.consComb.place(x=195, y=90)

        modifier = Button(labelFrame, text="Modifier", font=("Helvetica", 13), bg="#4EB1FA", fg="#FFFFFF", relief=FLAT,command=self.intervPerson)
        modifier.place(x=215, y=200)

    def intervPerson(self):
        msgbox = messagebox.showinfo("Parcelle", "Modification effectuée avec succès")

#app = Intervalle()
#app.mainloop()