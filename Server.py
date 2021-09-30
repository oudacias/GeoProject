import socket
import pickle
import os
import sys
sys.path.append(".")

from Connection.ConnectionFile import Connection

class SynchServer:

    def receiveData(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT current_database()")
        current_database = cur.fetchone()
        socktConxion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socktConxion.bind((socket.gethostbyname(socket.gethostname()), 1234))
        socktConxion.listen(5)
        start = True

        while start:
            client, address = socktConxion.accept()
            msg = client.recv(90000000)
            tableau = pickle.loads(msg)
            #if(tableau[0] == current_database[0]):
            if(tableau[0] != current_database[0] and len(tableau)>0):
                if (tableau[0] != 'stop'):
                    cur.execute("SELECT count(" + str(tableau[2]) + ") from " + str(tableau[1]) + " where " + str(tableau[2]) + " = " + str(tableau[4]) + "")
                    same_id = cur.fetchone()
                    if tableau[3] == 'ajout':
                        if same_id[0] > 0:
                            cur.execute("delete from " + str(tableau[1]) + " WHERE (" + str(tableau[2]) + " = " + str(tableau[4]) + ")")
                            conn.commit()
                        cur.execute("INSERT INTO " + str(tableau[1]) + " VALUES (" + (str(tableau[4:len(tableau)]).replace('[', '').replace(']', '').replace('None', 'null')) + ")")
                        conn.commit()
                    elif tableau[3] == 'modification':
                        cur.execute("delete from " + str(tableau[1]) + " WHERE (" + str(tableau[2]) + " = " + str(tableau[4]) + ")")
                        conn.commit()
                        cur.execute("INSERT INTO " + str(tableau[1]) + " VALUES (" + (str(tableau[4:len(tableau)]).replace('[', '').replace(']', '').replace('None', 'null')) + ")")
                        conn.commit()
                else:
                    start = False
            else:
                print('Different DB')
                start = False