import os
import datetime
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir)  + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection


class User:
                                             # ******************** Verify User Account *********************
    def user_verification(self, user, password):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        username = user.split()
        cur.execute("SELECT COUNT (*) FROM utilisateurs WHERE nom ='" + username[0] + "' and prenom ='" + username[1] + "' and password ='" + password + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False


                                                #********************* Verify Admin ****************************
    def admin_verification(self, utilisateur, password):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        username = utilisateur.split()
        cur.execute("SELECT COUNT (*) FROM utilisateurs WHERE nom ='" + username[0] + "' and prenom ='" + username[1] + "' and password ='" + password + "' and admin = 'oui';")
        adm = cur.fetchone()
        if (adm[0] == 1):
            return True
        elif (adm[0] == 0):
            return False

                                             # ******************** Change Password // Verify User Account *********************
    def verify_User(self, nm, prnom):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM utilisateurs WHERE nom ='" + nm + "' and prenom ='" + prnom + "';")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False


                                            #********************* Change Password ****************************
    def change_password(self, prenom, nom, pswrd):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("UPDATE utilisateurs SET password='" + pswrd + "' where prenom = '" + prenom + "' and nom = '" + nom + "';")
        conn.commit()


                                                    # ********************* COLUMN NAMES*********************
    def columnName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'utilisateurs'")
        col_name = cur.fetchall()
        return col_name


                                                    # ********************* VALUES *********************
    def select(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs ORDER BY id_user ASC ;")
        value = cur.fetchall()
        return value


                                                    # ********************* SELECTION QLQ NOMS DE COLONNES *********************
    def select_colName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'utilisateurs' and COLUMN_NAME <> 'id_user' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()
        return col_name


                                                    # ********************* SELECTION QLQ VALUES *********************
    def select_colValue(self, idSelected):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT id_brigade, nom, prenom, admin, password FROM utilisateurs where id_user="+idSelected+" ;")
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
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'utilisateurs' and COLUMN_NAME <> 'id_user' and COLUMN_NAME <> 'date_creation' and COLUMN_NAME <> 'date_modification'")
        col_name = cur.fetchall()

        for i in range(len(col_name)):
            cur.execute("UPDATE utilisateurs SET " + ''.join(col_name[i]) + "='" + tab_update[i] + "', date_modification = '"+str(datetime.datetime.now())+"' where id_user = '" + id + "';")
            conn.commit()


                                                    # ********************* VÉRIFIER UN COMPTE EXSIST OU NN  *********************
    def verifyAccount(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM utilisateurs WHERE id_user ='" + id + "' ;")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False


                                                    # ********************* DELETE ACCOUNT *********************
    def deleteAccount(self, id):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM utilisateurs WHERE id_user ='" + id + "';")
        conn.commit()


                                                    # ********************* MODIFIER QLQ VALUES *********************
    def insert(self, id_brigade, nom_user, prenom_user, admin, password):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO utilisateurs (id_user,id_brigade, nom, prenom, admin, password, date_creation) VALUES (DEFAULT ,"+id_brigade+" , '"+nom_user+"', '"+prenom_user+"', '"+admin+"', '"+password+"', '"+str(datetime.datetime.now())+"')")
        conn.commit()


                                                    # ********************* COMBOBOX LIST / UTILISATEUR **************
    def combboxUsr(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select nom from utilisateurs ;")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(''.join(a))
        return value

                                          # -------------- COMBOBOX // Nom et Prénom de toutes les personnels  ------------
    def usersList(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT nom,prenom FROM utilisateurs")
        values = cur.fetchall()
        value = []
        for a in range(len(values)):
            value.append(''.join(str(values[a][0]))+ ' '+ ''.join(str(values[a][1])))
        return value
