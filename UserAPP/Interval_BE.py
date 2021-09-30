import time
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class Intervalle:



                                # ********************************************************** DELETE INTERVAL
    def delteInterv(self, idB):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM intervalle USING brigades WHERE intervalle.id_brigade = brigades.id_brigade AND intervalle.id_brigade ='" + idB + "';")
        conn.commit()


                                # ********************************************************** SELECT INTERVAL PARCELLE
    def polygInterv(self, idBrg):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT intervalle_debut,intervalle_fin FROM intervalle WHERE id_brigade = '" + idBrg + "' AND nom_table = 'parcelles' ;")
        interv = cur.fetchall()
        return interv


                                # ********************************************************** SELECT INTERVAL PARCELLE
    def changeInterv_Polyg(self, idBrg):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        t = time.sleep(5)
        cur.execute("SELECT MAX (intervalle_fin) FROM intervalle where nom_table =  'parcelles';")
        intervMax = cur.fetchone()
        deb = str(intervMax[0])
        fin = str(intervMax[0])
        cur.execute("update intervalle set intervalle_debut = "+deb+"+1 , intervalle_fin = " +fin+"+5 where id_brigade = '" + idBrg + "';")
        conn.commit()


                                # ********************************************************** SELECT INTERVAL MAX
    def max_interv(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #t = time.sleep(5)
        cur.execute("SELECT MAX (intervalle_fin) FROM intervalle where nom_table =  'parcelles' and id_brigade = 1;")
        intervMax = cur.fetchone()
        return intervMax