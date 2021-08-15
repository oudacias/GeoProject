from datetime import datetime
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH):
    from Connection.ConnectionFile import Connection
else:
    print("yes")

class Marche:
    def __init__(self):
        self.tab = []

                                        # ******************** Create New Project *********************
    def create_projct (self, datValue, marche, sect, cercle, cerc_ar, prov, prov_ar, commune, com_ar, conservFonc, conFon_ar, geom, bul_off, date):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        if datValue == '' or datValue == None:
            cur.execute("INSERT INTO marche(id_marche, marche, secteur, cercle, الدائرة, province, الاقليم, commune, الجماعة, conservation_fonciere, المحافظةالعقارية, geometre, bulletin_off, date, date_creation) VALUES "
                "(DEFAULT ,'" + marche + "', '" + sect + "', '" + cercle + "', '" + cerc_ar + "', '" + prov + "', '" + prov_ar + "', '" + commune + "', '" + com_ar + "','" + conservFonc + "', '" + conFon_ar + "', '" + geom + "', '" + bul_off + "', null , '" + str(datetime.now()) + "')")
            conn.commit()
        elif datValue != '':
            cur.execute("INSERT INTO marche(id_marche, marche, secteur, cercle, الدائرة, province, الاقليم, commune, الجماعة, conservation_fonciere, المحافظةالعقارية, geometre, bulletin_off, date, date_creation) VALUES "
                        "(DEFAULT ,'"+marche+"', '"+sect+"', '"+cercle+"', '"+cerc_ar+"', '"+prov+"', '"+prov_ar+"', '"+commune+"', '"+com_ar+"','"+conservFonc+"', '"+conFon_ar+"', '"+geom+"', '"+bul_off+"', '"+date+"', '"+str(datetime.now())+"')")
            conn.commit()


                                        # ******************** Open Project **************************
    def open_project(self, marche):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM marche WHERE marche ='" + marche + "';")
        nbrlgn = cur.fetchone()
        if (nbrlgn[0] == 1):
            return True
        elif (nbrlgn[0] == 0):
            return False
        conn.close()


                                        # ******************** Project List**************************
    def list_project(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select distinct marche from marche;")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(''.join(a))
        return value


                                        # ******************** COMBOBOX Secteurs List ****************
    def combxSect(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select distinct secteur from marche;")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(''.join(a))
        return value



    def verifyMarche(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM marche ;")
        nbrlgn = cur.fetchone()
        if (nbrlgn[0] == 1):
            return True
        elif (nbrlgn[0] == 0):
            return False

    def dbCombbx(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select datname from pg_database")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(a[0])
        return value


    def verifyDB(self, dbName):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM pg_database WHERE datname='"+dbName+"';")
        nbrlgn = cur.fetchone()
        if (nbrlgn[0] >= 1):
            return True
        elif (nbrlgn[0] == 0):
            return False



    def connect_marche(self, dbN):
        if os.path.isfile(PATH):
            print("Hello")
        else:
            print("nooo")
        print(dbN +"////////")
        if(dbN != ''):
            from Connection.ConnectionFile import Connection
            connection = Connection()
            conn = connection.connect()
            cur = conn.cursor()
            cur.execute('select current_database()')
            current_db = cur.fetchone()
            file = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'

            connection_file = open(file, 'r+')
            content = connection_file.read()
            new_content = content.replace(current_db[0], dbN)
            connection_file.truncate(0)
            connection_file.close()
            connection_file = open(file, 'w+')
            connection_file.write(new_content)


                                        # ******************** COMBOBOX Secteurs List ****************
    def mrchName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select marche from marche;")
        values = cur.fetchone()
        return values


                                        # **************SELECT PROVINCE, CERCLE *********************

    def info_marche(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select cercle, province, commune from marche;")
        values = cur.fetchone()
        return values


                                        # **************SELECT PROVINCE, CERCLE *********************

    def selectValues(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select * from marche;")
        values = cur.fetchone()
        return values


                                        # **************SELECT PROVINCE, CERCLE *********************

    def modifyValues(self, march, sect, cercle_fr, cercle_ar, prov_fr, prov_ar, commun_fr, commun_ar, consFon_fr, consFon_ar, geom, bulOff):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'marche'  ;")
        colName = cur.fetchall()
        cur.execute("update marche set "+colName[1][0]+" = '" + march + "', "+colName[2][0]+" = '" + sect + "', "+colName[3][0]+" = '" + cercle_fr + "' , "+colName[4][0]+" = '" + cercle_ar + "', "+colName[5][0]+" = '" + prov_fr + "', "+colName[6][0]+" = '" + prov_ar + "', "+colName[7][0]+" = '" + commun_fr + "', "+colName[8][0]+" = '" + commun_ar + "', "+colName[9][0]+" = '" + consFon_fr + "', "+colName[10][0]+" = '" + consFon_ar + "', "+colName[11][0]+" = '" + geom + "', "+colName[12][0]+" = '" + bulOff + "', "+colName[14][0]+" = '"+str(datetime.now())+"';")
        val = conn.commit()
        return val

    def insert_marche(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("insert into marche(id_marche,marche) values (default ,'marche')")
        conn.commit()


