import datetime
import os

import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class Rivrains:

    def columnName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'rivrains'")
        col_name = cur.fetchall()
        return col_name

                                                      # --------------------- Polyg Selected // OPPOSANT -----------------------
    def researRiv(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM rivrains where id_parcelle = "+idP+";")
        reslt = cur.fetchall()
        return reslt

                                                                     # ******************** SELECT RIVRAINS// XML***********************
    def rivXml(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select rv.id_parcelle,rv.id_parcelle_rivrain,rv.direction,rv.point_debut,rv.point_fin from rivrains as rv inner join parcelles as pr on (rv.id_parcelle = pr.id_parcelle) where pr.id_parcelle= " + idP + ";")
        rivrain = cur.fetchall()
        return rivrain

