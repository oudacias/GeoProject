import os


class Connection():

    def create_connection_file(username, database, password):

        PATH = os.path.abspath(os.curdir) + '\\Connection\\ConnectionFile.py'


        f = open(PATH, "w")
        f.write("import psycopg2\n")
        f.write("from tkinter import messagebox \n")
        f.write("import sys \n")


        f.write("class Connection:\n")

        f.write("   def __init__(self):\n")
        f.write("       self.database = '" + database + "'\n")
        f.write("       self.user = '"+username+"' \n")
        f.write("       self.passwprd = '" + password + "'\n")

        f.write("   def connect(self):\n")
        f.write("       try:\n")
        f.write('           conn=psycopg2.connect("dbname =' + database + ' user='+username+' password=' + password + '")\n')
        f.write('           print("done")\n')
        f.write("           return conn\n")
        f.write("       except:\n")
        f.write("""           msg = messagebox.showinfo("Erreur", "Base de donnees n'existe pas")\n""")
        f.write("""           sys.exit(1)""")


        f.close()

