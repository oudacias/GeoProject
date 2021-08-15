import socket
import pickle
from datetime import date
import datetime
import os
import sys
sys.path.append(".")

from Connection.ConnectionFile import Connection

class SynchClientGnr:

    def envoie(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT current_database()")
        current_database = cur.fetchone()

        cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public'")
        tableauFinal = cur.fetchall()

        val = []
        for tab in tableauFinal:
            cur.execute("select * from " + str(tab[0]))
            val = cur.fetchall()
            if val:
                for t in val:
                    final = list(t)
                    final.insert(0, tab[0])
                    print(final)
                    sockets(final)
        stop = ['stop']
        sockets(stop)


    def sockets(vals, nom):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT adresse_ip, port FROM machines WHERE nom_machine = '"+nom+"' ")
        nomPort = cur.fetchone()

        socktConxion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socktConxion.connect(("'"+nomPort[0]+"'", nomPort[1]))
        msg = pickle.dumps(vals)
        socktConxion.send(msg)
        print('message sent')
        socktConxion.close()
        print('connection closed')

