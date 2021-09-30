import socket
import pickle
import os
import sys
import psycopg2

sys.path.append(".")
from datetime import date
from collections import OrderedDict
from tkinter.messagebox import *


from Connection.ConnectionFile import Connection

class SynchClientJr:
    def receiveData(self):

        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        socktConxion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socktConxion.bind(((socket.gethostbyname(socket.gethostname()), 9099)))
        socktConxion.listen(1)

        client, address = socktConxion.accept()
        if (client):
            start_socket = askokcancel("Message", "Une machine veut se connecter")

        if (start_socket):
            msg = pickle.dumps(True)
            client.send(msg)

            today = date.today()

            cur.execute("select count(*) from machines where adresse_ip = '" + str(address[0]) + "'")
            ipMachine = cur.fetchone()
            if ipMachine[0] > 0:
                cur.execute("select count(*) from synchronisation where adresse_ip = '" + str(address[0]) + "' and sent = true and date(date_creation) = '" + str(today) + "'")
                ipSynch = cur.fetchone()
                if ipSynch[0] == 1:
                    cur.execute("select nom_machine from machines WHERE type = 'server' ")
                    nomMachine = cur.fetchone()
                    showerror("Réception", "La machine " + nomMachine + " vous a déja transférée les données !")
                    msg = pickle.dumps(False)
                    client.send(msg)
                    return False
                else:
                    msg = pickle.dumps(True)
                    client.send(msg)
                    cur.execute("SELECT current_database()")
                    current_database = cur.fetchone()
                    start_add = True
                    start_update = True
                    today = date.today()
                    tables = ["marche", "zone", "sous_zone", "douar", "consistance", "type_sol", "type_speculation",
                              "type_opposition", "brigades", "parcelles", "personnes", "cles", "rivrains", "points",
                              "synchronisation", "machines"]
                    msg = client.recv(90000000)
                    database_name = pickle.loads(msg)
                    if (database_name == current_database[0]):
                        msg = pickle.dumps(True)
                        client.send(msg)
                        msg = client.recv(90000000)
                        action_table = pickle.loads(msg)
                        if (action_table[0] == "synchro_today_add"):
                            for tab in tables:
                                cur.execute("ALTER TABLE " + tab + " DISABLE TRIGGER all")
                                conn.commit()
                            last_id_table = OrderedDict()
                            for i in range(1, len(action_table)):
                                cur.execute("select column_name from information_schema.columns where table_name = '" +action_table[i] + "' limit 1")
                                id_column = cur.fetchone()
                                cur.execute("SELECT count(" + id_column[0] + ") from " + action_table[i] + " where date(date_creation) = '" + str(today) + "'")
                                max_id = cur.fetchone()
                                if (max_id[0] == None):
                                    last_id_table[action_table[i]] = [id_column[0], 0]
                                else:
                                    last_id_table[action_table[i]] = [id_column[0], max_id[0]]
                            client.send(pickle.dumps(last_id_table))
                            while start_add:
                                msg = client.recv(90000000)
                                table = pickle.loads(msg)
                                if (table[0] != "stop"):
                                    cur.execute("select count(*) from information_schema.columns where table_name='" + str(table[0]) + "';")
                                    nbr_column = cur.fetchone()
                                    s = ','.join("%s" for i in range(nbr_column[0]))
                                    cur.execute("INSERT INTO " + str(table[0]) + " VALUES (" + s + ");",table[1:len(table)])
                                else:
                                    start_add = False
                                    for tab in tables:
                                        cur.execute("alter table " + str(tab) + " enable trigger all;")
                                        conn.commit()

                        msg = client.recv(90000000)
                        action_table = pickle.loads(msg)
                        if (action_table[0] == "synchro_today_update"):
                            for tab in tables:
                                cur.execute("alter table " + str(tab) + " disable trigger all;")
                                conn.commit()
                            while start_update:
                                msg = client.recv(90000000)
                                table_data = pickle.loads(msg)
                                if (table_data[0] != "stop"):
                                    cur.execute("select column_name from information_schema.columns where table_name='" + str(table_data[0]) + "';")
                                    column_name = cur.fetchall()

                                    cur.execute("select count(*) from " + str(table_data[0]) + " where " + str(column_name[0][0]) + "=" + str(table_data[1]) + ";")
                                    check_id = cur.fetchone()
                                    if (check_id):
                                        sql_update_query = "update " + str(table_data[0]) + " set " + (', '.join(str(column_name[i][0]) + " = " + "%s" for i in range(1, len(column_name)))) + " where " + str(column_name[0][0]) + " = %s"
                                        temp_data = table_data[2:]
                                        temp_data.append(table_data[1])
                                        cur.execute(sql_update_query, (temp_data))
                                        conn.commit()
                                else:
                                    start_update = False
                                    for tab in tables:
                                        cur.execute("alter table " + str(tab) + " enable trigger all;")
                                        conn.commit()
                        showinfo("Réception", "Le transfert des données vers votre machine est terminé avec succès")

                        cur.execute("INSERT INTO synchronisation (adresse_ip,sent) VALUES ('" + str(address[0]) + "',True)")
                        conn.commit()
                    else:
                        msg = pickle.dumps(False)
                        client.send(msg)
                        showerror("Recevoir", "Problème de connection avec la Base de données!")
            else:
                msg = pickle.dumps(True)
                client.send(msg)
                showerror("Recevoir", "Machine Inconnue!")
        else:
            msg = pickle.dumps(False)
            client.send(msg)

        socktConxion.close()


#if __name__ == '__main__':
    #SynchClientJr().receiveData()

