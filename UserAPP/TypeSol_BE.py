import datetime
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection


class TypeSol:

    def combxTpsol(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select libelle_fr from type_sol ;")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(''.join(a))
        return value

    # ***********************************************************************selectionner les noms de colonnes
    def columnName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'type_sol'")
        col_name = cur.fetchall()
        return col_name

        # **********************************************************selectionner la liste types de sol

    def select(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM type_sol order by id_type_sol ASC;")
        value = cur.fetchall()
        return value

        # *****************************************************selectionner les noms de colonnes pour modifier ou supprimer une ligne sur le Treeview

    def select_colName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'type_sol' and COLUMN_NAME <> 'id_type_sol' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        return col_name

        # ************************************************************select les valeurs d'une ligne selectionnee sur le Treeview

    def select_colValue(self, idSelected):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT libelle_fr,libelle_ar,abreviation FROM type_sol where id_type_sol=" + idSelected + ";")
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
        cur.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'type_sol' and COLUMN_NAME <> 'id_type_sol' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        for i in range(len(col_name)):
            cur.execute("UPDATE type_sol SET " + ''.join(col_name[i]) + "='" + tab_update[
                i] + "', date_modification = '" + str(
                datetime.datetime.now()) + "' where id_type_sol = '" + id + "';")
            conn.commit()

            # ********************************************************************* supprimer une ligne de TREEVIEW*****

    def verifyTypeSol(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM type_sol WHERE id_type_sol ='" + id + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False

    def deleteTypeSol(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM type_sol WHERE id_type_sol ='" + id + "';")
        conn.commit()

        # **********************************************************************************Ajouter un Nouveau type de Sol

    def insert_typeSol(self, libelle_fr, libelle_ar, abrev):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO type_sol(id_type_sol ,libelle_fr, libelle_ar, abreviation, date_creation) VALUES (DEFAULT ,'" + libelle_fr + "', '" + libelle_ar + "', '" + abrev + "', '" + str(datetime.datetime.now()) + "')")
        conn.commit()

                                                    # ***************** ResearchPolyg // DOUAR **************
    def researPoly_Sol(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT  tp.libelle_fr,tp.id_type_sol FROM type_sol as tp inner join parcelles as pr on (tp.id_type_sol = pr.id_type_sol) and pr.id_parcelle=" + idP + ";")
        reslt = cur.fetchall()
        for a in reslt:
            return (a)

                                                    # ***************** SELECT TYPE_SOL // XML // ZN2 **************
    def sol_xml(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT  tp.id_type_sol, tp.libelle_fr, tp.abreviation, tp.libelle_ar FROM type_sol as tp inner join parcelles as pr on (tp.id_type_sol = pr.id_type_sol) and pr.id_parcelle=" + idP + ";")
        reslt = cur.fetchall()
        return reslt