import datetime
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class Douar:

    def combboxcDr(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select libelle_fr from douar ;")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(''.join(a))
        return value

# **********************************************************selectionner les noms de colonnes
    def columnName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'douar'")
        col_name = cur.fetchall()
        return col_name

# **********************************************************selectionner la liste consistance
    def select(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM douar;")
        value = cur.fetchall()
        return value

# **********************************************selectionner les noms de colonnes pour modifier ou supprimer une ligne sur le Treeview
    def select_colName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'douar' and COLUMN_NAME <> 'id_douar' and COLUMN_NAME <> 'id_souszone' and COLUMN_NAME <> 'geom' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        return col_name

# ************************************************************ select les valeurs d'une ligne selectionnee sur le Treeview
    def select_colValue(self, idSelected):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT libelle_fr,libelle_ar FROM douar where id_douar=" + idSelected + ";")
        value = cur.fetchall()
        tabValue = []
        for v in value:
            tabValue.append(v)
        return tabValue

# ***************************************************************** Modifier une ligne de le Treeview
    def update_colValue(self, tab_update, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'douar' and COLUMN_NAME <> 'id_douar' and COLUMN_NAME <> 'id_souszone' and COLUMN_NAME <> 'geom' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        for i in range(len(col_name)):
            cur.execute("UPDATE douar SET " + ''.join(col_name[i]) + "='" + tab_update[i] + "', date_modification = '" + str(datetime.datetime.now()) + "' where id_douar = '" + id + "';")
            conn.commit()

# ********************************************************************* supprimer une ligne de TREEVIEW*****
    def verifyDr(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM douar WHERE id_douar ='" + id + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False

    def deleteDr(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM douar WHERE id_douar ='" + id + "';")
        conn.commit()

# **********************************************************************************Ajouter une Nouvelle Consistance
    def insert_dr(self, sz, libFr, libAr):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO douar(id_douar, id_sousZone, libelle_fr, libelle_ar, date_creation) VALUES (DEFAULT , "+sz+", '" + libFr + "', '" + libAr + "', '"+str(datetime.datetime.now())+"')")
        conn.commit()


                                                    # ***************** LastPolyg // DOUAR **************
    def lastPolyDr(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT douar.libelle_fr FROM douar INNER JOIN parcelles ON ST_Intersects(parcelles.geom, douar.geom) and not ST_Contains(parcelles.geom, douar.geom) WHERE parcelles.id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles)")
        reslt = cur.fetchall()
        return reslt


                                                    # ***** SELECT DOUAR DES POINTS DEBUT ET FIN DE LA PARCELLE RIVRAIN// DOUAR **************
    def drRiv(self, idPoint):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT douar.libelle_fr FROM douar INNER JOIN points ON ST_Intersects(points.geom, douar.geom) and not ST_Contains(points.geom, douar.geom) WHERE points.id_point =  "+idPoint+"")
        reslt = cur.fetchone()
        return reslt


                                                    # ***************** ModifyPolyg // DOUAR **************
    def selectDr(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT douar.libelle_fr, douar.libelle_ar FROM douar INNER JOIN parcelles ON ST_Intersects(parcelles.geom, douar.geom) and not ST_Contains(parcelles.geom, douar.geom) WHERE parcelles.id_parcelle = "+idP+" ")
        reslt = cur.fetchall()
        tabValue = []
        for v in reslt:
            tabValue.append(v)
        return tabValue



                                                    # ***************** SELECT ID_DOUAR DE LA PARCELLE RIVRAIN **************
    def drRivPolyg(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT douar.id_douar FROM douar INNER JOIN parcelles ON ST_Intersects(parcelles.geom, douar.geom) and not ST_Contains(parcelles.geom, douar.geom) WHERE parcelles.id_parcelle = "+idP+" ")
        reslt = cur.fetchone()
        return reslt


                                                    # ***************** SELECT DOUAR // XML // EtatPARCELLAIRE // ZN2 **************
    def xmlDr(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT douar.id_douar, douar.libelle_fr, douar.libelle_ar FROM douar INNER JOIN parcelles ON ST_Intersects(parcelles.geom, douar.geom) and not ST_Contains(parcelles.geom, douar.geom) where parcelles.id_parcelle = "+idP+"")
        dr = cur.fetchall()
        return dr

