import socket
import pickle
import os
import sys

sys.path.append(".")
from datetime import date
from tkinter.messagebox import *


from Connection.ConnectionFile import Connection

class SynchServerGnr:
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
            cur.execute("SELECT current_database()")
            current_database = cur.fetchone()
            start_add = True
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
                if (action_table[0] == "insert"):
                    for tab in tables:
                        cur.execute("ALTER TABLE " + tab + " DISABLE TRIGGER all")
                        conn.commit()
                    for i in range(1, len(action_table)):
                        cur.execute("delete from " + action_table[i] + " ")
                        conn.commit()
                    while start_add:
                        msg = client.recv(90000000)
                        table = pickle.loads(msg)
                        if (table[0] != "stop"):
                            cur.execute("select count(*) from information_schema.columns where table_name='" + str(table[0]) + "';")
                            nbr_column = cur.fetchone()
                            s = ','.join("%s" for i in range(nbr_column[0]))
                            cur.execute("INSERT INTO " + str(table[0]) + " VALUES (" + s + ");", table[1:len(table)])
                            conn.commit()
                        else:
                            for tab in tables:
                                cur.execute("ALTER TABLE " + tab + " ENABLE TRIGGER all")
                                conn.commit()
                            start_add = False
                            showinfo("Réception", "Le transfert des données vers votre machine est terminé avec succès")

            elif database_name == "null":
                showerror("Réception", "Les marchés ne sont pas identiques")
                msg = pickle.dumps(False)
                client.send(msg)
                return False
            else:
                showerror("Réception", "Problème de connection avec la Base de données!")
                msg = pickle.dumps(False)
                client.send(msg)
                return False
        else:
            msg = pickle.dumps(False)
            client.send(msg)
        socktConxion.close()


if __name__ == '__main__':
    SynchServerGnr().receiveData()