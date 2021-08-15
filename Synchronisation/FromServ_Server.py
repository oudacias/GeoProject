import socket
import pickle
from datetime import date
from tkinter.messagebox import *
import datetime
import os
import sys

sys.path.append(".")
import psycopg2
import time


from Connection.ConnectionFile import Connection

class SynchServerJr:
    def sendData(self, adressIp):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()

        today = date.today()

        cur.execute("select count(*) from synchronisation where sent = true and date(date_creation) = '" + str(today) + "'")
        nbr_synch = cur.fetchone()

        cur.execute("select count(*) from machines")
        nbr_machines = cur.fetchone()

        start_synch = False

        if (nbr_machines[0] > nbr_synch[0]):
            start_synch = askokcancel("Message","Le nombre de synchronisations ne correspond pas au nombres machines. Continuez ?")
        elif (nbr_machines[0] == nbr_synch[0]):
            start_synch = True

        if (start_synch):
            socktConxion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socktConxion.connect((adressIp, 9099))

            msg = socktConxion.recv(90000000)
            check_socket = pickle.loads(msg)
            if (check_socket):

                msg = pickle.dumps(True)
                socktConxion.send(msg)
                cur.execute("select count(*) from machines where adresse_ip = '" + adressIp + "'")
                ipMachine = cur.fetchone()

                if (ipMachine[0] > 0):
                    msg = pickle.dumps(True)
                    socktConxion.send(msg)
                    msg = socktConxion.recv(90000000)
                    check_machine = pickle.loads(msg)

                    if (check_machine):
                        cur.execute("select count(*) from synchronisation where adresse_ip = '" + adressIp + "' and received = true and date(date_creation) = '" + str(today) + "'")
                        machineSych = cur.fetchone()

                        if machineSych[0] == 0:
                            msg = pickle.dumps(True)
                            socktConxion.send(msg)

                            cur.execute("SELECT current_database()")
                            current_database = cur.fetchone()
                            msg = pickle.dumps(current_database[0])
                            socktConxion.send(msg)
                            check_database = socktConxion.recv(900000000)
                            check_database = pickle.loads(check_database)
                            today = date.today()
                            if (check_database):
                                tables = ["marche", "zone", "sous_zone", "douar", "consistance", "type_sol",
                                          "type_speculation", "type_opposition", "brigades", "parcelles", "personnes",
                                          "cles", "points", "synchronisation", "machines"]
                                # Date_création = Today
                                today_tables_add = []
                                for tab in tables:
                                    cur.execute("select * from  " + str(tab) + " where date(date_creation) = '" + str(today) + "'")
                                    val = cur.fetchall()
                                    if (val):
                                        today_tables_add.append(str(tab))
                                if (today_tables_add):
                                    today_tables_add.insert(0, "synchro_today_add")
                                    msg = pickle.dumps(today_tables_add)
                                    socktConxion.send(msg)
                                    today_tables_add.pop(0)
                                    for table in today_tables_add:
                                        cur.execute("select * from  " + table + " where date(date_creation) = '" + str(today) + "' ")
                                        values = cur.fetchall()
                                        for v in range(len(values)):
                                            final_table = list(values[v])
                                            final_table.insert(0, table)
                                            msg = pickle.dumps(final_table)
                                            socktConxion.send(msg)
                                            time.sleep(0.5)
                                    msg = pickle.dumps(["stop"])
                                    socktConxion.send(msg)
                                else:
                                    msg = pickle.dumps(["stop"])
                                    socktConxion.send(msg)

# Date_Modification = Today AND date_création < Today
                                today_tables_update = []
                                for tab in tables:
                                    cur.execute("select * from  " + str(tab) + " where date(date_modification) = '" + str(today) + "' and date(date_creation) < '" + str(today) + "'")
                                    val = cur.fetchall()
                                    if (val):
                                        today_tables_update.append(str(tab))
                                if (today_tables_update):
                                    today_tables_update.insert(0, "synchro_today_update")
                                    msg = pickle.dumps(today_tables_update)
                                    socktConxion.send(msg)
                                    today_tables_update.pop(0)
                                    for table in today_tables_update:
                                        cur.execute("select * from  " + table + " where date(date_modification) = '" + str(today) + "' and date(date_creation) < '" + str(today) + "'")
                                        values = cur.fetchall()
                                        for v in range(len(values)):
                                            final_table = list(values[v])
                                            final_table.insert(0, table)
                                            msg = pickle.dumps(final_table)
                                            socktConxion.send(msg)
                                            time.sleep(0.5)
                                    msg = pickle.dumps(["stop"])
                                    socktConxion.send(msg)
                                else:
                                    msg = pickle.dumps(["stop"])
                                    socktConxion.send(msg)
                                    cur.execute("select count(*) from synchronisation where adresse_ip = '" + adressIp + "' and date(date_creation) = '" + str(today) + "'")
                                    machineSych = cur.fetchone()

                                    if machineSych[0] == 1:
                                        cur.execute("update synchronisation set received = true where adresse_ip = '" + adressIp + "' and date(date_creation) = '" + str(today) + "'")
                                        conn.commit()
                                    elif machineSych[0] == 0:
                                        cur.execute("INSERT INTO synchronisation (adresse_ip,received) VALUES ('" + str(adressIp) + "',True)")
                                        conn.commit()
                                cur.execute("select nom_machine from machines WHERE adresse_ip = '" + adressIp + "' ")
                                nomMachine = cur.fetchone()
                                showinfo("Envoie", "Le transfert de données vers la machine " + nomMachine + " est terminé")
                            else:
                                showerror("Envoie", "Problème de connection avec la Base de donnéessss!")

                        elif (machineSych[0] == 1):
                            showerror("Envoie", "Machine déjà synchronisée")
                            msg = pickle.dumps(False)
                            socktConxion.send(msg)
                    else:
                        showerror("Envoie", "Adresse non reconnue par l'autre machine!!!")
                else:
                    showerror("Envoie", "Machine Inconnue!!!")
                    msg = pickle.dumps(False)
                    socktConxion.send(msg)
            else:
                showerror("Envoie", "Machine Occuppée!!!")
                socktConxion.close()

        else:
            socktConxion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socktConxion.connect((adressIp, 9099))
            msg = pickle.dumps(False)
            socktConxion.send(msg)
        socktConxion.close()


if __name__ == '__main__':
    SynchServerJr().sendData()
