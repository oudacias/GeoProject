import tkinter as tk

from Log_in import Login


class Change_Project(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EpGis")
        self.geometry("485x275+400+220")

        container = tk.Frame(self, highlightthickness=0)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login.ConnectDB, Login.LogIn, Login.Modifypass):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.config(bg="#F7F9F9")
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame("ConnectDB")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()




class ConnectDB(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class Modifypass(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = Change_Project()
    app.mainloop()
