import socket
import pickle
from datetime import date
import datetime
import os
import sys
sys.path.append(".")

from Connection.ConnectionFile import Connection

class SynchClientJr:

    def envoie(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT current_database()")
        current_database = cur.fetchone()

        cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public'")
        tableauFinal = cur.fetchall()

        self.val = []
        today = date.today()
        for tab in tableauFinal:
            cur.execute("select * from  " + str(tab[0]) + " where date(date_creation) = '" + str(today) + "' or date_modification = '" + str(today) + "'")
            self.val = cur.fetchall()
            cur.execute("select date(date_creation),date_modification from  " + str(tab[0]) + " where date(date_creation) = '" + str(today) + "' or date_modification = '" + str(today) + "'")
            dat = cur.fetchall()
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = '" + tab[0] + "' limit 1;")
            column_id = cur.fetchone()

            if self.val:
                for t in range(len(self.val)):
                    final = list(self.val[t])
                    final.insert(0, current_database[0])

                    final.insert(1, tab[0])
                    final.insert(2, column_id[0])
                    final.insert(len(final) - 1, str(final[len(final) - 1]))
                    final.pop()

                    if dat[t][1] == None:
                        final.insert(3, 'ajout')
                        print(final)
                    elif datetime.datetime.strptime(dat[t][1], '%Y-%m-%d').date() == dat[t][0]:
                        final.insert(3, 'ajout')
                        print(final)
                    elif datetime.datetime.strptime(dat[t][1], '%Y-%m-%d').date() > dat[t][0]:
                        final.insert(3, 'modification')
                        print(final)
                    self.sockets(final)
                    self.sockets(final)
        stop = ['stop']
        self.sockets(stop)


    def selectIp(self,nom):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT adresse_ip, port FROM machines WHERE nom_machine = '"+nom+"' ")
        self.nomPort = cur.fetchone()


    def sockets(self,vals):
        socktConxion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socktConxion.connect(("'"+self.nomPort[0]+"'", self.nomPort[1]))
        msg = pickle.dumps(vals)
        socktConxion.send(msg)
        print('message sent')
        socktConxion.close()
        print('connection closed')

