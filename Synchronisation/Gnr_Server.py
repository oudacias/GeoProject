import socket
import pickle
import os
import sys
from tkinter.messagebox import *

sys.path.append(".")
import time

from Connection.ConnectionFile import Connection

class SynchServerGnr:
    def sendData(self, adressIp):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()

        cur.execute("select count(*) from machines limit 1")
        machine_count = cur.fetchone()
        if (machine_count[0] > 0):
            cur.execute("select port from machines limit 1")
            port = cur.fetchone()
            socktConxion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socktConxion.connect((adressIp, port[0]))
            msg = socktConxion.recv(90000000)
            check_socket = pickle.loads(msg)
            if (check_socket):
                cur.execute("select count(*) from machines where adresse_ip = '" + adressIp + "'")
                ipMachine = cur.fetchone()
                if ipMachine[0] > 0:
                    cur.execute("SELECT current_database()")
                    current_database = cur.fetchone()
                    msg = pickle.dumps(current_database[0])
                    socktConxion.send(msg)
                    check_database = socktConxion.recv(900000000)
                    check_database = pickle.loads(check_database)

                    if (check_database):
                        tables = ["marche", "zone", "sous_zone", "douar", "consistance", "type_sol", "type_speculation",
                                  "type_opposition", "brigades", "parcelles", "personnes", "cles", "points",
                                  "synchronisation", "machines"]
                        tableTab = []
                        for tab in tables:
                            cur.execute("select * from  " + str(tab) + ";")
                            values = cur.fetchall()
                            if (values):
                                tableTab.append(str(tab))

                        if (tableTab):
                            tableTab.insert(0, "insert")
                            msg = pickle.dumps(tableTab)
                            socktConxion.send(msg)

                            tableTab.pop(0)
                            for table in tableTab:
                                cur.execute("select * from  " + table + " ;")
                                values = cur.fetchall()
                                for v in range(len(values)):
                                    final_table = list(values[v])
                                    final_table.insert(0, table)
                                    msg = pickle.dumps(final_table)
                                    time.sleep(0.5)
                                    socktConxion.send(msg)
                            msg = pickle.dumps(["stop"])
                            socktConxion.send(msg)

                        else:
                            msg = pickle.dumps(["stop"])
                            socktConxion.send(msg)
                            cur.execute("select nom_machine from machines where adresse_ip = '" + adressIp + "'")
                            nomMachine = cur.fetchone()
                            showerror("Envoie", "Le transfert de données vers la machine " + nomMachine + " est terminé")
                    else:
                        showerror("Envoie", "Problème de connection avec la Base de données!")
                else:
                    msg = pickle.dumps("null")
                    socktConxion.send(msg)
            else:
                showerror("Envoie", "Machine Occuppée!!!")
        else:
            showerror("Envoie", "Pas de machine dans la base de données")

        socktConxion.close()


if __name__ == '__main__':
    SynchServerGnr().sendData()
