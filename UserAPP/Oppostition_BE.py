import datetime
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH):
    from Connection.ConnectionFile import Connection


class TypeOppos:

    def combxOpposition(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select distinct libelle_fr from type_opposition ;")
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
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'type_opposition'")
        col_name = cur.fetchall()
        return col_name

        # **********************************************************selectionner la liste des types d'opposition

    def select(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM type_opposition order by id_type_opposition ASC ;")
        value = cur.fetchall()
        return value

        # *************************************************selectionner les noms de colonnes pour modifier ou supprimer une ligne sur le Treeview

    def select_colName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'type_opposition' and COLUMN_NAME <> 'id_type_opposition' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        return col_name

        # ************************************************************select les valeurs d'une ligne selectionnee sur le Treeview

    def select_colValue(self, idSelected):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT libelle_fr,libelle_ar FROM type_opposition where id_type_opposition=" + idSelected + ";")
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
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'type_opposition' and COLUMN_NAME <> 'id_type_opposition' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        for i in range(len(col_name)):
            cur.execute("UPDATE type_opposition SET " + ''.join(col_name[i]) + "='" + tab_update[
                i] + "', date_modification = '" + str(
                datetime.datetime.now()) + "' where id_type_opposition = '" + id + "';")
            conn.commit()

            # ********************************************************************* supprimer une ligne de TREEVIEW*****

    def verifyOppost(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM type_opposition WHERE id_type_opposition ='" + id + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False

    def deleteOppost(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM type_opposition WHERE id_type_opposition ='" + id + "';")
        conn.commit()

        # **********************************************************************************Ajouter un Nouveau Type de Speculation

    def insertOppost(self, libelle_fr, libelle_ar):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO type_opposition(id_type_opposition ,libelle_fr, libelle_ar, date_creation) VALUES (DEFAULT ,'" + libelle_fr + "', '" + libelle_ar + "', '" + str(datetime.datetime.now()) + "')")
        conn.commit()

    def combxTpOpp(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select libelle_fr from type_opposition;")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(a[0])
        return value


                        # *************************************************SELECT MOTIF OPPOSITION

    def motif_Opp(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select op.libelle_fr from type_opposition as op inner join cles as c on (op.id_type_opposition = c.id_type_opposition) where c.cle_polyg = '"+str(idP)+"' ")
        col_name = cur.fetchall()
        columns = []
        for col in col_name:
            columns.append(col[0])
        return columns
