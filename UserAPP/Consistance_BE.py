import datetime
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH):
    from Connection.ConnectionFile import Connection


class Consistance:

    def combxConst(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select libelle_fr from consistance ;")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(a[0])
        return value



# **********************************************************selectionner les noms de colonnes
    def columnName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'consistance'")
        col_name = cur.fetchall()
        return col_name

# **********************************************************selectionner la liste consistance
    def selectConsist(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM consistance ORDER BY id_consistance ASC;")
        value = cur.fetchall()
        return value

# **********************************************selectionner les noms de colonnes pour modifier ou supprimer une ligne sur le Treeview
    def select_colName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'consistance' and COLUMN_NAME <> 'id_consistance' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        return col_name

# ************************************************************select les valeurs d'une ligne selectionnee sur le Treeview
    def select_colValue(self, idSelected):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT libelle_fr,libelle_ar,abreviation FROM consistance where id_consistance=" + idSelected + ";")
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
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'consistance' and COLUMN_NAME <> 'id_consistance' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        for i in range(len(col_name)):
            cur.execute("UPDATE consistance SET " + ''.join(col_name[i]) + "='" + tab_update[i] + "', date_modification = '" + str(datetime.datetime.now()) + "' where id_consistance = '" + id + "';")
            conn.commit()

# ********************************************************************* supprimer une ligne de TREEVIEW*****
    def verifyConsistance(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM consistance WHERE id_consistance ='" + id + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False

    def deleteConsistance(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM consistance WHERE id_consistance ='" + id + "';")
        conn.commit()

# **********************************************************************************Ajouter une Nouvelle Consistance
    def addNewConsis(self, libelle_fr, libelle_ar, abrev):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO consistance(id_consistance ,libelle_fr, libelle_ar, abreviation, date_creation) VALUES (DEFAULT ,'" + libelle_fr + "', '" + libelle_ar + "', '" + abrev + "', '" + str(datetime.datetime.now()) + "')")
        conn.commit()


                                                    # ***************** ResearchPolyg // Consistance **************
    def researPoly_Cons(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT  cs.libelle_fr FROM consistance as cs inner join parcelles as pr on (cs.id_consistance = pr.id_consistance) and pr.id_parcelle=" + idP + ";")
        reslt = cur.fetchall()
        for a in reslt:
            return (a)

                                                  # ***************** ResearchPolyg // Consistance **************
    def constVal(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT cs.id_consistance FROM consistance as cs inner join parcelles as pr on (cs.id_consistance = pr.id_consistance) and pr.id_parcelle=3;")
        reslt = cur.fetchall()
        for a in reslt:
            return (a)


                                                    # ***************** SELECT CONSISTANCE // XML // EtatPacellaire **************
    def Const_xml(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT cs.id_consistance,cs.libelle_fr,cs.abreviation,cs.libelle_ar FROM consistance as cs inner join parcelles as pr on (cs.id_consistance = pr.id_consistance) and pr.id_parcelle=" + idP + ";")
        reslt = cur.fetchall()
        return reslt

