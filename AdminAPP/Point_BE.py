import datetime
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH):
    from Connection.ConnectionFile import Connection

class Point_BE:

                                                                       # ******************** SELECT NUM_POINT ***********************
    def numPt(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #idP = []
        cur.execute("SELECT pt.id_point, pt.X_def, pt.Y_def, pt.type_point, pt.num_point FROM points as pt INNER JOIN parcelles as pr  ON ST_Intersects(pr.geom, pt.geom)  and not ST_Contains(pr.geom, pt.geom) where pr.id_parcelle= "+idP+" ")
        #cur.execute("SELECT pt.num_point FROM points as pt INNER JOIN parcelles as pr  ON ST_Intersects(pr.geom, pt.geom)")
        numPnt = cur.fetchall()
        return numPnt

                                                                       # ******************** SELECT COORD X Y ***********************
    def coord_XY(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #cur.execute("SELECT pt.x_def,pt.y_def FROM points as pt INNER JOIN parcelles as pr  ON ST_Intersects(pr.geom, pt.geom) where pr.id_parcelle= "+idP+" ")
        cur.execute("SELECT pt.id_point, pt.x_def,pt.y_def FROM points as pt INNER JOIN parcelles as pr  ON ST_Intersects(pr.geom, pt.geom)  and not ST_Contains(pr.geom, pt.geom)  where pr.id_parcelle= "+idP+" ")
        coordxy = cur.fetchall()
        return coordxy

                                                                       # ******************** SELECT POINT DEBUT ET FIN ***********************
    def tpPoint(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT pt.type_point FROM points as pt INNER JOIN rivrains as rv  inner join parcelles as pr ON (pt.id_point = rv.point_debut) OR (pt.id_point = rv.point_fin) where pr.id_parcelle= "+idP+" ")
        numpnt = cur.fetchall()
        return numpnt

                                                                       # ******************** SELECT num_point pour les point Debut et Fin de rivrain ***********************
    def numPoint(self, idPoint):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT num_point, type_point, X_def, Y_def FROM points where id_point= "+idPoint+" ")
        numpnt = cur.fetchone()
        return numpnt
