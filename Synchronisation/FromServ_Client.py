import socket
import pickle
import os
import sys
import psycopg2

sys.path.append(".")
from datetime import date
from tkinter.messagebox import *


from Connection.ConnectionFile import Connection

class SynchServerJr:
    def receiveData(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()

        socktConxion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socktConxion.bind(((socket.gethostbyname(socket.gethostname()), 9099)))
        socktConxion.listen(1)
        start_socket = False
        client, address = socktConxion.accept()
        if (client):
            start_socket = askokcancel("Message", "Une machine veut se connecter")
        if (start_socket):
            msg = pickle.dumps(True)
            client.send(msg)

            today = date.today()

            msg = client.recv(90000000)
            check_synch = pickle.loads(msg)

            if (check_synch):

                msg = client.recv(90000000)
                check_machine = pickle.loads(msg)

                if (check_machine):

                    cur.execute("select count(*) from machines where adresse_ip = '" + str(address[0]) + "'")
                    ipMachine = cur.fetchone()

                    if ipMachine[0] > 0:

                        msg = pickle.dumps(True)
                        client.send(msg)

                        cur.execute("SELECT current_database()")
                        current_database = cur.fetchone()

                        start_add = True
                        start_update = True

                        tables = ["marche", "zone", "sous_zone", "douar", "consistance", "type_sol", "type_speculation",
                                  "type_opposition", "brigades", "parcelles", "personnes", "cles", "rivrains", "points",
                                  "synchronisation", "machines"]
                        today = date.today()
                        msg = client.recv(90000000)
                        database_name = pickle.loads(msg)

                        if (database_name != current_database[0]):
                            msg = pickle.dumps(True)
                            client.send(msg)

                            # Date_création = Today
                            msg = client.recv(90000000)
                            action_table = pickle.loads(msg)
                            if (action_table[0] == "synchro_today_add"):
                                for tab in tables:
                                    cur.execute("ALTER TABLE " + tab + " DISABLE TRIGGER all")
                                    conn.commit()
                                for i in range(1, len(action_table)):
                                    cur.execute(
                                        "delete from " + action_table[i] + " where date(date_creation) = '" + str(
                                            today) + "'")
                                    conn.commit()
                                while start_add:
                                    msg = client.recv(90000000)
                                    table = pickle.loads(msg)
                                    if (table[0] != "stop"):
                                        cur.execute(
                                            "select count(*) from information_schema.columns where table_name='" + str(
                                                table[0]) + "';")
                                        nbr_column = cur.fetchone()
                                        s = ','.join("%s" for i in range(nbr_column[0]))
                                        cur.execute("INSERT INTO " + str(table[0]) + " VALUES (" + s + ");",
                                                    table[1:len(table)])
                                        conn.commit()
                                    else:
                                        for tab in tables:
                                            cur.execute("ALTER TABLE " + tab + " ENABLE TRIGGER all")
                                            conn.commit()
                                        start_add = False

                            # Date_Modification = Today AND date_création < Today
                            msg = client.recv(90000000)
                            action_table = pickle.loads(msg)
                            if (action_table[0] == "synchro_today_update"):
                                for tab in tables:
                                    cur.execute("ALTER TABLE " + tab + " DISABLE TRIGGER all")
                                    conn.commit()
                                while start_update:
                                    msg = client.recv(90000000)
                                    table_data = pickle.loads(msg)
                                    if (table_data[0] != "stop"):
                                        cur.execute(
                                            "select column_name from information_schema.columns where table_name='" + str(
                                                table_data[0]) + "';")
                                        column_name = cur.fetchall()
                                        sql_update_query = "update " + str(table_data[0]) + " set " + (', '.join(
                                            str(column_name[i][0]) + " = " + "%s" for i in
                                            range(1, len(column_name)))) + " where " + str(column_name[0][0]) + " = %s"
                                        temp_data = table_data[2:]
                                        x = temp_data.append(table_data[1])
                                        cur.execute(sql_update_query, (temp_data))
                                        conn.commit()
                                    else:
                                        for tab in tables:
                                            cur.execute("ALTER TABLE " + tab + " ENABLE TRIGGER all")
                                            conn.commit()
                                        start_update = False
                                showinfo("Recevoir",
                                         "le transfert des données vers votre machine est terminé avec succès")

                        else:
                            showerror("Recevoir", "Problème de connection avec la Base de données!")
                            msg = pickle.dumps(False)
                            client.send(msg)
                            return False
                    else:
                        showerror("Recevoir", "Machine Inconnue!")
                        msg = pickle.dumps(False)
                        client.send(msg)
                        return False
                else:
                    showerror("Envoie", "Adresse non reconnue par l'autre machine!!!")
            else:
                showerror("Envoie", "Reception des données déjà éffectuée")
        else:
            msg = pickle.dumps(False)
            client.send(msg)
        socktConxion.close()


if __name__ == '__main__':
    SynchServerJr().receiveData()