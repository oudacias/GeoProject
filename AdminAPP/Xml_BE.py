import os
import sys
sys.path.append(".")


from Connection.ConnectionFile import Connection

class Xml_BE:

    def xmlPolygs(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select * from  parcelles;")
        values = cur.fetchall()
        return values

    def valPolyg(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select id_parcelle, parcelle_fr, parcelle_ar, id_douar from  parcelles;")
        polyg = cur.fetchall()
        return polyg






