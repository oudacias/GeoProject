import datetime
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class SousZ:

    def combboxSZ(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select libelle_fr from sous_zone ;")
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
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'sous_zone'")
        col_name = cur.fetchall()
        return col_name

# **********************************************************selectionner la liste consistance
    def select(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sous_zone  ORDER BY id_souszone ASC;")
        value = cur.fetchall()
        return value

# **********************************************selectionner les noms de colonnes pour modifier ou supprimer une ligne sur le Treeview
    def select_colName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'sous_zone' and COLUMN_NAME <> 'id_souszone' and COLUMN_NAME <> 'id_zone' and COLUMN_NAME <> 'geom' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        return col_name

# ************************************************************select les valeurs d'une ligne selectionnee sur le Treeview
    def select_colValue(self, idSelected):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT libelle_fr FROM sous_zone where id_sousZone=" + idSelected + ";")
        value = cur.fetchall()
        tabValue = []
        for v in value:
            tabValue.append(v)
        return tabValue

# *****************************************************************Modifier une ligne de le Treeview
    def update_colValue(self, tab_update, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'sous_zone'  and COLUMN_NAME <> 'id_souszone' and COLUMN_NAME <> 'id_zone' and COLUMN_NAME <> 'geom' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        for i in range(len(col_name)):
            cur.execute("UPDATE sous_zone SET " + ''.join(col_name[i]) + "='" + tab_update[i] + "', date_modification = '" + str(datetime.datetime.now()) + "' where id_sousZone = '" + id + "';")
            conn.commit()

# ********************************************************************* supprimer une ligne de TREEVIEW*****
    def verifySZ(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM sous_zone WHERE id_sousZone ='" + id + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False

    def deleteConsistance(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM sous_zone WHERE id_sousZone ='" + id + "';")
        conn.commit()

# **********************************************************************************Ajouter une Nouvelle SousZone
    def insert_sz(self, zn, libAr):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO sous_zone(id_sousZone, id_Zone, libelle_fr, date_creation) VALUES (DEFAULT ," + zn + ", '" + libAr + "', '" + str(datetime.datetime.now()) + "')")
        conn.commit()

    def lastPolySZ(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT sous_zone.libelle_fr FROM sous_zone INNER JOIN douar ON ST_Intersects(sous_zone.geom, douar.geom) "
                    "INNER JOIN parcelles  ON ST_Intersects(parcelles.geom, douar.geom)"
                    " WHERE parcelles.id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles) ")
        reslt = cur.fetchall()
        return reslt
        #  and not ST_Contains(parcelles.geom, douar.geom)

# ******************************************************************************* SELECT SOUS_ZONE
    def selectSZ(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT sous_zone.libelle_fr, sous_zone.id_souszone FROM sous_zone INNER JOIN douar ON ST_Intersects(sous_zone.geom, douar.geom) and not ST_Contains(sous_zone.geom, douar.geom) "
                    "INNER JOIN parcelles  ON ST_Intersects(parcelles.geom, douar.geom) and not ST_Contains(parcelles.geom, douar.geom)"
                    " WHERE parcelles.id_parcelle = "+idP+" ")
        reslt = cur.fetchall()
        return reslt

