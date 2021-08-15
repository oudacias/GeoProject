import psycopg2
from tkinter import messagebox 
import sys 
class Connection:
   def __init__(self):
       self.database = 'tt'
       self.user = 'openpg' 
       self.passwprd = 'openpgpwd'
   def connect(self):
       try:
           conn=psycopg2.connect("dbname =ife_project2 user=openpg password=openpgpwd")
           print("done")
           return conn
       except:
           msg = messagebox.showinfo("Erreur", "Base de donnees n'existe pas")
           sys.exit(1)