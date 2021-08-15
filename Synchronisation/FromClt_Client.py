import socket
import pickle
from datetime import date
import os
import sys

sys.path.append(".")
import psycopg2
import time
from tkinter.messagebox import *


from Connection.ConnectionFile import Connection

class SynchClientJr:
    def sendData(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select port from machines limit 1")
        port = cur.fetchone()
        cur.execute("select adresse_ip from machines WHERE type = 'server' ")
        ip = cur.fetchone()

        if (ip != None):
            socktConxion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socktConxion.connect((ip[0], port[0]))
            msg = socktConxion.recv(90000000)
            check_socket = pickle.loads(msg)
            if (check_socket):
                synch_status = socktConxion.recv(900000000)
                synch_status = pickle.loads(synch_status)

                if (synch_status):
                    cur.execute("SELECT current_database()")
                    current_database = cur.fetchone()
                    msg = pickle.dumps(current_database[0])
                    socktConxion.send(msg)
                    check_database = socktConxion.recv(900000000)
                    check_database = pickle.loads(check_database)
                    today_tables_add = []
                    today = date.today()

                    if (check_database):
                        tables = ["marche", "zone", "sous_zone", "douar", "consistance", "type_sol", "type_speculation",
                                  "type_opposition", "brigades", "parcelles", "personnes", "cles", "rivrains", "points",
                                  "synchronisation", "machines"]
                        for tab in tables:
                            cur.execute("select * from  " + str(tab) + " where date(date_creation) = '" + str(today) + "'")
                            val = cur.fetchall()
                            if (val):
                                today_tables_add.append(str(tab))
                        if (today_tables_add):
                            today_tables_add.insert(0, "synchro_today_add")
                            msg = pickle.dumps(today_tables_add)
                            socktConxion.send(msg)
                            updated_ids = socktConxion.recv(900000000)
                            updated_id = pickle.loads(updated_ids)
                            for key, value in updated_id.items():
                                if (value[1] > 0):
                                    cur.execute("select " + value[0] + " from  " + key + " where date(date_creation) = '" + str(today) + "' order by " + value[0] + " desc")
                                    val = cur.fetchall()
                                    for v in val:
                                        cur.execute("update " + key + " set " + value[0] + " = " + str(int(v[0] + value[1])) + " where " + value[0] + "=" + str(v[0]))
                            for key, value in updated_id.items():
                                cur.execute("select * from  " + key + " where date(date_creation) = '" + str(today) + "' order by " + value[0] + " asc")
                                val = cur.fetchall()
                                for v in range(len(val)):
                                    final_table = list(val[v])
                                    final_table.insert(0, key)
                                    msg = pickle.dumps(final_table)
                                    time.sleep(0.2)
                                    socktConxion.send(msg)
                            msg = pickle.dumps(["stop"])
                            socktConxion.send(msg)
                            time.sleep(0.2)
                        else:
                            showerror("Envoie", "Aucune donnée ajoutée aujourd'hui!")
                            msg = pickle.dumps(["stop"])
                            socktConxion.send(msg)

                        time.sleep(0.3)
                        today_tables_update = []
                        for tab in tables:
                            cur.execute("select * from  " + str(tab) + " where date(date_modification) = '" + str(today) + "' and date(date_creation) < '" + str(today) + "'")
                            val = cur.fetchall()
                            if (val):
                                today_tables_update.append(tab)
                        if (today_tables_update):
                            msg = pickle.dumps(["synchro_today_update"])
                            socktConxion.send(msg)
                            time.sleep(0.2)
                            for tab in today_tables_update:
                                cur.execute("select * from  " + str(tab) + " where date(date_modification) = '" + str(today) + "' and date(date_creation) < '" + str(today) + "'")
                                val = cur.fetchall()
                                for v in range(len(val)):
                                    today_tables_update = list(val[v])
                                    today_tables_update.insert(0, tab)
                                    msg = pickle.dumps(today_tables_update)
                                    socktConxion.send(msg)
                                    time.sleep(0.4)
                        else:
                            showerror("Envoie", "Aucune donnée modifiée aujourd'hui!")
                            msg = pickle.dumps(["stop"])
                            socktConxion.send(msg)
                        cur.execute("select nom_machine from machines WHERE type = 'server' ")
                        nomMachine = cur.fetchone()
                        showinfo("Envoie", "le transfert de données vers la machine " + nomMachine + " est terminé")
                        socktConxion.close()
                    else:
                        showerror("Envoie", "Problème de connection avec la Base de données!")
                else:
                    showerror("Envoie", "Envoie des données déjà efféctué!")
            else:
                showerror("Envoie", "Machine Occuppée!!!")
                socktConxion.close()


if __name__ == '__main__':
    SynchClientJr().sendData()
