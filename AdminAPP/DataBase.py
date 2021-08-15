import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
from Connection import Connection
from tkinter import messagebox
import re


class Database:
    def createdb(self, username, dbname, password, epsg):
        try:
            conn = psycopg2.connect("user="+username+" password=" + password + " dbname ='postgres'")
            cur = conn.cursor()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            if(epsg.isdigit()):
                try:
                    if (re.match("^[A-Za-z0-9_-]*$", dbname) and bool(re.search(r"\s", dbname)) == False):
                        cur.execute("create database " + dbname + "")
                        print(dbname)
                        connection = Connection.Connection.create_connection_file(username, dbname, password)
                        P = self.createPostgis(username, dbname, password, epsg)
                    else:
                        msg = messagebox.showinfo("Erreur", "Nom de base de donnees est invalide")
                        return False
                except Exception as err:
                    print(err)
                    msg = messagebox.showinfo("Erreur", "Base de donnees existe deja")
                    return False
            else:
                msg = messagebox.showinfo("Erreur", "Veuillez ajouter EPSG")
                return False
        except:
            msg = messagebox.showinfo("Erreur", "Nom ou mot de passe incorrect")
            return False
        return True

    def createPostgis(self, username, dbname, password, epsg):
        conn = psycopg2.connect("dbname=" + dbname + " user="+username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE EXTENSION postgis")
        conn.commit()

        self.marche(username, dbname, password)
        self.zone(username, dbname, password)
        self.ssZone(username, dbname, password)
        self.douar(username, dbname, password)
        self.consist(username, dbname, password)
        self.insertConsist(username, dbname, password)
        self.typeSol(username, dbname, password)
        self.insertTpSol(username, dbname, password)
        self.typeSpec(username, dbname, password)
        self.insertTpSpec(username, dbname, password)
        self.typeOppos(username, dbname, password)
        self.insertTpOppos(username, dbname, password)
        self.brgd(username, dbname, password)
        self.usr(username, dbname, password)
        self.polygs(username, dbname, password, epsg)
        self.perso(username, dbname, password)
        self.cles(username, dbname, password)
        self.rivrains(username, dbname, password)
        #self.intervalle(username, dbname, password)
        self.pnts(username, dbname, password)
        self.shynch(username, dbname, password)
        self.machines(username, dbname, password)
        #self.check_intervalle(username, dbname, password)
        #self.insert_Interv(username, dbname, password)
        self.insertBrigd(username, dbname, password)
        self.insertuUsr(username, dbname, password)

        # self.tplimite(username, dbname, password)
        # self.descPoint(username, dbname, password)
        # self.insertDescrp(username, dbname, password)
        # self.insertLimit(username, dbname, password)
        self.addBorne(username, dbname, password)
        self.addLimit(username, dbname, password)
        self.direction(username, dbname, password)

        self.calcul_surface(username, dbname, password)
        self.calcul_centroid(username, dbname, password)
        self.calcul_coordinates(username, dbname, password)

    def marche(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE marche (id_marche SERIAL NOT NULL , "
                    "marche VARCHAR(80) DEFAULT (''),"
                    "secteur VARCHAR (60) DEFAULT (''),"
                    "cercle VARCHAR (60) DEFAULT (''), الدائرة VARCHAR (60) DEFAULT (''),"
                    "province VARCHAR (60) DEFAULT (''), الاقليم VARCHAR (60) DEFAULT (''),"
                    "commune VARCHAR (60) DEFAULT (''), الجماعة VARCHAR (60) DEFAULT (''),"
                    "conservation_fonciere VARCHAR (80) DEFAULT (''), المحافظةالعقارية VARCHAR (80) DEFAULT (''),"
                    "bulletin_off VARCHAR (50) DEFAULT (''),"
                    "geometre VARCHAR (50) DEFAULT (''),"
                    "date DATE DEFAULT NULL ,"
                    "date_modification DATE DEFAULT NULL , "
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_marche_PK PRIMARY KEY (id_marche));")
        conn.commit()

    def zone(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE zone "
                    "(id_zone SERIAL NOT NULL,"
                    "libelle VARCHAR (40) DEFAULT (''),"
                    "geom GEOMETRY (MultiPolygon,26191),"
                    "date_modification DATE , "
                    "date_creation TIMESTAMP DEFAULT now() ,"
                    "CONSTRAINT  id_zone_pk PRIMARY KEY (id_zone));")
        conn.commit()

    def ssZone(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE sous_zone "
                    "(id_sousZone SERIAL NOT NULL,"
                    "libelle_fr VARCHAR(60) DEFAULT (''),"
                    "geom GEOMETRY (MultiPolygon,26191),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_sousZone_PK PRIMARY KEY (id_sousZone));")
        conn.commit()

    def douar(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE douar"
                    "(id_douar SERIAL NOT NULL,"
                    "libelle_fr VARCHAR(40) DEFAULT (''),"
                    "libelle_ar VARCHAR(40) DEFAULT (''),"
                    "geom GEOMETRY(MultiPolygon,26191),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_douar_PK PRIMARY KEY (id_douar));")
        conn.commit()

    def consist(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE consistance (id_consistance SERIAL NOT NULL , "
                    "libelle_fr VARCHAR(40) DEFAULT (''),"
                    "libelle_ar VARCHAR(40) DEFAULT (''), "
                    "abreviation VARCHAR (10) DEFAULT (''),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT id_consistance_pk PRIMARY KEY (id_consistance));")
        conn.commit()

    def insertConsist(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("INSERT INTO consistance (id_consistance,libelle_fr,libelle_ar,abreviation) VALUES "
                    "(100 , '', '', ''),"
                    "(DEFAULT, 'Terrain de Culture', 'أرض فلاحية', 'TC'),"
                    "(DEFAULT, 'Terrain Implanté', 'أرض مغروسة', 'TP'),"
                    "(DEFAULT, 'Terrain nu', 'أرض عارية', 'TN'),"
                    "(DEFAULT, 'Terrain Bâti', 'ارض بها بنايات', 'TB');")
        conn.commit()

    def typeSol(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE type_sol (id_type_sol SERIAL NOT NULL , "
                    "libelle_fr VARCHAR(40) DEFAULT (''),"
                    "libelle_ar VARCHAR(40) DEFAULT (''), "
                    "abreviation VARCHAR (10) DEFAULT (''),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT id_typeSol_pk PRIMARY KEY (id_type_sol));")
        conn.commit()

    def insertTpSol(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("INSERT INTO type_sol (id_type_sol,libelle_fr,libelle_ar,abreviation) VALUES "
                    "(100 , '', '', ''),"
                    "(DEFAULT , 'R’mel','رمل', 'RML'),"
                    "(DEFAULT , 'Hamri','حمري', 'HAM'),"
                    "(DEFAULT , 'Tirs','ترس', 'TIR'),"
                    "(DEFAULT , 'Dehs','دحس', 'DEH'),"
                    "(DEFAULT , 'Beida','بيضا', 'BIA');")
        conn.commit()

    def typeSpec(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE type_speculation (id_type_speculation SERIAL NOT NULL , "
                    "libelle_fr VARCHAR(40) DEFAULT (''),"
                    "libelle_ar VARCHAR(40) DEFAULT (''),"
                    "abreviation VARCHAR (10) DEFAULT (''),"
                    "date_modification DATE, "
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT id_typeSpeculation_pk PRIMARY KEY (id_type_speculation));")
        conn.commit()

    def insertTpSpec(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("INSERT INTO type_speculation (id_type_speculation,libelle_fr,libelle_ar,abreviation) VALUES "
                    "(DEFAULT , 'Culture Traditionnelle', '', 'TR'),"
                    "(DEFAULT , 'Culture Industrielle', '', 'IN'),"
                    "(DEFAULT , 'Culture Maraichère-potagère', '', 'MA'),"
                    "(100 , '', '', '');")
        conn.commit()

    def typeOppos(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE type_opposition (id_type_opposition SERIAL NOT NULL , "
                    "libelle_fr VARCHAR(40) DEFAULT (''),"
                    "libelle_ar VARCHAR(40) DEFAULT (''),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_typeOppost_PK PRIMARY KEY (id_type_opposition));")
        conn.commit()

    def insertTpOppos(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("INSERT INTO type_opposition (id_type_opposition,libelle_fr,libelle_ar,date_creation) VALUES "
                    "(DEFAULT , 'Totale', 'كامل', '" + str(datetime.datetime.now()) + "' ),"
                                                                                      "(DEFAULT , 'partielle', 'جزئي', '" + str(
            datetime.datetime.now()) + "' ),"
                                       "(DEFAULT , 'réciproque', 'متبادل', '" + str(datetime.datetime.now()) + "' ),"
                                                                                                               "(DEFAULT , 'd office', 'إداري', '" + str(
            datetime.datetime.now()) + "' ),"
                                       "(DEFAULT , 'droits indivi', 'حقوق شخصية', '" + str(
            datetime.datetime.now()) + "');")
        conn.commit()

    def perso(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE personnes "
                    "(id_personne SERIAL NOT NULL,"
                    "nom_fr VARCHAR(100) DEFAULT (''),"
                    "nom_ar VARCHAR(100) DEFAULT (''),"
                    "prenom_fr VARCHAR (80) DEFAULT (''),"
                    "prenom_ar VARCHAR (80) DEFAULT (''),"
                    "adresse_fr VARCHAR (200) DEFAULT (''),"
                    "adresse_ar VARCHAR (200) DEFAULT (''),"
                    "cin VARCHAR (10) DEFAULT (''),"
                    "tel NUMERIC (20) DEFAULT NULL ,"
                    "tel2 NUMERIC (20) DEFAULT NULL ,"
                    "date_naissance DATE DEFAULT NULL ,"
                    "id_brigade INTEGER, "
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_personne_pk PRIMARY KEY (id_personne));")
        conn.commit()

    def usr(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE utilisateurs (id_user SERIAL NOT NULL , "
                    "id_brigade INTEGER ,"
                    "nom VARCHAR(100) DEFAULT (''),"
                    "prenom VARCHAR (80) DEFAULT (''),"
                    "admin VARCHAR (5) DEFAULT (''),"
                    "password VARCHAR (100) DEFAULT (''),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_user_PK PRIMARY KEY (id_user));")
        conn.commit()

    def insertuUsr(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("INSERT INTO utilisateurs (id_user,id_brigade,nom,prenom,admin,password,date_creation) VALUES "
                    "(DEFAULT, 1 , 'admin', 'admin', 'oui', 123, '" + str(datetime.datetime.now()) + "');")
        conn.commit()

    def brgd(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE brigades (id_brigade SERIAL NOT NULL , "
                    "brigade_fr VARCHAR(60) DEFAULT (''),"
                    "brigade_ar VARCHAR(60) DEFAULT (''), "
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT id_brigade_pk PRIMARY KEY (id_brigade));")
        conn.commit()

    def insertBrigd(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("INSERT INTO brigades (id_brigade,brigade_fr,brigade_ar,date_creation) VALUES "
                    "(DEFAULT, 'Brigade 1', 'الفرقة 1', '" + str(datetime.datetime.now()) + "');")
        conn.commit()

    def rivrains(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE rivrains "
                    "(id_rivrain SERIAL NOT NULL,"
                    "id_parcelle INTEGER,"
                    "id_parcelle_rivrain INTEGER,"
                    "direction VARCHAR (30) DEFAULT (''),"
                    "point_debut INTEGER ,"
                    "point_fin INTEGER ,"
                    "bornes_rivrain VARCHAR (30) DEFAULT (''),"
                    "geom geometry ,"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now());")
        conn.commit()

    def tplimite(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE type_limite "
                    "(id_type_limite SERIAL NOT NULL,"
                    "type_limite_fr VARCHAR(150) DEFAULT (''),"
                    "abreviation VARCHAR (20) DEFAULT (''),"
                    "date_modification DATE ,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT id_type_limite_pk PRIMARY KEY (id_type_limite));")
        conn.commit()

    def insertLimit(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("INSERT INTO type_limite (id_type_limite,type_limite_fr,date_creation) VALUES "
                    "(DEFAULT , 'Limite rectiligne en T.C', '" + str(datetime.datetime.now()) + "'),"
                                                                                                "(DEFAULT , 'Limite naturelle suivant le bord d’une piste de largeur variable', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’un sentier', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’un sentier publique', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’un oued', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’un chaabat', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’un khandak', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’un route', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’un route goudronnée', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’une seguia cimentée', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’une seguia cimentée', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Limite naturelle suivant le bord d’une seguia en terre', '" + str(
            datetime.datetime.now()) + "');")
        conn.commit()

    def polygs(self, username, dbname, password, epsg):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE parcelles "
                    "(id_parcelle SERIAL NOT NULL,"
                    "parcelle_fr VARCHAR(60) DEFAULT (''),"
                    "parcelle_ar VARCHAR(60) DEFAULT (''),"
                    "id_consistance INTEGER DEFAULT 100,"
                    "id_type_sol INTEGER DEFAULT 100,"
                    "id_type_speculation INTEGER DEFAULT 100,"
                    "num_ordre INTEGER,"
                    "mode_faire_valoir VARCHAR(5) DEFAULT (''),"
                    "livret_remis_a VARCHAR(20) DEFAULT (''),"
                    "id_utilisateur INTEGER,"
                    "date_modification DATE,"
                    "geom geometry(Polygon," + epsg + "),"
                    "requisition VARCHAR(20) DEFAULT (''),"
                    "titre VARCHAR(20) DEFAULT (''),"
                    "bornes VARCHAR(130) DEFAULT (''),"
                    "nbr_points VARCHAR(80) DEFAULT (''),"
                    "num_mapp VARCHAR(15) DEFAULT (''),"
                    "echelle VARCHAR(15) DEFAULT (''),"
                    "centroïde_x double precision,"
                    "centroïde_y double precision,"
                    "surface_hect double PRECISION,"
                    "surface_ares double PRECISION,"
                    "surface_cent double PRECISION,"
                    "correction_lambert double precision ,"
                    "surface_corrigee double precision,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_parcelle_PK PRIMARY KEY (id_parcelle),"
                    "CONSTRAINT id_consistance_fk FOREIGN KEY (id_consistance) REFERENCES consistance(id_consistance) ON UPDATE CASCADE,"
                    "CONSTRAINT id_type_sol_fk FOREIGN KEY (id_type_sol) REFERENCES type_sol(id_type_sol) ON UPDATE CASCADE,"
                    "CONSTRAINT id_type_speculation_fk FOREIGN KEY (id_type_speculation) REFERENCES type_speculation(id_type_speculation) ON UPDATE CASCADE);")
        conn.commit()

    def cles(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE cles "
                    "(id_cle SERIAL NOT NULL,"
                    "cle_polyg INTEGER ,"
                    "cle_presume INTEGER,"
                    "cle_opposant INTEGER, "
                    "id_type_opposition INTEGER, "
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_cle_PK PRIMARY KEY (id_cle),"
                    "CONSTRAINT cle_polyg_Fk FOREIGN KEY (cle_polyg) REFERENCES parcelles(id_parcelle) ON UPDATE CASCADE,"
                    "CONSTRAINT id_type_opposition_Fk FOREIGN KEY (id_type_opposition) REFERENCES type_opposition(id_type_opposition) ON UPDATE CASCADE, "
                    "CONSTRAINT cle_presume_Fk FOREIGN KEY (cle_presume) REFERENCES personnes(id_personne) ON UPDATE CASCADE, "
                    "CONSTRAINT cle_opposant_Fk FOREIGN KEY (cle_opposant) REFERENCES personnes(id_personne) ON UPDATE CASCADE );")
        conn.commit()

    def descPoint(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE description_point"
                    "(id_description SERIAL NOT NULL,"
                    "description_fr VARCHAR (150) DEFAULT (''),"
                    "description_ar VARCHAR (150) DEFAULT (''),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT id_description_PK1 PRIMARY KEY (id_description));")
        conn.commit()

    def insertDescrp(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("INSERT INTO description_point (id_description,description_fr,date_creation) VALUES "
                    "(DEFAULT , 'Marqué sur un rocher', '" + str(datetime.datetime.now()) + "'),"
                                                                                            "(DEFAULT , 'Marqué sur un mur de construction', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée en T.C', '" + str(datetime.datetime.now()) + "'),"
                                                                                                         "(DEFAULT , 'Marqué sur un pilier', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’une piste de largeur variable', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’un sentier', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’un sentier publique', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’un oued', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’une chaabat', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’un khandak', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’une route', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’une route goudronnée', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’une seguia cimentée', '" + str(
            datetime.datetime.now()) + "'),"
                                       "(DEFAULT , 'Plantée au bord d’une seguia en terre', '" + str(
            datetime.datetime.now()) + "');")
        conn.commit()

    def pnts(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE points"
                    "(id_point SERIAL NOT NULL,"
                    "type_point VARCHAR(6) DEFAULT (''),"
                    "num_point VARCHAR (100) DEFAULT (''),"
                    "description_point VARCHAR(100) DEFAULT (''), "
                    "X_approx double precision,"
                    "Y_approx double precision,"
                    "X_def double precision,"
                    "Y_def double precision,"
                    "geom GEOMETRY (POINT,26191),"
                    "reference VARCHAR (100) DEFAULT (''),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_point_PK PRIMARY KEY (id_point) );")
        # "CONSTRAINT id_descrp_Fk FOREIGN KEY (id_descrp) REFERENCES description_point(id_description) );")
        conn.commit()

    def intervalle(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE intervalle"
                    "(id_intervalle SERIAL NOT NULL,"
                    "id_brigade INTEGER,"
                    "intervalle_debut INTEGER,"
                    "intervalle_fin INTEGER,"
                    "nom_table VARCHAR (30),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_intarv_PK PRIMARY KEY (id_intervalle),"
                    "CONSTRAINT id_brigade_Fk FOREIGN KEY (id_brigade) REFERENCES brigades(id_brigade) ON UPDATE CASCADE );")
        conn.commit()

    def shynch(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE synchronisation "
                    "(id_synchr SERIAL NOT NULL,"
                    "adresse_ip INTEGER,"
                    "sent BOOLEAN,"
                    "received BOOLEAN,"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(), "
                    "CONSTRAINT  id_synchr_PK PRIMARY KEY (id_synchr) );")
        conn.commit()

    def machines(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("CREATE TABLE machines "
                    "(id_machine SERIAL NOT NULL,"
                    "nom_machine VARCHAR (40) NOT NULL ,"
                    "adresse_ip VARCHAR (20) NOT NULL ,"
                    "port INTEGER DEFAULT (9099),"
                    "type VARCHAR (20) DEFAULT (''),"
                    "date_modification DATE,"
                    "date_creation TIMESTAMP DEFAULT now(),"
                    "CONSTRAINT  id_machine_PK PRIMARY KEY (id_machine))")
        conn.commit()

    # insert_intervalle
    def insert_Interv(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute(""" CREATE FUNCTION public.insert_intervalle() 
                        RETURNS trigger
                        LANGUAGE 'plpgsql'

                     AS $BODY$ 
                     DECLARE 
                             num_row numeric(10); 
                             current_intervalle_personne numeric(100); 
                             current_intervalle_parcelle numeric(100); 
                             current_intervalle_point numeric(100); 
                             end_intervalle numeric(60); 
                             id_current_brigade numeric(15); 
                    BEGIN 
                          select id_brigade into id_current_brigade from brigades order by id_brigade desc limit 1;
                          select into num_row count(*) from intervalle;
                        if num_row = 0 
                            then 
		                        insert into intervalle(id_brigade,intervalle_debut,intervalle_fin,nom_table) values (id_current_brigade,1,5,'parcelles');
                                insert into intervalle(id_brigade,intervalle_debut,intervalle_fin,nom_table) values (id_current_brigade,1,20,'points');
                                insert into intervalle(id_brigade,intervalle_debut,intervalle_fin,nom_table) values (id_current_brigade,1,15,'personnes');
                        end if; 
                        if num_row > 0 
                            then 
                                select intervalle_fin into current_intervalle_parcelle from intervalle where nom_table ='parcelles' order by id_intervalle desc limit 1;
                                select intervalle_fin into current_intervalle_personne from intervalle where nom_table ='personnes' order by id_intervalle desc limit 1;
                                select intervalle_fin into current_intervalle_point from intervalle where nom_table ='points' order by id_intervalle desc limit 1;
                                insert into intervalle(id_brigade,intervalle_debut,intervalle_fin,nom_table) values (id_current_brigade,current_intervalle_parcelle + 1,current_intervalle_parcelle +5,'parcelles');
                                insert into intervalle(id_brigade,intervalle_debut,intervalle_fin,nom_table) values (id_current_brigade,current_intervalle_point + 1,current_intervalle_point +20,'points');
                                insert into intervalle(id_brigade,intervalle_debut,intervalle_fin,nom_table) values (id_current_brigade,current_intervalle_personne + 1,current_intervalle_personne +15,'personnes');
                        end if; 
                        return NULL; 
                    END;
                    $BODY$;

                    CREATE TRIGGER insert_intervalle
                    After INSERT ON brigades
                    FOR EACH ROW EXECUTE PROCEDURE insert_intervalle();""")
        conn.commit()

    # check_intervalle
    def check_intervalle(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("""CREATE FUNCTION public.check_intervalle()
                        RETURNS trigger
                        LANGUAGE 'plpgsql'
                        VOLATILE
                        COST 100
                    AS $BODY$
                    DECLARE 
                        id_brigades numeric;
                        start_intervalle numeric(60);
                        end_intervalle numeric(60);
                        count_brigade numeric(25);
                        created timestamp;
                        count_brigade_intervalle numeric(100);
                        arg TEXT;
                        current_intervalle numeric;
                        id_p numeric;


                    BEGIN

                    FOREACH arg IN ARRAY TG_ARGV LOOP
                        if arg = 'parcelles' then
                            select max(id_parcelle) into count_brigade from parcelles where id_brigade = new.id_brigade;
                            select intervalle_debut,intervalle_fin into start_intervalle,end_intervalle from intervalle where id_brigade = new.id_brigade and nom_table = 'parcelles';
                            if(count_brigade IS NULL) then
                                new.id_parcelle := start_intervalle;
                            elseif(count_brigade + 1 <= end_intervalle) then
                                new.id_parcelle := count_brigade + 1;
                            elseif (count_brigade + 1 > end_intervalle) then
                            raise notice '%', count_brigade;
                            raise notice '%', end_intervalle;
                                select intervalle_fin into current_intervalle from intervalle where nom_table='parcelles' and intervalle_fin = (select intervalle_fin from intervalle where nom_table='parcelles' order by intervalle_fin desc limit 1 );
                                update intervalle set intervalle_debut =current_intervalle, intervalle_fin = current_intervalle +5, date_modification = today_day  where id_brigade = new.id_brigade and nom_table = 'parcelles';
                                new.id_parcelle :=  current_intervalle +1;
                            end if;

                        elseif arg = 'points' then
                            select max(id_point) into count_brigade from points where id_brigade = new.id_brigade;
                            select intervalle_debut,intervalle_fin into start_intervalle,end_intervalle from intervalle where id_brigade = new.id_brigade and nom_table = 'points';
                            if(count_brigade IS NULL) then
                                new.id_point := start_intervalle;
                            elseif(count_brigade + 1 <= end_intervalle) then
                                new.id_point := count_brigade + 1;
                            elseif (count_brigade + 1 > end_intervalle) then
                                select intervalle_fin into current_intervalle from intervalle where nom_table='points' and intervalle_fin = (select intervalle_fin from intervalle where nom_table='points' order by intervalle_fin desc limit 1 );
                                update intervalle set intervalle_debut =current_intervalle, intervalle_fin = current_intervalle +5, date_modification = today_day  where id_brigade = new.id_brigade and nom_table = 'points';
                                new.id_point :=  current_intervalle +1;
                            end if;
                            new.x_approx := ST_X(new.geom);
                            new.y_approx := ST_Y(new.geom);


                        elseif arg = 'personnes' then
                        select max(id_personne) into count_brigade from personnes where id_brigade = new.id_brigade;
                            select intervalle_debut,intervalle_fin into start_intervalle,end_intervalle from intervalle where id_brigade = new.id_brigade and nom_table = 'personnes';
                            if(count_brigade IS NULL) then
                                new.id_personne := start_intervalle;
                            elseif(count_brigade + 1 <= end_intervalle) then
                                new.id_personne := count_brigade + 1;
                            elseif (count_brigade + 1 > end_intervalle) then
                            raise notice '%', count_brigade;
                            raise notice '%', end_intervalle;
                                select intervalle_fin into current_intervalle from intervalle where nom_table='personnes' and intervalle_fin = (select intervalle_fin from intervalle where nom_table='personnes' order by intervalle_fin desc limit 1 );
                                update intervalle set intervalle_debut =current_intervalle, intervalle_fin = current_intervalle +5, date_modification = today_day  where id_brigade = new.id_brigade and nom_table = 'personnes';
                                new.id_personne :=  current_intervalle +1;
                            end if;
                        end if;
                    end loop;
                    RETURN NEW;
                    END;
                    $BODY$;
                    DROP TRIGGER IF EXISTS check_intervalle
                      ON parcelles;
                    CREATE TRIGGER check_intervalle
                      before Insert
                      ON parcelles
                      FOR EACH ROW
                      EXECUTE PROCEDURE check_intervalle('parcelles');
                    DROP TRIGGER IF EXISTS check_intervalle
                      ON points;
                    CREATE TRIGGER check_intervalle
                      before Insert
                      ON points
                      FOR EACH ROW
                      EXECUTE PROCEDURE check_intervalle('points');
                    DROP TRIGGER IF EXISTS check_intervalle
                      ON personnes;
                    CREATE TRIGGER check_intervalle
                      before Insert
                      ON personnes
                      FOR EACH ROW
                      EXECUTE PROCEDURE check_intervalle('personnes');""")
        conn.commit()

    # Add Limites
    def addLimit(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("""CREATE FUNCTION public.add_limite()
                        RETURNS trigger 
                        LANGUAGE 'plpgsql' 
                        COST 100 
                        VOLATILE NOT LEAKPROOF 
                     AS $BODY$
                     DECLARE 
                        DECLARE 
                            poly_join record;
                            ids_limites RECORD;
                            limites record;
                            limites1 record;
                            borne_dd numeric;
                            borne_ff numeric;
                            id_limites varchar(250);
                            id_limites1 varchar(250);
                            direction_c varchar(30);
                            direction_i varchar(30);
                            num_rows numeric;
                        BEGIN
                            FOR poly_join IN SELECT distinct(p3.id_parcelle)
                            FROM parcelles p1,parcelles p3,points p2 where p1.id_parcelle =new.id_parcelle
                            and ST_Distance(p1.geom,p2.geom) = 0 and ST_Distance(p3.geom,p2.geom) = 0 and p1.id_parcelle<>p3.id_parcelle
                            LOOP
                            id_limites = '';
                            id_limites1 = '';
                            SELECT p2.id_point into borne_dd
                            FROM parcelles p1,parcelles p3,points p2 where (p1.id_parcelle =new.id_parcelle
                            and ST_Distance(p1.geom,p2.geom) = 0 and ST_Distance(p3.geom,p2.geom) = 0 and p1.id_parcelle<>p3.id_parcelle
                            and p3.id_parcelle = poly_join.id_parcelle)
                            order by p3.geom,p2.geom limit 1;
                             SELECT p2.id_point into borne_ff
                            FROM parcelles p1,parcelles p3,points p2 where (p1.id_parcelle =new.id_parcelle
                            and ST_Distance(p1.geom,p2.geom) = 0 and ST_Distance(p3.geom,p2.geom) = 0 and p1.id_parcelle<>p3.id_parcelle) and p3.id_parcelle = poly_join.id_parcelle order by p3.geom,p2.geom desc limit 1;
                            SELECT
                            ST_Direction(ST_Azimuth(ST_Centroid(p1.geom),ST_Centroid(p2.geom ))),ST_Direction(ST_Azimuth(ST_Centroid(p2.geom),ST_Centroid(p1.geom ))) into direction_c , direction_i
                            FROM parcelles p1,parcelles p2
                            where p1.id_parcelle = new.id_parcelle and p2.id_parcelle = poly_join.id_parcelle;
                            FOR limites IN SELECT p2.id_point 
                            FROM parcelles p1,parcelles p3,points p2 where p1.id_parcelle =new.id_parcelle
                            and ST_Distance(p1.geom,p2.geom) = 0 and ST_Distance(p3.geom,p2.geom) = 0 and p1.id_parcelle<>p3.id_parcelle
                            and p3.id_parcelle = poly_join.id_parcelle order by p3.geom,p2.geom
                            LOOP
                              id_limites = concat(id_limites,limites);
                            END LOOP;

                            FOR limites1 IN SELECT p2.id_point 
                            FROM parcelles p1,parcelles p3,points p2 where p1.id_parcelle =new.id_parcelle
                            and ST_Distance(p1.geom,p2.geom) = 0 and ST_Distance(p3.geom,p2.geom) = 0 and p1.id_parcelle<>p3.id_parcelle
                            and p3.id_parcelle = poly_join.id_parcelle order by p3.geom,p2.geom desc
                            LOOP
                              id_limites1 = concat(id_limites1,limites1);
                            END LOOP;

                                id_limites = replace(trim(id_limites,'()'),')(','==>');
                                id_limites1 = replace(trim(id_limites1,'()'),')(','==>');

                                insert into rivrains (id_rivrain,point_debut,point_fin,bornes_rivrain,direction,id_parcelle,id_parcelle_rivrain) values (default,borne_dd,borne_ff,id_limites,direction_c,new.id_parcelle,poly_join.id_parcelle);
                                insert into rivrains (id_rivrain,point_debut,point_fin,bornes_rivrain,direction,id_parcelle,id_parcelle_rivrain) values (default,borne_ff,borne_dd,id_limites1,direction_i,poly_join.id_parcelle,new.id_parcelle);  
                            END LOOP;
                            return NULL;
                        END;
                    $BODY$;

                    ALTER FUNCTION public.add_limite()
                        OWNER TO """+username+""";
                       drop trigger if exists add_limite
                        on parcelles;
                        create trigger add_limite
                        after INSERT on parcelles for each ROW
                        execute procedure add_limite();""")
        conn.commit()

    # Add Bornes
    def addBorne(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("""CREATE or replace FUNCTION public.add_borne()
                        RETURNS trigger 
                        LANGUAGE 'plpgsql' 
                        COST 100 
                        VOLATILE NOT LEAKPROOF 
                     AS $BODY$
                     DECLARE 
                        ids numeric;
                        ed varchar(1200);
                        linestring_text varchar(5000);
                        point_text RECORD;
                        num_rows numeric;
                        tmp_point_count numeric;
                    BEGIN
                        ed = '';
                        tmp_point_count = 0;
                        SELECT ST_AsEWKT(ST_ExteriorRing(new.geom)) into linestring_text;
                        FOR point_text in SELECT ST_AsText(
                        ST_PointN(column1,generate_series(1, ST_NPoints(column1)))) FROM ( VALUES (linestring_text::geometry) ) AS foo
                        LOOP
                            select id_point into ids from points where ST_AsText(geom) = point_text.ST_AsText;
                            raise notice '%',ids;
                            ed = concat(ed,ids,'=>');
                            tmp_point_count = tmp_point_count+1;
                        END LOOP;		
                            update parcelles set bornes = left(ed,length(ed)-2) where id_parcelle = new.id_parcelle;
                            update parcelles set nbr_points = tmp_point_count -1  where id_parcelle = new.id_parcelle;
                        return NULL;
                    END;
                    $BODY$;

                    ALTER FUNCTION public.add_borne()
                        OWNER TO """+username+""";
                        drop trigger if exists add_borne on parcelles;
                        create trigger add_borne after INSERT 
                        on parcelles for each ROW
                        execute PROCEDURE  add_borne();""")
        conn.commit()

    def direction(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("""CREATE OR REPLACE FUNCTION ST_Direction(azimuth float8) RETURNS character varying AS
                        $BODY$SELECT CASE
                          WHEN $1 < 0.0 THEN 'less than 0'
                          WHEN degrees($1) < 22.5 THEN 'Nord'
                          WHEN degrees($1) < 67.5 THEN 'Nord Est'
                          WHEN degrees($1) < 112.5 THEN 'Est'
                          WHEN degrees($1) < 157.5 THEN 'Sud Est'
                          WHEN degrees($1) < 202.5 THEN 'Sud'
                          WHEN degrees($1) < 247.5 THEN 'Sud Ouest'
                          WHEN degrees($1) < 292.5 THEN 'Ouest' 
                          WHEN degrees($1) < 292.5 THEN 'Ouest'
                          WHEN degrees($1) < 337.5 THEN 'Nord Ouest'
                          WHEN degrees($1) <= 360.0 THEN 'Nord'
                        END;$BODY$ LANGUAGE sql IMMUTABLE COST 100;
                        COMMENT ON FUNCTION ST_Direction(float8) IS 'Hello';""")
        conn.commit()

    def calcul_surface(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("""CREATE OR REPLACE FUNCTION public.calcul_area()
                        RETURNS trigger
                        LANGUAGE 'plpgsql'
                        VOLATILE
                        COST 100
                    AS $BODY$
                    DECLARE   
                    BEGIN
                        new.surface_hect := ST_Area(new.geom) * 0.0001;
                        new.surface_cent := ST_Area(new.geom) * 0.0247;
                        new.surface_ares := ST_Area(new.geom) * 0.01; 

                    RETURN NEW;
                    END;
                    $BODY$;

                    DROP TRIGGER IF EXISTS calcul_area ON parcelles;
                    CREATE TRIGGER calcul_area before Insert
                    ON parcelles FOR EACH ROW
                    EXECUTE PROCEDURE calcul_area();""")
        conn.commit()

    def calcul_centroid(self,username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username+" password=" + password + "")
        cur = conn.cursor()
        cur.execute("""CREATE OR REPLACE FUNCTION public.calcul_centroid()
                        RETURNS trigger
                        LANGUAGE 'plpgsql'
                        VOLATILE
                        COST 100
                    AS $BODY$
                    DECLARE   
                    BEGIN
                        new.centroïde_x := ST_X(ST_Centroid(new.geom));
                        new.centroïde_y := ST_Y(ST_Centroid(new.geom));
                    RETURN NEW;
                    END;
                    $BODY$;

                    DROP TRIGGER IF EXISTS calcul_centroid ON parcelles;
                    CREATE TRIGGER calcul_centroid before Insert
                    ON parcelles FOR EACH ROW
                    EXECUTE PROCEDURE calcul_centroid();""")
        conn.commit()
    def calcul_coordinates(self, username, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user=" + username + " password=" + password + "")
        cur = conn.cursor()
        cur.execute("""CREATE OR REPLACE FUNCTION public.calcul_coordinates()
                RETURNS trigger
                LANGUAGE 'plpgsql'
                VOLATILE
                COST 100
            AS $BODY$
            DECLARE 
                        
            BEGIN
                new.x_approx := ST_X(new.geom);
                new.y_approx := ST_Y(new.geom);
            
            RETURN NEW;
            END;
            $BODY$;
            DROP TRIGGER IF EXISTS calcul_coordinates
              ON points;
            CREATE TRIGGER calcul_coordinates
              before Insert
              ON points
              FOR EACH ROW
              EXECUTE PROCEDURE calcul_coordinates();""")
        conn.commit()





