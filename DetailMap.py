import matplotlib
import psycopg2
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

import sys
import os
sys.path.append(".")


from Connection.ConnectionFile import Connection

class DetailMap:
    def __init__(self,  window, id_parcelle):

        self.window = window
        fig = Figure(figsize=(5, 5))
        a = fig.add_subplot(111)

        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT ST_AsGeoJSON(geom) :: json->'coordinates' AS coordinates FROM parcelles where id_parcelle = " + str(id_parcelle) + ";")
        bornes = cur.fetchone()
        x1 = []
        y1 = []

        for i in range(len(bornes[0][0])):
            x1.append(bornes[0][0][i][0])
            y1.append(bornes[0][0][i][1])

        shapes = [[x1, y1]]
        for shape in shapes:
            x, y = shape
            a.plot(x, y, 'b')
        a.axis('off')

        frame = Frame(window, width=1366, height=714)
        frame1 = Frame(window, width=370, height=714)
        frame.pack()
        canvas = Canvas(window, width=714, height=714)
        canvas.pack_propagate(0)
        canvas.place(x=470, y=0)
        frame1.pack_propagate(0)
        frame1.place(x=0, y=0)

        canvas = FigureCanvasTkAgg(fig, master=frame1)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def detailMap(window, idP):

        fig = Figure(figsize=(5, 5))
        a = fig.add_subplot(111)

        conn = psycopg2.connect(user="postgres", password="1234", database="epgis1", host="localhost")
        cursor = conn.cursor()
        cursor.execute("SELECT ST_AsGeoJSON(geom) :: json->'coordinates' AS coordinates FROM parcelles where id_parcelle = "+idP+" ;")
        bornes = cursor.fetchone()
        x1 = []
        y1 = []

        for i in range(len(bornes[0][0])):
            x1.append(bornes[0][0][i][0])
            y1.append(bornes[0][0][i][1])

        shapes = [[x1, y1]]
        for shape in shapes:
            x, y = shape
            a.plot(x, y, 'b')
        a.axis('off')

        frame = Frame(window, width=1366, height=714, bg="#FFFFFF")
        frame.pack()
        frame1 = Frame(window, width=370, height=714, bg="#FFFFFF")
        frame1.pack_propagate(0)
        frame1.place(x=0, y=0)
        canvas = Canvas(window, width=714, height=714, bg="#FFFFFF")
        canvas.pack_propagate(0)
        canvas.place(x=470, y=0)


        canvas = FigureCanvasTkAgg(fig, master=frame1)
        canvas.get_tk_widget().pack()
        canvas.draw()


