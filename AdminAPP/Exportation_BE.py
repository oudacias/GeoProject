from datetime import datetime
import os
import sys

sys.path.append(".")

PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection

class Filtrage:
    def filtrage(self, idMin, idMax, datMin, datMax, sz, dr, cin,user , idP):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        result = []
        username = user.split()
        if idMin != '' and idMax == '' and datMin == '' and datMax == '' and sz == '' and dr == '' and user == '' and cin == '' and idP == '':
            cur.execute("SELECT id_parcelle,parcelle_fr,parcelle_ar,id_consistance,id_type_sol,id_type_speculation,num_ordre,mode_faire_valoir,livret_remis_a, requisition,titre,centroïde_x,centroïde_y FROM parcelles WHERE id_parcelle >= " + idMin + " ORDER BY id_parcelle ASC;")
            result = cur.fetchall()

        elif idMin == '' and idMax != '' and datMin == '' and datMax == '' and sz == '' and dr == '' and user == '' and cin == '' and idP == '':
            cur.execute("SELECT id_parcelle,parcelle_fr,parcelle_ar,id_consistance,id_type_sol,id_type_speculation,num_ordre,mode_faire_valoir,livret_remis_a, requisition,titre,surface_hect,surface_ares,surface_cent FROM parcelles WHERE id_parcelle <= " + idMax + " ORDER BY id_parcelle ASC;")
            result = cur.fetchall()

        elif idMin == '' and idMax == '' and datMin != '' and datMax == '' and sz == '' and dr == '' and user == '' and cin == '' and idP == '':
            cur.execute("SELECT id_parcelle,parcelle_fr,parcelle_ar,id_consistance,id_type_sol,id_type_speculation,num_ordre,mode_faire_valoir,livret_remis_a, requisition,titre,surface_hect,surface_ares,surface_cent FROM parcelles WHERE date_creation >= '" + datMin + "' ORDER BY id_parcelle ASC;")
            result = cur.fetchall()

        elif idMin == '' and idMax == '' and datMin == '' and datMax != '' and sz == '' and dr == '' and user == '' and cin == '' and idP == '':
            cur.execute("SELECT id_parcelle,parcelle_fr,parcelle_ar,id_consistance,id_type_sol,id_type_speculation,num_ordre,mode_faire_valoir,livret_remis_a,requisition,titre,surface_hect,surface_ares,surface_cent FROM parcelles WHERE date_creation <= '" + str(datetime.combine(datetime. strptime(datMax, '%d-%m-%Y'), datetime.max.time())) + "' ORDER BY id_parcelle ASC;")
            result = cur.fetchall()

        elif idMin == '' and idMax == '' and datMin != '' and datMax != '' and sz == '' and dr == '' and user == '' and cin == '' and idP == '':
            cur.execute("SELECT id_parcelle,parcelle_fr,parcelle_ar,id_consistance,id_type_sol,id_type_speculation,num_ordre,mode_faire_valoir,livret_remis_a,requisition,titre,surface_hect,surface_ares,surface_cent FROM parcelles WHERE date_creation <= '" + str(datetime.combine(datetime. strptime(datMax, '%d-%m-%Y'), datetime.max.time())) + "' and date_creation >= '" + datMin + "' ORDER BY id_parcelle ASC;")
            result = cur.fetchall()

        elif idMin == '' and idMax == '' and datMin == '' and datMax == '' and sz != '' and dr == '' and user == '' and cin == '' and idP == '':
            cur.execute("SELECT pr.id_parcelle,pr.parcelle_fr,pr.parcelle_ar,pr.id_consistance,pr.id_type_sol,pr.id_type_speculation,pr.num_ordre,pr.mode_faire_valoir,pr.livret_remis_a,requisition,titre,surface_hect,surface_ares,surface_cent from parcelles as pr INNER JOIN douar as d ON ST_Intersects(pr.geom, d.geom) and not ST_Contains(pr.geom, d.geom)  INNER JOIN sous_zone as sz ON ST_Intersects(sz.geom, d.geom) and not ST_Contains(sz.geom, d.geom) where sz.libelle_fr = '" + sz + "' ORDER BY id_parcelle ASC;")
            result = cur.fetchall()

        elif idMin == '' and idMax == '' and datMin == '' and datMax == '' and sz == '' and dr != '' and user == '' and cin == '' and idP == '':
            cur.execute("SELECT pr.id_parcelle,pr.parcelle_fr,pr.parcelle_ar,pr.id_consistance,pr.id_type_sol,pr.id_type_speculation,pr.num_ordre,pr.mode_faire_valoir,pr.livret_remis_a,requisition,titre,surface_hect,surface_ares,surface_cent from parcelles as pr INNER JOIN douar as d ON ST_Intersects(pr.geom, d.geom) and not ST_Contains(pr.geom, d.geom) where d.libelle_fr = '" + dr + "' ORDER BY pr.id_parcelle ASC;")
            result = cur.fetchall()

        elif idMin == '' and idMax == '' and datMin == '' and datMax == '' and sz == '' and dr == '' and user == '' and cin != '' and idP == '':
            cur.execute("SELECT pr.id_parcelle,pr.parcelle_fr,pr.parcelle_ar,pr.id_consistance,pr.id_type_sol,pr.id_type_speculation,pr.num_ordre,pr.mode_faire_valoir,pr.livret_remis_a,requisition,titre,surface_hect,surface_ares,surface_cent from parcelles as pr inner join cles as c on (c.cle_polyg = pr.id_parcelle) inner join personnes as ps on (c.cle_presume = ps.id_personne) where ps.cin = '" + cin + "' ORDER BY id_parcelle ASC;")
            result = cur.fetchall()

        elif idMin == '' and idMax == '' and datMin == '' and datMax == '' and sz == '' and dr == '' and user != '' and cin == '' and idP == '':
            cur.execute("SELECT pr.id_parcelle,pr.parcelle_fr,pr.parcelle_ar,pr.id_consistance,pr.id_type_sol,pr.id_type_speculation,pr.num_ordre,pr.mode_faire_valoir,pr.livret_remis_a,requisition,titre,surface_hect,surface_ares,surface_cent from parcelles as pr inner join utilisateurs as u on (u.id_user = pr.id_utilisateur) where u.nom ='" + username[0] + "' and u.prenom ='" + username[1] + "'  ORDER BY id_parcelle ASC ;")
            result = cur.fetchall()

        elif idMin == '' and idMax == '' and datMin == '' and datMax == '' and sz == '' and dr == '' and user == '' and cin == '' and idP != '':
            cur.execute("SELECT id_parcelle,parcelle_fr,parcelle_ar,id_consistance,id_type_sol,id_type_speculation,num_ordre,mode_faire_valoir, livret_remis_a,requisition,titre,surface_hect,surface_ares,surface_cent FROM parcelles where id_parcelle in (" + idP + ") ;")
            result = cur.fetchall()

        return result
