import datetime
import os

PATH = os.path.abspath(os.curdir) +'/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class Cles:


                                            # ------------------- LAST POLYG // ADD NEW PRÉSUMÉ ------------------------
    def insertPres(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO cles (id_cle,cle_polyg,cle_presume) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT MAX (id_personne) FROM personnes));")
        conn.commit()


                                            # ------------------- LAST POLYG // ADD NEW OPPOSANT -----------------------
    def insertOpp(self, tpopp):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO cles (id_cle,cle_polyg,cle_opposant,id_type_opposition, date_creation) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT MAX (id_personne) FROM personnes), (SELECT id_type_opposition FROM type_opposition WHERE libelle_fr='"+str(tpopp)+"'), '" + str(datetime.datetime.now()) + "');")
        conn.commit()



                                            # ------------------- MODIFY POLYG // ADD NEW OPPOSANT -----------------------
    def insertNew_CleOppo(self, tpopp, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO cles (id_cle,cle_polyg,cle_opposant,id_type_opposition, date_creation) VALUES (DEFAULT , "+idP+", (SELECT MAX (id_personne) FROM personnes), (SELECT id_type_opposition FROM type_opposition WHERE libelle_fr='"+str(tpopp)+"'), '" + str(datetime.datetime.now()) + "');")
        conn.commit()


                                                # ----------------LAST POLYG /**/ PRÉSUMÉ / OPPOSANT -------------------
    def addPres(self, personne, cinPrs):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()

        nomPrenom = personne.split()
        if personne != '':
            cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_personne) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE (nom_fr ='" +nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "')));")
            value = conn.commit()
        else:
            cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_personne) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE cin ='" + cinPrs + "'));")
            value = conn.commit()
        return value

    def addProp(self, personne):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        nomPrenom = personne.split()
        cur.execute(
            "INSERT INTO cles (id_cle,cle_polyg,cle_personne) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE nom_fr ='" +
            nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "'));")
        conn.commit()


    def oppNP(self, personne):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        nomPrenom = personne.split()
        cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_personne) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE (nom_fr ='" +nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "')));")
        value = conn.commit()
        return value

    def oppCin(self, cinOpp):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_personne) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE cin = '" + cinOpp + "'));")
        value = conn.commit()
        return value

        '''nomPrenom = personne.split()
        cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_personne) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE (nom_fr ='" + nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "') or (cin = '" + cinOpp + "')));")
        value = conn.commit()
        return value'''


    def addPersonCle(self, person, cinPrsm):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        nomPrenom = person.split()
        value = []
        if person != '' and cinPrsm == '':
            cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_presume) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE nom_fr ='" + nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "'));")
            value = conn.commit()
        elif person == '' and cinPrsm != '':
            cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_presume) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE cin ='" + cinPrsm + "'));")
            value = conn.commit()
        return value


    def addOpposCle(self, person, cinPrsm):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        nomPrenom = person.split()
        value = []
        if person != '' and cinPrsm == '':
            cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_opposant) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE nom_fr ='" + nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "'));")
            value = conn.commit()
        elif person == '' and cinPrsm != '':
            cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_opposant) VALUES (DEFAULT , (SELECT MAX (id_parcelle) FROM parcelles), (SELECT id_personne FROM personnes WHERE cin ='" + cinPrsm + "'));")
            value = conn.commit()
        return value



    def add_NewOpposCle(self, person, cinPrsm, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        nomPrenom = person.split()
        value = []
        if person != '' and cinPrsm == '':
            cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_opposant) VALUES (DEFAULT , "+idP+", (SELECT id_personne FROM personnes WHERE nom_fr ='" + nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "'));")
            value = conn.commit()
        elif person == '' and cinPrsm != '':
            cur.execute("INSERT INTO cles (id_cle, cle_polyg, cle_opposant) VALUES (DEFAULT , "+idP+", (SELECT id_personne FROM personnes WHERE cin ='" + cinPrsm + "'));")
            value = conn.commit()
        return value


                                                                                # ******************** DELETE POLYG ***********************
    def delete(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("delete from cles where cle_polyg = "+str(idP)+";")
        conn.commit()


    def updatcles(self, tpopp, person, cinPrsm):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        nomPrenom = person.split()
        value = []
        if person != '' and cinPrsm == '':
            cur.execute("UPDATE cles set id_type_opposition = (SELECT id_type_opposition FROM type_opposition WHERE libelle_fr='"+str(tpopp)+"') where cle_polyg=(SELECT MAX (id_parcelle) FROM parcelles) and cle_opposant = (SELECT id_personne FROM personnes WHERE nom_fr ='" + nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "');")
            value = conn.commit()
        elif person == '' and cinPrsm != '':
            cur.execute("UPDATE cles set id_type_opposition = (SELECT id_type_opposition FROM type_opposition WHERE libelle_fr='" + str(tpopp) + "') where cle_polyg=(SELECT MAX (id_parcelle) FROM parcelles) and cle_opposant = (SELECT id_personne FROM personnes WHERE cin ='" + cinPrsm + "');")
            value = conn.commit()
        return value


    def updat_NewCleOppos(self, tpopp, person, cinPrsm, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        nomPrenom = person.split()
        value = []
        if person != '' and cinPrsm == '':
            cur.execute("UPDATE cles set id_type_opposition = (SELECT id_type_opposition FROM type_opposition WHERE libelle_fr='"+str(tpopp)+"') where cle_polyg="+idP+" and cle_opposant = (SELECT id_personne FROM personnes WHERE nom_fr ='" + nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "');")
            value = conn.commit()
        elif person == '' and cinPrsm != '':
            cur.execute("UPDATE cles set id_type_opposition = (SELECT id_type_opposition FROM type_opposition WHERE libelle_fr='" + str(tpopp) + "') where cle_polyg="+idP+" and cle_opposant = (SELECT id_personne FROM personnes WHERE cin ='" + cinPrsm + "');")
            value = conn.commit()
        return value


    def opposition_pieces(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select COUNT (cle_opposant) from cles where cle_polyg = "+idP+";")
        val = cur.fetchall()
        for v in val:
            return v

    def updat_ClesOppos(self, motif, idOpp, idP ):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        if motif == '':
            cur.execute("UPDATE cles set id_type_opposition = (SELECT id_type_opposition FROM cles WHERE cle_polyg = " + idP + " and cle_opposant= '"+str(idOpp)+"'), date_modification = '" + str(datetime.datetime.now()) + "' where cle_polyg=" + idP + " and cle_opposant = '"+str(idOpp)+"';")
            value2 = conn.commit()
            return value2

        cur.execute("UPDATE cles set id_type_opposition = (SELECT id_type_opposition FROM type_opposition WHERE libelle_fr='"+str(motif)+"'), date_modification = '" + str(datetime.datetime.now()) + "' where cle_polyg="+idP+" and cle_opposant = '"+str(idOpp)+"';")
        value = conn.commit()
        return value

                                                    # -------------------- SUPPRIMER CLE_OPPOSANT ---------------------
    def delet_CleOppo(self, idP, idOpp):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM cles where cle_polyg = "+idP+" and cle_opposant = "+str(idOpp)+" ;")
        value = conn.commit()
        return value

    def cleOppos(self, idOpp):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #cur.execute("select cs.cle_opposant from cles as cs inner join personnes as ps on (ps.id_personne = cs.cle_opposant) where cs.cle_polyg = " + idP + ";")
        cur.execute("select cle_opposant from cles where cle_opposant = " + str(idOpp) + ";")
        opposVal = cur.fetchone()
        return opposVal


    def clePres(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #cur.execute("select cs.cle_opposant from cles as cs inner join personnes as ps on (ps.id_personne = cs.cle_opposant) where cs.cle_polyg = " + idP + ";")
        cur.execute("select cle_presume from cles;")
        presumVal = cur.fetchall()
        return presumVal
