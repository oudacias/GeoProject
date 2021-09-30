import datetime
import os

import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH):
    from Connection.ConnectionFile import Connection

class Personnes:


            # ***************** LastPoly // update Presume **************
    def addIdPolyg(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("UPDATE personnes SET  id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles), date_modification = '" + str(datetime.datetime.now()) + "' ;")
        conn.commit()

                                                                    # ***************** LastPoly // insert personnes **************
    def insertPerson(self, pnmF, pnmA, nmF, nmA, adrF, adrA, cin, tel, tel2, dtN):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #username = usr.split()

        if(tel == '' or tel == 'None' ):
            tel = 'null'
        if (tel2 == '' or tel2 == 'None'):
            tel2 = 'null'
        if(dtN == '' or dtN == 'None'):
            cur.execute("INSERT INTO personnes (id_personne,prenom_fr,prenom_ar,nom_fr,nom_ar,adresse_fr,adresse_ar,cin,tel,tel2,date_naissance) VALUES "
                "(DEFAULT ,'" + pnmF + "', '" + pnmA + "', '" + nmF + "', '" + nmA + "', '" + adrF + "', '" + adrA + "', '" + cin + "', " + tel + ", " + tel2 + ", null);")
            val2 = conn.commit()
            return val2

        cur.execute("INSERT INTO personnes (id_personne,prenom_fr,prenom_ar,nom_fr,nom_ar,adresse_fr,adresse_ar,cin,tel,tel2,date_naissance) VALUES "
                    "(DEFAULT ,'" + pnmF + "', '" + pnmA + "', '" + nmF + "', '" + nmA + "', '" + adrF + "', '" + adrA + "', '" + cin + "', " + tel+ ", " + tel2+ ", '" + dtN+ "');")
        val = conn.commit()
        return val


                                            # -------------- COMBOBOX // Nom et Prénom de toutes Personnes  ------------
    def personList(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #cur.execute("SELECT nom_fr,prenom_fr FROM personnes")
        cur.execute("SELECT nom_fr,prenom_fr FROM personnes")
        values = cur.fetchall()
        value = []
        for a in range(len(values)):
            value.append(''.join(str(values[a][0]))+ ' '+ ''.join(str(values[a][1])))
        return value


                                            # -------------------SUPPRESSION // Nom et Prénom de présumé ---------------
    def selectNomPrenm(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #cur.execute("SELECT nom_fr,prenom_fr FROM personnes")
        cur.execute("SELECT pr.nom_fr,pr.prenom_fr FROM personnes as pr INNER JOIN cles as cs ON (pr.id_personne = cs.cle_presume) and (cs.cle_polyg = "+idP+")")
        values = cur.fetchall()
        value = []
        for a in range(len(values)):
            value.append(''.join(str(values[a][0]))+ ' '+ ''.join(str(values[a][1])))
        return value



    def selectidP(self, personne):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        nomPrenom = personne.split()
        cur.execute("SELECT id_personne FROM personnes WHERE nom_fr ='" + nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "'")
        val = cur.fetchall()
        return val

    def researPres(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT pr.id_personne,pr.prenom_fr,pr.prenom_ar,pr.nom_fr,pr.nom_ar,pr.adresse_fr,pr.adresse_ar,pr.cin,pr.tel,pr.tel2,pr.date_naissance FROM personnes as pr inner join cles as cs on (pr.id_personne = cs.cle_presume) and (cs.cle_polyg = "+idP+");")
        val = cur.fetchall()
        for a in val:
            return (a)

    def columnName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'personnes'")
        col_name = cur.fetchall()
        return col_name


                                                         # --------------------- Polyg Selected // OPPOSANT -----------------------
    def researOppo(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT pr.id_personne,pr.prenom_fr,pr.prenom_ar,pr.nom_fr,pr.nom_ar,pr.adresse_fr,pr.adresse_ar,pr.cin,pr.tel,pr.tel2,pr.date_naissance FROM personnes as pr inner join cles as cs on (pr.id_personne = cs.cle_opposant) and (cs.cle_polyg = "+idP+") ORDER BY pr.id_personne ASC;")
        reslt = cur.fetchall()
        return reslt

    def selectOppo(self, idP,idPrs):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT pr.id_personne,pr.prenom_fr,pr.prenom_ar,pr.nom_fr,pr.nom_ar,pr.adresse_fr,pr.adresse_ar,pr.cin,pr.tel,pr.tel2,pr.date_naissance FROM personnes as pr inner join cles as cs on (pr.id_personne = cs.cle_opposant) and (cs.cle_polyg = "+idP+") and (cs.cle_opposant = "+str(idPrs)+");")
        reslt = cur.fetchall()
        return reslt


    def researProp(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT pr.id_personne,pr.prenom_fr,pr.prenom_ar,pr.nom_fr,pr.nom_ar,pr.adresse_fr,pr.adresse_ar,pr.cin,pr.tel,pr.tel2,pr.date_naissance FROM personnes as pr inner join cles as cs on (pr.id_personne = cs.cle_personne) and (cs.cle_polyg = "+idP+");")
        reslt = cur.fetchall()
        return reslt

    def selectOpp(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT id_personne,prenom_fr,prenom_ar,nom_fr,nom_ar,adresse_fr,adresse_ar,cin,tel,tel2,date_naissance FROM personnes WHERE id_personne="+idP+";")
        reslt = cur.fetchall()
        return reslt

    def combboxcCIN(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select cin from personnes;")
        values = cur.fetchall()
        value = []
        for a in values:
            value.append(''.join(a))
        return value

                                                                        # ******************** UPDATE Presume ***********************
    def updatPoly(self, fr, ar, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("UPDATE parcelles SET parcelle_fr = '" + fr + "' , parcelle_ar='" + ar + "' WHERE id_parcelle = "+idP+";")
        val = conn.commit()
        return val

    '''
                                                    # ------------------ LAST POLYG // AJOUTER UN OPPOSANT EXISTANT-----------------
        def addOpps(self, personne, cinOpp):
            connection = Connection()
            conn = connection.connect()
            cur = conn.cursor()
            nomPrenom = personne.split()
            values = []
            if personne != '' and cinOpp == '':
                cur.execute("UPDATE personnes SET opposant = 'oui' WHERE nom_fr ='" + nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "';")
                values = conn.commit()
            if personne == '' and cinOpp != '':
                cur.execute("UPDATE personnes SET opposant = 'oui' WHERE cin = '"+cinOpp+"';")
                values = conn.commit()
            return values
    
    
                                                    # ------------------ LAST POLYG // AJOUTER UN PRESUME EXISTANT-----------------
        def addPresm(self, person, cinPrsm):
            connection = Connection()
            conn = connection.connect()
            cur = conn.cursor()
            nomPrenom = person.split()
            values = []
            if person != '' and cinPrsm == '':
                cur.execute("UPDATE personnes SET presume = 'oui' WHERE nom_fr ='" + nomPrenom[0] + "' and prenom_fr ='" + nomPrenom[1] + "';")
                values = conn.commit()
            if person == '' and cinPrsm != '':
                cur.execute("UPDATE personnes SET presume = 'oui' WHERE cin = '"+cinPrsm+"';")
                values = conn.commit()
            return values
    '''

    def updatPres(self, cin):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("UPDATE personnes SET presume = 'oui' WHERE cin = '"+cin+"';")
        val = conn.commit()
        return val

    def modifyPresm(self, telValue, tel2Value, dNaissance, prnm, prnmAr, nm, nmAr, adrss, adrssAr, cin, tel, tel2, dateN, idPerson):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()

        if telValue != '' and tel2Value != '' and dNaissance != '':
            cur.execute("UPDATE personnes SET prenom_fr = '" + prnm + "', prenom_ar = '" + prnmAr + "' , nom_fr = '" + nm + "' , nom_ar = '" + nmAr + "' , adresse_fr = '" + adrss + "' , adresse_ar = '" + adrssAr + "' , cin = '" + cin + "' , tel = " + tel + " , tel2 = " + tel2 + ", date_naissance = '" + dateN + "', date_modification = '" + str(
                    datetime.datetime.now()) + "' WHERE id_personne = " + str(idPerson) + ";")
            updat = conn.commit()
            return updat

        elif telValue != '' and tel2Value == '' and dNaissance == '':
            cur.execute("UPDATE personnes SET prenom_fr = '" + prnm + "', prenom_ar = '" + prnmAr + "' , nom_fr = '" + nm + "' , nom_ar = '" + nmAr + "' , adresse_fr = '" + adrss + "' , adresse_ar = '" + adrssAr + "' , cin = '" + cin + "' , tel = " + tel + " , tel2 = null, date_naissance = null, date_modification = '" + str(datetime.datetime.now()) + "' WHERE id_personne = " + str(idPerson) + ";")
            updat2 = conn.commit()
            return updat2

        elif telValue == '' and tel2Value == '' and dNaissance != '':
            cur.execute("UPDATE personnes SET prenom_fr = '" + prnm + "', prenom_ar = '" + prnmAr + "' , nom_fr = '" + nm + "' , nom_ar = '" + nmAr + "' , adresse_fr = '" + adrss + "' , adresse_ar = '" + adrssAr + "' , cin = '" + cin + "' , tel = null , tel2 = null, date_naissance = '" + dateN + "', date_modification = '" + str(datetime.datetime.now()) + "' WHERE id_personne = " + str(idPerson) + ";")
            updat3 = conn.commit()
            return updat3

        elif telValue != '' and tel2Value == ''and dNaissance != '':
            cur.execute("UPDATE personnes SET prenom_fr = '" + prnm + "', prenom_ar = '" + prnmAr + "' , nom_fr = '" + nm + "' , nom_ar = '" + nmAr + "' , adresse_fr = '" + adrss + "' , adresse_ar = '" + adrssAr + "' , cin = '" + cin + "' , tel =  " + tel + " , tel2 = null , date_naissance = '" + dateN + "', date_modification = '" + str(datetime.datetime.now()) + "' WHERE id_personne = " + str(idPerson) + ";")
            updat4 = conn.commit()
            return updat4

            '''if dNaissance == '':
            cur.execute("UPDATE personnes SET prenom_fr = '" + prnm + "', prenom_ar = '" + prnmAr + "' , nom_fr = '" + nm + "' , nom_ar = '" + nmAr + "' , adresse_fr = '" + adrss + "' , adresse_ar = '" + adrssAr + "' , cin = '" + cin + "' , tel = " + tel + " , tel2 = " + tel2 + ", "
                            "date_naissance = (SELECT ps.date_naissance FROM personnes as ps inner join cles as cs on (ps.id_personne=cs.cle_opposant) where cs.cle_opposant = '"+str(idPerson)+"'), date_modification = '" + str(datetime.datetime.now()) + "' WHERE id_personne = " + str(idPerson) + ";")
            val4 = conn.commit()
            return val4'''



    def modifyOpp(self, dNaissance, prnm, prnmAr, nm, nmAr, adrss, adrssAr, cin, tel, tel2, dateN, idPerson):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        if (tel == '' or tel == 'None'):
            tel = 'null'
        if (tel2 == '' or tel2 == 'None'):
            tel2 = 'null'
        if (dateN == '' or dateN == 'None'):
            dateN = 'null'

        if dNaissance == '':
            cur.execute("SELECT ps.date_naissance FROM personnes as ps inner join cles as cs on (ps.id_personne=cs.cle_opposant) where cs.cle_opposant = "+str(idPerson)+" ")
            datNais = cur.fetchone()
            print(datNais[0])
            cur.execute("UPDATE personnes SET prenom_fr = '" + prnm + "', prenom_ar = '" + prnmAr + "' , nom_fr = '" + nm + "' , nom_ar = '" + nmAr + "' , adresse_fr = '" + adrss + "' , adresse_ar = '" + adrssAr + "' , cin = '" + cin + "' , tel = " + tel + " , tel2 = " + tel2 + ", date_naissance = NULL, date_modification = '" + str(datetime.datetime.now()) + "' WHERE id_personne = " + str(idPerson) + ";")
            val2 = conn.commit()
            return val2

        cur.execute("UPDATE personnes SET prenom_fr = '" + prnm + "', prenom_ar = '" + prnmAr + "' , nom_fr = '" + nm + "' , nom_ar = '" + nmAr + "' , adresse_fr = '" + adrss + "' , adresse_ar = '" + adrssAr + "' , cin = '" + cin + "' , tel = " + tel + " , tel2 = " + tel2 + ", date_naissance = '" + dateN + "', date_modification = '" + str(datetime.datetime.now()) + "' WHERE id_personne = "+str(idPerson)+";")
        val = conn.commit()
        return val


# ---------------------------------------------------- EtatParcellaire // XML // ZN2 // SELECT PRESUME -------------------------------------------
    def prsm_xml(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select pr.id_personne,pr.nom_fr,pr.nom_ar,pr.prenom_fr,pr.prenom_ar,pr.adresse_fr,pr.adresse_ar,pr.cin,pr.tel,pr.tel2,pr.date_naissance from personnes as pr inner join cles as cl on (pr.id_personne =cl.cle_presume) where cl.cle_polyg = "+idP+";")
        prmVal = cur.fetchall()
        return prmVal


# ---------------------------------------------------- EtatParcellaire // XML // SELECT id -------------------------------------------
    def oppos(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select pr.id_personne,pr.nom_fr,pr.nom_ar,pr.prenom_fr,pr.prenom_ar,pr.adresse_fr,pr.adresse_ar,pr.cin,pr.tel,pr.tel2,pr.date_naissance from personnes as pr inner join cles as cl on (pr.id_personne =cl.cle_opposant) where cl.cle_polyg = "+idP+";")
        opposVal = cur.fetchall()
        return opposVal

# ------------------------------ DELETE PERSONNE -------------------------------------
    def delet_Oppo(self, idPerson):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("delete from personnes where id_personne = "+str(idPerson)+";")
        conn.commit()

    def idPerson(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select ps.id_personne from personnes as ps inner join cles as cs on (ps.id_personne = cs.cle_presume) where cs.cle_polyg = " + idP + ";")
        opposVal = cur.fetchone()
        return opposVal


                                                # ------------------- verify person if exist ------------------------
    def verifyPerson(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select COUNT (*) from personnes where id_personne = " + idP + ";")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False

                                                # ------------------- verify person if exist (WITH JOIN) ------------------------
    def verifyPersonne(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select COUNT (*) from personnes as pr inner join cles as cs on (pr.id_personne = cs.cle_presume) and (cs.cle_polyg = "+idP+");")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False

