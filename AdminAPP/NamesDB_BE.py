import os
import datetime
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class NewDB:

                                                                       # ******************** Les noms de colonnes // TREEVIEW***********************
    def addNew_db(self, nom_db):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO db_name values (DEFAULT , '"+nom_db+"', '"+str(datetime.datetime.now())+"')")
        conn.commit()