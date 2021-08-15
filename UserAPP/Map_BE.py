import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import os
import matplotlib
import psycopg2
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class Map_BE:

    def plotPolyg(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT ST_AsGeoJSON(geom) :: json->'coordinates' AS coordinates FROM parcelles where ST_AsGeoJSON(geom) is not null;;")
        bornes = cur.fetchall()
        x1 = []
        y1 = []
        for b in bornes:
            for i in range(len(b[0][0])):
                x1.append(b[0][0][i][0])
                y1.append(b[0][0][i][1])
            shapes = [[x1, y1]]
            for shape in shapes:
                x, y = shape
                plt.plot(x, y, 'b')
            x1.clear()
            y1.clear()

    def selectPolyg(event):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT Find_SRID('public', 'parcelles', 'geom');")
        srid = cur.fetchone()
        cur.execute("SELECT ST_PointFromText('POINT(" + str(event.xdata) + " " + str(event.ydata) + ")', "+str(srid[0])+");")
        point = cur.fetchone()
        cur.execute("SELECT pa.id_parcelle FROM parcelles pa WHERE ST_contains(pa.geom, '" + str(point[0]) + "') order by id_parcelle;;")
        parcelle = cur.fetchone()
        return parcelle

    def detailMap(window, id_parcelle):
        fig = Figure(figsize=(5, 5))
        a = fig.add_subplot(111)

        conn = psycopg2.connect(user="postgres", password="1234", database="epgis1", host="localhost")
        cursor = conn.cursor()
        cursor.execute("SELECT ST_AsGeoJSON(geom) :: json->'coordinates' AS coordinates FROM parcelles where id_parcelle = " + str(id_parcelle) + ";")
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
