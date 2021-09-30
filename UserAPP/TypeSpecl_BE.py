import datetime
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH):
    from Connection.ConnectionFile import Connection


class TypeSpecul:

    def combxTpSpecl(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select libelle_fr from type_speculation ;")
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
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'type_speculation'")
        col_name = cur.fetchall()
        return col_name

        # **********************************************************selectionner la liste des types de speculation

    def select(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM type_speculation order by id_type_speculation ASC ;")
        value = cur.fetchall()
        return value

        # *************************************************selectionner les noms de colonnes pour modifier ou supprimer une ligne sur le Treeview

    def select_colName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'type_speculation' and COLUMN_NAME <> 'id_type_speculation' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        return col_name

        # ************************************************************select les valeurs d'une ligne selectionnee sur le Treeview

    def select_colValue(self, idSelected):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT libelle_fr,libelle_ar,abreviation FROM type_speculation where id_type_speculation=" + idSelected + ";")
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
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'type_speculation' and COLUMN_NAME <> 'id_type_speculation' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        for i in range(len(col_name)):
            cur.execute("UPDATE type_speculation SET " + ''.join(col_name[i]) + "='" + tab_update[
                i] + "', date_modification = '" + str(
                datetime.datetime.now()) + "' where id_type_speculation = '" + id + "';")
            conn.commit()

            # ********************************************************************* supprimer une ligne de TREEVIEW*****

    def verifyTypeSpeculation(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM type_speculation WHERE id_type_speculation ='" + id + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False

    def deleteTypeSpeculation(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM type_speculation WHERE id_type_speculation ='" + id + "';")
        conn.commit()

        # **********************************************************************************Ajouter un Nouveau Type de Speculation

    def insertTypeSpeculation(self, libelle_fr, libelle_ar, abrev):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO type_speculation(id_type_speculation ,libelle_fr, libelle_ar, abreviation, date_creation) VALUES (DEFAULT ,'" + libelle_fr + "', '" + libelle_ar + "', '" + abrev + "', '" + str(
                datetime.datetime.now()) + "')")
        conn.commit()


                                                    # ***************** ResearchPolyg // Type de Spéculation **************
    def researPoly_Spec(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT  sp.libelle_fr, sp.id_type_speculation FROM type_speculation as sp inner join parcelles as pr on (sp.id_type_speculation = pr.id_type_speculation) and pr.id_parcelle=" + idP + ";")
        reslt = cur.fetchall()
        for a in reslt:
            return (a)


                                                    # ***************** SELECT TYPE_SPECULATION // XML **************
    def spec_xml(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT  sp.id_type_speculation, sp.libelle_fr , sp.abreviation, sp.libelle_ar FROM type_speculation as sp inner join parcelles as pr on (sp.id_type_speculation = pr.id_type_speculation) and pr.id_parcelle=" + idP + ";")
        reslt = cur.fetchall()
        return reslt

