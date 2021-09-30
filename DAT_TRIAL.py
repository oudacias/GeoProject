# insert_intervalle
def insert_Interv(self, dbname, password):
    conn = psycopg2.connect("dbname=" + dbname + " user='postgres' password=" + password + "")
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
def check_intervalle(self, dbname, password):
    conn = psycopg2.connect("dbname=" + dbname + " user='postgres' password=" + password + "")
    cur = conn.cursor()
    cur.execute("""CREATE FUNCTION public.check_intervalle()
                        RETURNS trigger 
                        LANGUAGE 'plpgsql' 
                        COST 100 
                        VOLATILE NOT LEAKPROOF 
                     AS $BODY$
                     DECLARE 
                                id_brigades numeric(10);
                                start_intervalle numeric(60);
                                end_intervalle numeric(60);
                                count_brigade numeric(25);
                                created timestamp;
                                count_brigade_intervalle numeric(100);
                                arg TEXT;
                                id_insert numeric(100);
                    BEGIN
                    FOREACH arg IN ARRAY TG_ARGV LOOP
                    if arg = 'parcelles' then 
                         select id_brigade,id_parcelle into id_brigades,id_insert from parcelles order by date_creation desc limit 1;
                         select count(*) into count_brigade from parcelles where id_brigade = id_brigades;
		                 select intervalle_debut,intervalle_fin into start_intervalle,end_intervalle from intervalle where id_brigade = id_brigades and nom_table = 'parcelle'; 
                         case
                         when count_brigade = 1
                            then
                            update parcelles set id_parcelle = start_intervalle where id_parcelle = id_insert;
                        else
				                select count(*) into count_brigade_intervalle from parcelles where id_brigade = id_brigades and id_parcelle between start_intervalle and end_intervalle;
                            case 
                                when start_intervalle + count_brigade_intervalle + 1 > end_intervalle
                                then
                                    select count(*) into count_brigade from brigades;
					                update intervalle set intervalle_debut = start_intervalle + count_brigade *5 , intervalle_fin = end_intervalle + count_brigade *5  where id_brigade = id_brigades and nom_table = 'parcelles';
					                update parcelles set id_parcelle = start_intervalle + count_brigade_intervalle where id_parcelle = id_insert;
                                else 
					                update parcelles set id_parcelle = start_intervalle + count_brigade_intervalle  where id_parcelle = id_insert;
                            end case;
                        end case;
                        elseif arg = 'points' then
                        select id_brigade,id_point into id_brigades,id_insert from points order by date_creation desc limit 1;
                        select count(*) into count_brigade from points where id_brigade = id_brigades;
                        select intervalle_debut,intervalle_fin into start_intervalle,end_intervalle from intervalle where id_brigade = id_brigades and nom_table = 'points'; 
                        case
                        when count_brigade = 1
                            then 
                            update points set id_point = start_intervalle where id_point = id_insert; 
                        else 
                                select count(*) into count_brigade_intervalle from points where id_brigade = id_brigades and id_point between start_intervalle and end_intervalle;
                            case
                                when start_intervalle + count_brigade_intervalle + 1 > end_intervalle
                                then
                                    select count(*) into count_brigade from brigades;
                                    update intervalle set intervalle_debut = start_intervalle + count_brigade *5 , intervalle_fin = end_intervalle + count_brigade *5  where id_brigade = id_brigades and nom_table = 'points';
                                    update points set id_point = start_intervalle + count_brigade_intervalle where id_point = id_insert;
                                else
                                    update points set id_point = start_intervalle + count_brigade_intervalle  where id_point = id_insert;
                            end case;
                        end case;
                        elseif arg = 'personnes' then
                        select id_brigade,date_creation into id_brigades,created from personnes order by date_creation desc limit 1;
                        select count(*) into count_brigade from personnes where id_brigade = id_brigades;
                         select intervalle_debut,intervalle_fin into start_intervalle,end_intervalle from intervalle where id_brigade = id_brigades and nom_table = 'personnes'; 
                        case
                        when count_brigade = 1
                            then 
                            update personnes set id_personne = start_intervalle where date_creation = created; 
                        else 
                                select count(*) into count_brigade_intervalle from personnes where id_brigade = id_brigades and id_personne between start_intervalle and end_intervalle;
                            case
                                when start_intervalle + count_brigade_intervalle + 1 > end_intervalle
                                then
                                    select count(*) into count_brigade from brigades;
                                    update intervalle set intervalle_debut = start_intervalle + count_brigade *5 , intervalle_fin = end_intervalle + count_brigade *5  where id_brigade = id_brigades and nom_table = 'parcelles';
                                    update personnes set id_personne = start_intervalle + count_brigade_intervalle where date_creation = created;
                                else
                                    update personnes set id_personne = start_intervalle + count_brigade_intervalle  where date_creation = created;
                            end case;
                        end case;
                        end if;
                        end loop;
                            return NULL;

                    END;
                    $BODY$;
                    ALTER FUNCTION public.check_intervalle() OWNER TO postgres;

                    CREATE TRIGGER check_intervalle_parcelle
                    AFTER INSERT
                    ON public.parcelles
                    FOR EACH ROW
                    EXECUTE PROCEDURE public.check_intervalle('parcelles');


                    CREATE TRIGGER check_intervalle_personne
                    AFTER INSERT
                    ON public.personnes
                    FOR EACH ROW
                    EXECUTE PROCEDURE public.check_intervalle('personnes');


                    CREATE TRIGGER check_intervalle_point
                    AFTER INSERT
                    ON public.points
                    FOR EACH ROW
                    EXECUTE PROCEDURE public.check_intervalle('points');""")
    conn.commit()

    # Add Bornes
    def addBorne(self, dbname, password):
        conn = psycopg2.connect("dbname=" + dbname + " user='postgres' password=" + password + "")
        cur = conn.cursor()
        cur.execute("""CREATE FUNCTION public.add_borne()
                        RETURNS trigger 
                        LANGUAGE 'plpgsql' 
                        COST 100 
                        VOLATILE NOT LEAKPROOF 
                     AS $BODY$
                     DECLARE 
                        last_polys record;
                        ids RECORD;
                        ed varchar(1200);
                        num_rows numeric;
                    BEGIN
                    SELECT count(id_parcelle) into num_rows from parcelles where date_creation > (select max(date_creation) from parcelles where EXTRACT(minute FROM (date_creation)) <  EXTRACT(minute FROM (select max(date_creation) from parcelles)) - 1);
                    case
                    when num_rows>0 then
                        FOR last_polys IN SELECT id_parcelle from parcelles where date_creation > (select max(date_creation) from parcelles where EXTRACT(minute FROM (date_creation)) <  EXTRACT(minute FROM (select max(date_creation) from parcelles)) - 1) 
                        loop
                        ed = '';
                            FOR ids IN SELECT points.id_point 
                            FROM parcelles INNER JOIN points
                            ON ST_Intersects(parcelles.geom, points.geom) and not ST_Contains(parcelles.geom, points.geom)
                             where parcelles.id_parcelle = last_polys.id_parcelle
                            LOOP
                                    ed = concat(ed,ids);
                            END LOOP;
                                 ed = replace(trim(ed,'()'),')(','==>');
                                 update parcelles set bornes = ed where id_parcelle = last_polys.id_parcelle;
                        end loop;
                    else

                        FOR last_polys IN SELECT id_parcelle from parcelles 
                        loop
                        ed = '';
                            FOR ids IN SELECT points.id_point 
                            FROM parcelles INNER JOIN points
                            ON ST_Intersects(parcelles.geom, points.geom) and not ST_Contains(parcelles.geom, points.geom)
                             where parcelles.id_parcelle = last_polys.id_parcelle
                            LOOP
                                    ed = concat(ed,ids);
                            END LOOP;
                                   ed = replace(trim(ed,'()'),')(','==>');
                                   update parcelles set bornes = ed where id_parcelle = last_polys.id_parcelle;
                            end loop;
                    end case;
                        return NULL;
                    END;
                    $BODY$;

                    ALTER FUNCTION public.add_borne()
                        OWNER TO postgres;
                        drop trigger if exists add_borne on parcelles;
                        create trigger add_borne after INSERT 
                        on parcelles for each ROW
                        execute PROCEDURE  add_borne();""")
        conn.commit()
