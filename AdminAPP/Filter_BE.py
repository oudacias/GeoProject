import datetime
import os
import sys
sys.path.append(".")

from Connection.ConnectionFile import Connection

class Export:

    def selectIds(self, idP, id_un, id_deux, idsP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        result = []
        if (idP != '' and id_un == '' and id_deux == '' and idsP == ''):
            cur.execute("SELECT * FROM parcelles WHERE id_parcelle=" + idP + ";")
            result = cur.fetchall()

        elif (idP == '' and id_un != '' and id_deux == '' and idsP == ''):
            cur.execute("SELECT * FROM parcelles WHERE id_parcelle >= " + id_un + ";")
            result = cur.fetchall()

        elif (idP == '' and id_un == '' and id_deux != '' and idsP == ''):
            cur.execute("SELECT * FROM parcelles WHERE  id_parcelle <= " + id_deux + ";")
            result = cur.fetchall()

        elif (idP != '' and id_un != '' and id_deux != '' and idsP == ''):
            cur.execute("SELECT * FROM parcelles WHERE  id_parcelle = " + idP + " AND id_parcelle >= " + id_un + " OR id_parcelle <= " + id_deux + ";")
            result = cur.fetchall()

        elif (idP == '' and id_un != '' and id_deux != '' and idsP == ''):
            cur.execute("SELECT * FROM parcelles WHERE id_parcelle >= " + id_un + " AND  id_parcelle <= " + id_deux + " ;")
            result = cur.fetchall()
        return result

    def selectId(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT id_parcelle FROM parcelles;")
        result = cur.fetchall()
        return result

        '''if (idP != '' and id_un != '' and id_deux != '' and idsP != ''):
            cur.execute("SELECT * FROM parcelles WHERE id_parcelle = " + idP + " AND id_parcelle <= " + id_un + " AND id_parcelle>=" + id_deux + "  AND id_parcelle=" + idsP + ";")
            result = cur.fetchall()

        elif (idP != '' and id_un == '' and id_deux == '' and idsP == ''):
            cur.execute("SELECT * FROM parcelles WHERE id_parcelle=" + idP + ";")
            result = cur.fetchall()

        elif (idP == '' and id_un != '' and id_deux == '' and idsP == ''):
            cur.execute("SELECT * FROM parcelles WHERE id_parcelle<= " + id_un + ";")
            result = cur.fetchall()

        elif (idP == '' and id_un == '' and id_deux != '' and idsP == ''):
            cur.execute("SELECT * FROM parcelles WHERE  id_parcelle>=" + id_deux + ";")
            result = cur.fetchall()

        elif (idP == '' and id_un == '' and id_deux == '' and idsP != ''):
            pass

        elif (idP != '' and id_un != '' and id_deux != '' and idsP == ''):
            cur.execute("SELECT * FROM parcelle WHERE  id_parcelle = " + idP + " AND id_parcelle <= " + id_un + " AND id_parcelle >= " + id_deux + ";")
            result = cur.fetchall()


        elif (idP == '' and id_un != '' and id_deux != '' and idsP != ''):
            cur.execute("SELECT * FROM parcelle WHERE  id_parcelle <= " + id_un + " AND id_parcelle >= " + id_deux + "  AND id_parcelle=" + idsP + ";")
            result = cur.fetchall()

        elif (idP == '' and id_un != '' and id_deux != '' and idsP == ''):
            cur.execute("SELECT * FROM parcelle WHERE id_parcelle <= " + id_un + " AND  id_parcelle >= " + id_deux + " ;")
            result = cur.fetchall()

        elif (idP != '' and id_un == '' and id_deux == '' and idsP != ''):
            cur.execute("SELECT * FROM parcelle WHERE id_parcelle=" + idP + " AND id_parcelle=" + idsP + ";")
            result = cur.fetchall()'''

