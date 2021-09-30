from datetime import date
from datetime import datetime
import os
import sys
sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '\\Connection\\ConnectionFile.py'
if os.path.isfile(PATH):
    from Connection.ConnectionFile import Connection

class Parcelle:

                                                                       # ******************** Les noms de colonnes // TREEVIEW***********************
    def columnName(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = 'parcelles' and COLUMN_NAME <> 'id_utilisateur' and COLUMN_NAME <> 'id_brigade' and COLUMN_NAME <> 'date_modification'  and COLUMN_NAME <> 'geom'"
                    " and COLUMN_NAME <> 'num_mapp' and COLUMN_NAME <> 'nbr_points' and COLUMN_NAME <> 'echelle' "
                    "and COLUMN_NAME <> 'centroïde_x' and COLUMN_NAME <> 'centroïde_y' and COLUMN_NAME <> 'correction_lambert' and COLUMN_NAME <> 'surface_corrigee'")
        col_name = cur.fetchall()
        return col_name


                                                                       # ******************** LA LISTE DES PARCELLES // TREEVIEW***********************
    def listsParcelle(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT id_parcelle,parcelle_fr,parcelle_ar,id_consistance,id_type_sol,id_type_speculation,num_ordre,mode_faire_valoir,livret_remis_a,requisition,titre,bornes,surface_hect,surface_ares,surface_cent,date_creation,nbr_points FROM parcelles ORDER BY id_parcelle ASC ;")
        reslt = cur.fetchall()
        return reslt


                                                                       # ******************** SELECT PARCELLE // XML ***********************
    def polyg_xml(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT id_parcelle,parcelle_fr,parcelle_ar,id_consistance,id_type_sol,id_type_speculation,num_ordre,mode_faire_valoir,livret_remis_a,date_creation,requisition,titre,centroïde_x,centroïde_y, nbr_points, surface_hect,surface_ares,surface_cent FROM parcelles where id_parcelle = "+idP+";")
        reslt = cur.fetchall()
        return reslt


                                                                        #******************** LastPolyg // Informations ***********************
    def lastPolyInfo(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT id_parcelle, parcelle_fr, parcelle_ar FROM parcelles where id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles);")
        reslt = cur.fetchall()
        return reslt


                                                                        #******************** VERIFY_LastPolyg ***********************
    def verify_lastPoly(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT count (id_parcelle) FROM parcelles where id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles);")
        reslt = cur.fetchone()
        return reslt


                                                                        # *********************** RESEARCH POLYGONE **************************
    def researchPolyg(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT id_parcelle, parcelle_fr, parcelle_ar, mode_faire_valoir, nbr_points, surface_hect, surface_ares, surface_cent, date_creation FROM parcelles WHERE id_parcelle=" + idP + ";")
        reslt = cur.fetchall()
        for a in reslt:
            return (a)


    def verifyPolyg(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM parcelles WHERE id_parcelle = "+idP+"")
        lgn = cur.fetchone()
        if (lgn[0] == 1):
            return True
        elif (lgn[0] == 0):
            return False


                                                                    # ******************** UPDATE LastPolyg ***********************
    def updateLastPoly(self, fr, ar, cons, sol, spec, fv, livr):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("UPDATE parcelles SET parcelle_fr = '" + fr + "' , parcelle_ar='" + ar + "' , id_consistance = (select id_consistance from consistance where libelle_fr='"+cons+"')"
                                                                                               ", id_type_sol = (select id_type_sol from type_sol where libelle_fr='"+sol+"'), id_type_speculation = (select id_type_speculation from type_speculation where libelle_fr='"+spec+"')"
                                                                                               ", mode_faire_valoir = '"+fv+"', livret_remis_a='"+livr+"'"
                                                                                               ",date_modification = '"+str(datetime.now())+"' WHERE id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles);")
        val = conn.commit()
        return val


                                                                    # ******************** UPDATE LastPolyg ***********************
    def updateLastPol_SECOURS(self, fr, ar, cons, sol, spec, fv, livr, utilisateur):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        username = utilisateur.split()
        cur.execute("UPDATE parcelles SET parcelle_fr = '" + fr + "' , parcelle_ar='" + ar + "' , id_consistance = (select id_consistance from consistance where libelle_fr='"+cons+"')"
                                                                                               ", id_type_sol = (select id_type_sol from type_sol where libelle_fr='"+sol+"'), id_type_speculation = (select id_type_speculation from type_speculation where libelle_fr='"+spec+"')"
                                                                                               ", mode_faire_valoir = '"+fv+"', livret_remis_a='"+livr+"'"
                                                                                               ", id_utilisateur = (select id_user from utilisateurs where nom ='" + username[0] + "' and prenom ='" + username[1] + "')"
                                                                                               ", date_modification = '"+str(datetime.now())+"', id_brigade = (select b.id_brigade from brigades as b inner join utilisateurs as u on (u.id_brigade = b.id_brigade) and (u.nom ='" + username[0] + "' and u.prenom ='" + username[1] + "')) WHERE id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles);")
        val = conn.commit()
        return val



                                                                    # ******************** UPDATE LastPolyg ***********************
    def updateLastPoly2(self, fr, ar, cons, sol, spec, fv, livr, utilisateur):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        username = utilisateur.split()
        cur.execute("UPDATE parcelles SET parcelle_fr = '" + fr + "' , parcelle_ar='" + ar + "' , id_consistance = (select id_consistance from consistance where libelle_fr='"+cons+"') "
                                                                                               ", id_type_sol = (select id_type_sol from type_sol where libelle_fr='"+sol+"')"
                                                                                               ", id_type_speculation = (select id_type_speculation from type_speculation where libelle_fr='"+spec+"')"
                                                                                               ", mode_faire_valoir = '"+fv+"', livret_remis_a='"+livr+"', id_utilisateur = (select id_user from utilisateurs where nom ='" + username[0] + "' and prenom ='" + username[1] + "'), date_modification = '"+str(datetime.now())+"' WHERE id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles);")
        val = conn.commit()
        return val



                                                                        # ******************** UPDATE Polyg ***********************
    def updatPoly(self, fr, ar, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("UPDATE parcelles SET parcelle_fr = '" + fr + "' , parcelle_ar='" + ar + "' WHERE id_parcelle = "+idP+";")
        val = conn.commit()
        return val

                                                                    # ************************* MODIFIER ID_CONSISTANCE
    def modify_const(self, const, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("UPDATE parcelles SET id_consistance = (select id_consistance from consistance where libelle_fr='" + const + "') where id_parcelle ="+idP+";")
        val = conn.commit()
        return val


                                                                    # ************************* MODIFIER ID_TYPE SOL
    def modify_Tpsol(self, sol, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("UPDATE parcelles SET id_type_sol = (select id_type_sol from type_sol where libelle_fr='" + sol + "') where id_parcelle ="+idP+";")
        val = conn.commit()
        return val


                                                                    # ************************* MODIFIER ID_SPECULATION
    def modify_specul(self, specul, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("UPDATE parcelles SET id_type_speculation = (select id_type_speculation from type_speculation where libelle_fr='" + specul + "') where id_parcelle ="+idP+";")
        val = conn.commit()
        return val


                                                                                # ******************** DELETE POLYG ***********************
    def delete(self, idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("delete from parcelles where id_parcelle = "+str(idP)+";")
        conn.commit()


                                                                                # ******************** COMBOBOX ID_PARCELLE ***********************
    def combboxID(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT id_parcelle FROM parcelles ORDER BY id_parcelle ASC;")
        valeurs = cur.fetchall()
        return valeurs

                                                                                # ******************** COMBOBOX ID_UTILISATEUR ***********************
    def combboxUSR(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT id_utilisateur FROM parcelles ORDER BY id_utilisateur ASC;")
        valeurs = cur.fetchall()
        return valeurs

    def xslTest(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT  id_parcelle, parcelle_fr, parcelle_ar FROM parcelles ")
        valeurs = cur.fetchall()
        return valeurs

    def lignesNumb(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM parcelles")
        lgn = cur.fetchone()
        return lgn


                                                    # ******************** select listParcelles // DAT ***********************
    def idsPolyg(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #cur.execute("select id_parcelle from  parcelles where id_parcelle = "+idP+";")
        cur.execute("select id_parcelle from  parcelles  ORDER by id_parcelle ASC ")
        values = cur.fetchall()
        return values



                                                    # ******************** select listParcelles // DAT ***********************
    def idParcel(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        #cur.execute("select id_parcelle from  parcelles where id_parcelle = "+idP+";")
        cur.execute("select id_parcelle from  parcelles ")
        values = cur.fetchall()
        return values



                                                    # ******************** select listParcelles // DAT ***********************
    def selectAll(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("select * from  parcelles ORDER BY id_parcelle ASC;")
        values = cur.fetchall()
        return values

                                                                      # ******************** LA LISTE DES PARCELLES // TREEVIEW***********************
    def listsParcelles(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("SELECT id_parcelle,parcelle_fr,parcelle_ar,id_consistance,id_type_sol,id_type_speculation,num_ordre,mode_faire_valoir,livret_remis_a,date_creation,requisition,titre,centroïde_x,centroïde_y,surface,num_ordre FROM parcelles ORDER BY id_parcelle ASC ;")
        reslt = cur.fetchall()
        return reslt

















'''
                                                                                # ******************** ADD ID PRESUME ********************
    def addIdPers(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO parcelles id_personne VALUES id_personne = (SELECT MAX(id_personne)FROM personnes where presume = 'oui') WHERE id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles);")
        conn.commit()


                                                                                # ******************** ADD ID OPPOSANT ***********************
    def addIdOppo(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO parcelles id_personne VALUES id_personne = (SELECT MAX(id_personne)FROM personnes where opposant = 'oui') WHERE id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles);")
        conn.commit()


                                                                                # ******************** ADD ID PROP ***********************
    def addIdProp(self):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO parcelles (id_personne) VALUES (id_personne = (SELECT MAX(id_personne))FROM personnes where proprietaire = 'oui') WHERE id_parcelle = (SELECT MAX(id_parcelle)FROM parcelles);")
        conn.commit()


    '''



