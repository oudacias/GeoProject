import tkinter as tk
from tkinter import *
import sys
import os
from AdminAPP import MainAdmin
from UserAPP import MainUser



class Bienvenu:
    def bien_venu(self):

        file1 = open("../AdminAPP/MyFile.txt", "r")
        nom = file1.read()
        print(nom)


        if(nom == 'Admin'):
            print("trial")
            os.system("python ../AdminApp/MainAdmin.py")
            '''mAd = MainAdmin.MainAdmin()
            mAd.mainloop()'''
        elif(nom == 'User'):
            mUsr = MainUser.MainUser()
            mUsr.mainloop()


if __name__ == "__main__":
    b = Bienvenu()
    b.bien_venu()


