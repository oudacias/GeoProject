from UserAPP import Parcelle_BE
from AdminAPP import Point_BE
import os
class Dat_Polygs():

    def dat_file(self):



        filename = 'Toutes_les_parcelles.dat'
        if (os.path.isdir(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\\IFE_PIECES\\DAT')) == False):
            os.makedirs(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\\IFE_PIECES\\DAT', filename), mode=0o777)
        filepath = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\\IFE_PIECES\\DAT', filename)
        os.chmod(os.path.abspath(os.curdir), mode=0o777)
        print(os.path.abspath(os.curdir))

        fichier = open(filepath, "w")

        polyg = Parcelle_BE.Parcelle()
        pntCount = Point_BE.Point_BE()
        listPolyg = polyg.selectAll()
        nbrPnt = polyg.listsParcelle()
        for v in range(len(listPolyg)):
            point = pntCount.numPt(str(listPolyg[v][0]))
            xy = pntCount.coord_XY(str(listPolyg[v][0]))
            mappe = str(listPolyg[v][16])
            fichier.write(str(listPolyg[v][0]))
            fichier.write('\n')
            fichier.write('IFE\n')
            fichier.write('mappe** \n')
            fichier.write(str(nbrPnt[v][16]) + '\n')
            for n in range(len(point)):
                fichier.write(str(xy[n]).replace("(", "").replace(",", "").replace(")", "") + "\n")
            fichier.write("\n"+"\n")
        fichier.close()



m = Dat_Polygs()
m.dat_file()