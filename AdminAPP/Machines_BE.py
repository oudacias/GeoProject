import os
import datetime
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class NewMachin:

                                                                       # ******************** Les noms de colonnes // TREEVIEW***********************
    def addMachine(self, nom, ip, type):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO machines (id_machine, nom_machine, adresse_ip, port, type, date_creation) values (DEFAULT , '"+nom+"', '"+ip+"' , default, '"+type+"', '"+str(datetime.datetime.now())+"')")
        conn.commit()


                                                                        # ***************** selectionner les noms de colonnes
    def columnName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'machines'")
        col_name = cur.fetchall()
        return col_name


                                                    # ********************* VALUES *********************
    def select(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM machines ORDER BY id_machine ASC ;")
        value = cur.fetchall()
        return value

                                                   # ********************* SELECTIONER QLQ NOMS DE COLONNES *********************
    def select_colName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'machines' and COLUMN_NAME <> 'id_machine' and COLUMN_NAME <> 'port'  and COLUMN_NAME <> 'date_modification'  and COLUMN_NAME <> 'date_creation'")
        col_name = cur.fetchall()
        return col_name


                                                    # ********************* SELECTION QLQ VALUES *********************
    def select_colValue(self, idSelected):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT nom_machine, adresse_ip , type FROM machines where id_machine="+idSelected+";")
        value = cur.fetchall()
        tabValue = []
        for v in value:
            tabValue.append(v)
        return tabValue



                                                    # ********************* MODIFIER QLQ VALUES *********************
    def update_colValue(self, tab_update, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'machines' and COLUMN_NAME <> 'id_machine' and COLUMN_NAME <> 'port' and COLUMN_NAME <> 'date_modification'  and COLUMN_NAME <> 'date_creation'")
        col_name = cur.fetchall()

        for i in range(len(col_name)):
            cur.execute("UPDATE machines SET " + ''.join(col_name[i]) + "='" + tab_update[i] + "' where id_machine = '" + id + "';")
            conn.commit()


                                                    # ********************* DELETE ACCOUNT *********************
    def deleteMachine(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM machines WHERE id_machine ='" + id + "';")
        conn.commit()


                                                    # ********************* VÉRIFIER UNE MACHINE EXSIST OU NN  *********************
    def verifyMachine(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM machines WHERE id_machine ='" + id + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False


                                            # ********************* COMBOBOX LIST // MACHINES  *********************
    def combboxcMachin(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select nom_machine from machines;")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(''.join(a))
        return value



                                            # *********************SELECT IP_MACHINE  *********************
    def iPMachinE(self, nomMachine):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select adresse_ip  from machines WHERE nom_machine = '" + nomMachine + "';")
        ipMachine = cur.fetchone()
        return ipMachine

