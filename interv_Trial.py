import tkinter
import os

root = tkinter.Tk()
canvas = tkinter.Canvas(root)
canvas.grid(row = 0, column = 0)
project_directory = os.path.abspath(os.curdir)

datF = project_directory +"/icons/map-location.png"
photo = tkinter.PhotoImage(file = datF)
canvas.create_image(0, 0, image=photo)
root.mainloop()
