from tkinter import ttk
from tkinter.messagebox import *
from tkinter import *
import tkinter as tk

class OpenProject(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("600x180+380+180")
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        container = tk.Frame(self)
        container.config(bg="red")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        page_name = Open_project.__name__
        frame = Open_project(parent=container, controller= self)
        frame.config(bg="#F2F3F5")
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky= "nsew")
        self.show_frame("Open_project")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Open_project(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        quit_button = tk.Button(self, text="X", relief='flat', font=("Helvetica", 14), bg="#F2F3F5", command=self.quiter)
        quit_button.place(x=570)

        label = tk.Label(controller, text="Ouvrir un marché", font=("Helvetica", 18), fg="#000000", bg="#F2F3F5")
        label.place(x=200, y=30)

        label = tk.Label(self, text="Marché", font=("Helvetica", 12), fg="#61C2DC", bg="#F2F3F5")
        label.place(x=50, y=100)

        '''f1 = tk.Frame(self, bg='#E8B24D', relief='flat', bd=1, width=55)
        f1.place(x=150, y=40)'''
        '''marche = Marche()
        self.marche_var = StringVar()
        self.marche_box = ttk.Combobox(self, textvariable=self.marche_var, width=55)
        self.marche_box.place(x=130, y=100)
        self.marche_box['values'] = marche.list_project()'''

        '''f5 = Frame(self, bg='red', relief='flat', bd=1)
        f5.place(x=500, y=100)'''
        btn1 = tk.Button(self, text="Ouvrir ", font=("Helvetica", 10, 'bold'), height=1, fg="#000000", bg="#E98712",relief='flat', activebackground="#FFFFFF", activeforeground="#61C2DC").place(x=500, y=95)


    '''def projt(self):
        march = Marche()
        opn = march.open_project(self.marche_var.get())
        if opn == True:
            self.controller.destroy()
            p = MainUser()
        else:
            showinfo("suppression", "Aucun marché trouvé")'''


    def quiter(self):
        self.controller.destroy()

if __name__ == "__main__":
    app = OpenProject()
    app.mainloop()


'''label = tk.Label(self.frame1, text="Zone", font=("Helvetica", 12), fg="#61C2DC", bg="#FFFFFF")
        label.grid(row=2, column=0, pady=5)
        f3 = tk.Frame(self.frame1, bg='#E8B24D', relief='flat', bd=1,  width=55)
        f3.grid(row=2, column=1)
        self.entr_zone = tk.Entry(f3, width=55, relief='flat')
        self.entr_zone.grid(column=2, row=1)

        label = tk.Label(self.frame1, text="Sous-zone", font=("Helvetica", 12), fg="#61C2DC", bg="#FFFFFF")
        label.grid(row=3, column=0)
        f4 = tk.Frame(self.frame1, bg='#E8B24D', relief='flat', bd=1, width=52)
        f4.grid(row=3, column=1, pady=5)
        self.cbox = ttk.Combobox(f4, values=["Sous-zone-01", 2, 3, 3, 4, 5, 6, 7, 8, 9, 10], state='readonly', width=52)
        self.cbox.grid(column=3, row=1)

        label = tk.Label(self.frame1, text="Douar", font=("Helvetica", 12), fg="#61C2DC", bg="#FFFFFF")
        label.grid(row=4, column=0)
        f2 = tk.Frame(self.frame1, bg='#E8B24D', relief='flat', bd=1, width=55)
        f2.grid(row=4, column=1, pady=5)
        self.entr_douar = tk.Entry(f2, width=55, relief='flat')
        self.entr_douar.grid(column=4, row=1)'''