import os
import datetime
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class Brigades:

                                                    # ********************* COLUMN NAMES*********************
    def columnName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'brigades'")
        col_name = cur.fetchall()
        return col_name


                                                    # ********************* VALUES *********************
    def select(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM brigades;")
        value = cur.fetchall()
        return value


                                                    # ********************* SELECTION QLQ NOMS DE COLONNES *********************
    def select_colName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'brigades' and COLUMN_NAME <> 'id_brigade' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        return col_name


                                                    # ********************* SELECTION QLQ VALUES *********************
    def select_colValue(self, idSelected):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT brigade_fr,brigade_ar FROM brigades where id_brigade="+idSelected+";")
        value = cur.fetchall()
        tabValue = []
        for v in value:
            tabValue.append(v)
        return tabValue


                                                    # ********************* MODIFIER Brigade*********************

    def update_colValue(self, tab_update, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'brigades' and COLUMN_NAME <> 'id_brigade' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()

        for i in range(len(col_name)):
            cur.execute("UPDATE brigades SET " + ''.join(col_name[i]) + "='" + tab_update[i] + "', date_modification = '"+str(datetime.datetime.now())+"' where id_brigade = '" + id + "';")
            conn.commit()



                                                    # ********************* Verify Brigade  *********************
    def verifyBrg(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM brigades WHERE id_brigade ='" + id + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False


                                                    # ********************* Delete brigade *********************
    def deleteBrg(self, idB):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM brigades WHERE id_brigade ='" + idB + "';")
        conn.commit()


                                                    # ********************* Nouvelle brigade *********************
    def insert(self, brig_fr, brig_ar):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO brigades (id_brigade, brigade_fr, brigade_ar, date_creation) VALUES (DEFAULT ,'"+brig_fr+"', '"+brig_ar+"', '"+str(datetime.datetime.now())+"')")
        conn.commit()


                                                    #******************** Last Brigade ***********************
    def selectLastBrig(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT brigade_fr FROM brigades where id_brigade = (SELECT MAX(id_brigade)FROM brigades);")
        reslt = cur.fetchone()
        return reslt


                                                    #******************** id Brigades ***********************
    def idsBrigades(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT id_brigade FROM brigades ORDER BY id_brigade ASC ;")
        reslt = cur.fetchall()
        tabValue = []
        for v in reslt:
            tabValue.append(v)
        return tabValue

