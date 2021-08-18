import datetime
import os

PATH = os.path.abspath(os.curdir) +'/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection


class Zone:
    def selectZn(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT zone.libelle FROM zone"
                    " INNER JOIN sous_zone ON ST_Intersects(sous_zone.geom, zone.geom) and not ST_Contains(sous_zone.geom, zone.geom)"
                    " INNER JOIN douar ON ST_Intersects(douar.geom, sous_zone.geom) and not ST_Contains(douar.geom, sous_zone.geom) "
                    " INNER JOIN parcelles  ON ST_Intersects(parcelles.geom, douar.geom) and not ST_Contains(parcelles.geom, douar.geom)"
                    " WHERE parcelles.id_parcelle = 2 ")
        reslt = cur.fetchall()
        return reslt


                                       # ********************* LastPolyg // ZONE ***********************
    def lastPolyZn(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT zone.libelle FROM zone INNER JOIN sous_zone ON ST_Intersects(sous_zone.geom, zone.geom)"
                    "INNER JOIN douar ON ST_Intersects(douar.geom, sous_zone.geom)"
                    "INNER JOIN parcelles  ON ST_Intersects(parcelles.geom, douar.geom)"
                    "WHERE parcelles.id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles) ")
        reslt = cur.fetchone()
        return reslt
