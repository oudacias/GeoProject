import psycopg2
import datetime

conn = psycopg2.connect("dbname =ife_project2 user=postgres password=123 port =5433")
cur = conn.cursor()
cur.execute("select count(*) from information_schema.columns where table_name= 'points';")

nbr_column = cur.fetchone()
print(nbr_column)
cur.execute("INSERT INTO points VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", [100, 'P', '', 'Marqué sur un rocher', None, None, None, None, None, '01010000204F660000465BEFC40CC92B41D12AB2CF65634AC1', '', None, datetime.datetime(2021, 7, 28, 17, 26, 42, 757405)])








