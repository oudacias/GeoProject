import psycopg2
from tkinter import messagebox 
import sys 
class Connection:
   def __init__(self):
       self.database = 'ife_project2'
       self.user = 'postgres'
       self.passwprd = '123'
   def connect(self):
       try:
           conn=psycopg2.connect("dbname =ife_project2 user=postgres password=123 port =5433")
           print("done")
           return conn
       except:
           msg = messagebox.showinfo("Erreur", "Base de donnees n'existe pas")
           sys.exit(1)
