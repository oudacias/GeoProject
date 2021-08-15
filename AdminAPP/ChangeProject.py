import tkinter as tk

from Log_in import Login


class Change_Project(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EpGis")
        self.geometry("485x275+400+220")
        #self.iconbitmap(r'C:\Users\LAILA\PycharmProjects\EpGis\icons\iconlogo.ico')

        container = tk.Frame(self, highlightthickness=0)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        page_name = Login.LogIn.__name__
        frame = Login.LogIn(parent=container, controller=self)
        self.frames[page_name] = frame
        frame.config(bg="#F7F9F9")
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = Change_Project()
    app.mainloop()

