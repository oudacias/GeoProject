from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from UserAPP import Douar_BE
from UserAPP import Parcelle_BE
from AdminAPP import Point_BE
from UserAPP import Personnes_BE
from AdminAPP import Rivrain_BE
from UserAPP import Consistance_BE
from UserAPP import TypeSpecl_BE
from UserAPP import TypeSol_BE
import os
from tkinter import messagebox

class Export_Xml():
    def xmlFile(self):
        values = Parcelle_BE.Parcelle.selectAll(self)
        top_xml = Element('parcelles')

# -- PARCELLE --
        tab = ['numParcelle', 'nomParcelleAR', 'nomParcelleFR', 'nombreBorne', 'surfCalculer', 'surfAdopter', 'surfaceHA', 'surfaceA', 'surfaceCA', 'adresseFR', 'adresseAR',
               'idSynchronisation', 'idDouar', 'fournisseurDonnee', 'idEnqueteurP', 'idEnqueteurJ', 'idValidateur', 'numeroOrdre', 'numero', 'Bornes', 'OppositionOpposants']
        polyg = Parcelle_BE.Parcelle.listsParcelle(self)

        for value in range(len(values)):
            middle_xml = SubElement(top_xml, 'parcelle')
            dr = Douar_BE.Douar.xmlDr(self, str(polyg[value][0]))
            riv = Rivrain_BE.Rivrains.rivXml(self, str(polyg[value][0]))
            prsm = Personnes_BE.Personnes.prsm_xml(self, str(polyg[value][0]))
            pnt = Point_BE.Point_BE.numPt(self, str(polyg[value][0]))
            cnst = Consistance_BE.Consistance.Const_xml(self, str(polyg[value][0]))
            sol = TypeSol_BE.TypeSol.sol_xml(self, str(polyg[value][0]))
            specl = TypeSpecl_BE.TypeSpecul.spec_xml(self, str(polyg[value][0]))

            for j in range(len(tab)):
                sub = SubElement(middle_xml, tab[j])
                if tab[j] == 'numParcelle':
                    sub.text = str(polyg[value][0])
                if tab[j] == 'nomParcelleAR':
                    sub.text = str(polyg[value][2])
                if tab[j] == 'nomParcelleFR':
                    sub.text = str(polyg[value][1])
                if tab[j] == 'nombreBorne':
                    sub.text = str(polyg[value][16])
                if tab[j] == 'surfCalculer':
                    sub.text = '0'
                if tab[j] == 'surfAdopter':
                    sub.text = '0'
                if tab[j] == 'surfaceHA':
                    if polyg[value][12] == None:
                        sub.text = '0'
                    else:
                        sub.text = str(polyg[value][12])
                if tab[j] == 'surfaceA':
                    if polyg[value][13] == None:
                        sub.text = '0'
                    else:
                        sub.text = str(polyg[value][13])
                if tab[j] == 'surfaceCA':
                    if polyg[value][14] == None:
                        sub.text = '0'
                    else:
                        sub.text = str(polyg[value][14])
                if tab[j] == 'adresseFR':
                    sub.text = str(dr[0][1])
                if tab[j] == 'adresseAR':
                    sub.text = str(dr[0][2])
                if tab[j] == 'idSynchronisation':
                    sub.text = '0'
                if tab[j] == 'idDouar':
                    sub.text = str(dr[0][0])
                if tab[j] == 'idEnqueteurP':
                    sub.text = '0'
                if tab[j] == 'idEnqueteurJ':
                    sub.text = '0'
                if tab[j] == 'idValidateur':
                    sub.text = '0'
                if tab[j] == 'numeroOrdre':
                    if polyg[value][6] == None:
                        sub.text = '0'
                    else:
                        sub.text = str(polyg[value][6])
                if tab[j] == 'numero':
                    sub.text = '0'
                if tab[j] == 'Bornes ':
                    sub.text = ''
                if tab[j] == 'OppositionOpposants ':
                    sub.text = ''


# -- Rivrain --
            rivrn = ['description', 'Direction', 'Id_douar', 'Id_Riverain', 'num_parcelle', 'pointDebutName', 'pointFinName', 'Type_Riverain', 'Adresse', 'CIN', 'Nom', 'Prenom', 'GSM ']
            pntDF = ['id_douar', 'name', 'num_parcelle', 'type']
            if polyg != '':
                sub = SubElement(middle_xml, 'Rivrains')
                subelmt = SubElement(sub, 'RiverainPersonnePhysiques')
                for r in range(len(riv)):
                    drRiv = Douar_BE.Douar.drRivPolyg(self, str(riv[r][1]))
                    numPointD = Point_BE.Point_BE.numPoint(self, str(riv[r][3]))
                    numPointF = Point_BE.Point_BE.numPoint(self, str(riv[r][4]))
                    drPointD = Douar_BE.Douar.drRiv(self, str(riv[r][3]))
                    drPointF = Douar_BE.Douar.drRiv(self, str(riv[r][4]))

                    prsmRiv = Personnes_BE.Personnes.prsm_xml(self, str(riv[r][1]))
                    subelmt2 = SubElement(subelmt, 'RiverainPersonnePhysiques')
                    for rv in range(len(rivrn)):
                        subelmt3 = SubElement(subelmt2, rivrn[rv])
                        if rivrn[rv] == 'description':
                            subelmt3.text = ''
                        if rivrn[rv] == 'Direction':
                            subelmt3.text = str(riv[r][2])
                        if rivrn[rv] == 'Id_douar':
                            subelmt3.text = str(drRiv[0])
                        if rivrn[rv] == 'Id_Riverain':
                            subelmt3.text = str(riv[r][1])
                        if rivrn[rv] == 'num_parcelle ':
                            subelmt3.text = ' '
                        if rivrn[rv] == 'pointDebutName':
                            subelmt3.text = numPointD[0]
                        if rivrn[rv] == 'pointFinName':
                            subelmt3.text = numPointF[0]
                        if rivrn[rv] == 'Type_Riverain':
                            subelmt3.text = 'Personne Physique'
                        if rivrn[rv] == 'Adresse':
                            subelmt3.text = prsmRiv[0][5]
                        if rivrn[rv] == 'CIN':
                            subelmt3.text = prsmRiv[0][7]
                        if rivrn[rv] == 'Nom':
                            subelmt3.text = prsmRiv[0][1]
                        if rivrn[rv] == 'Prenom':
                            subelmt3.text = prsmRiv[0][3]
                        if rivrn[rv] == 'GSM':
                            subelmt3.text = prsmRiv[0][8]
                    pntD = SubElement(subelmt2, 'pointDebut')
                    pntF = SubElement(subelmt2, 'pointFin')
                    for p in range(len(pntDF)):
                        subelmt4 = SubElement(pntD, pntDF[p])
                        subelmt5 = SubElement(pntF, pntDF[p])
                        if pntDF[p] == 'id_douar':
                            subelmt4.text = drPointD[0]
                            subelmt5.text = drPointF[0]
                        if pntDF[p] == 'name':
                            subelmt4.text = numPointD[0]
                            subelmt5.text = numPointF[0]
                        if pntDF[p] == 'num_parcelle':
                            subelmt4.text = ''
                            subelmt5.text = ''
                        if pntDF[p] == 'type':
                            subelmt4.text = 'Personne Physique'
                            subelmt5.text = 'Personne Physique'

# -- Presume --
            prsTab = ['adresse', 'cin', 'nomAR', 'nomFR', 'nomPere', 'nomPereAR', 'prenomAR', 'prenomFR', 'tel']
            prs = SubElement(middle_xml, 'presumeParcelles')
            subPrs = SubElement(prs, 'presumeParcelle')
            subPrsm = SubElement(subPrs, 'presume')

            for pr in range(len(prsTab)):
                prsSubElmnt = SubElement(subPrsm, prsTab[pr])
                if prsTab[pr] == 'adresse':
                    prsSubElmnt.text = str(prsm[0][5])
                if prsTab[pr] == 'cin':
                    prsSubElmnt.text = str(prsm[0][7])
                if prsTab[pr] == 'nomAR':
                    prsSubElmnt.text = str(prsm[0][2])
                if prsTab[pr] == 'nomFR':
                    prsSubElmnt.text = str(prsm[0][1])
                if prsTab[pr] == 'nomPere':
                    prsSubElmnt.text = ''
                if prsTab[pr] == 'nomPereAR':
                    prsSubElmnt.text = ''
                if prsTab[pr] == 'prenomAR':
                    prsSubElmnt.text = str(prsm[0][4])
                if prsTab[pr] == 'prenomFR':
                    prsSubElmnt.text = str(prsm[0][3])
                if prsTab[pr] == 'tel':
                    prsSubElmnt.text = str(prsm[0][8])

# -- parcelaire --
            prcTab = ['idDouar', 'nombreBorne', 'numParcelle', 'surfAdopter', 'surfCalculer', 'surfaceA', 'surfaceCA', 'surfaceHA', 'gId']
            pnts = ['id_douar', 'name', 'num_parcelle', 'partie', 'type']
            coord = ['x', 'y', 'z']
            prcel = SubElement(middle_xml, 'parcelaire')
            for pc in range(len(prcTab)):
                prcelSub = SubElement(prcel, prcTab[pc])
                if prcTab[pc] == 'idDouar':
                    prcelSub.text = str(dr[0][0])
                if prcTab[pc] == 'nombreBorne':
                    prcelSub.text = str(polyg[value][16])
                if prcTab[pc] == 'numParcelle':
                    prcelSub.text = str(polyg[value][0])
                if prcTab[pc] == 'surfAdopter':
                    prcelSub.text = '0'
                if prcTab[pc] == 'surfCalculer':
                    prcelSub.text = '0'
                if prcTab[pc] == 'surfaceA':
                    if polyg[value][13] == None:
                        prcelSub.text = '0'
                    else:
                        prcelSub.text = str(polyg[value][13])
                if prcTab[pc] == 'surfaceCA':
                    if polyg[value][14] == None:
                        prcelSub.text = '0'
                    else:
                        prcelSub.text = str(polyg[value][14])
                if prcTab[pc] == 'surfaceHA':
                    if polyg[value][12] == None:
                        prcelSub.text = '0'
                    else:
                        prcelSub.text = str(polyg[value][12])
                if prcTab[pc] == 'gId':
                    prcelSub.text = '0'
            pntPrcs = SubElement(prcel, 'pointParcellaires')
            for n in range(len(pnt)):
                parceValues = Point_BE.Point_BE.numPoint(self, str(pnt[n][0]))
                drPntParce = Douar_BE.Douar.drRiv(self, str(pnt[n][0]))
                pntPrc = SubElement(pntPrcs, 'pointParcellaire')
                for pn in range(len(pnts)):
                    pntPrcElmnt = SubElement(pntPrc, pnts[pn])
                    if pnts[pn] == 'id_douar':
                        pntPrcElmnt.text = drPntParce[0]
                    if pnts[pn] == 'name':
                        pntPrcElmnt.text = parceValues[0]
                    if pnts[pn] == 'num_parcelle':
                        pntPrcElmnt.text = str(polyg[value][0])
                    if pnts[pn] == 'partie':
                        pntPrcElmnt.text = 'P1'
                    if pnts[pn] == 'type':
                        pntPrcElmnt.text = parceValues[1]
                crdt = SubElement(pntPrc, 'coordinate')
                for crd in range(len(coord)):
                    crdtElmnt = SubElement(crdt, coord[crd])
                    if coord[crd] == 'x':
                        if parceValues[2] ==None:
                            crdtElmnt.text = ''
                        else:
                            crdtElmnt.text = str(float(parceValues[2]))
                    if coord[crd] == 'y':
                        if parceValues[3] == None:
                            crdtElmnt.text =''
                        else:
                            crdtElmnt.text =str(float(parceValues[3]))
                    if coord[crd] == 'z':
                        crdtElmnt.text = '0'

# -- DocParcelles --
            dcPrcel = SubElement(middle_xml, 'DocParcelles')

# -- Charges --
            chrg = SubElement(middle_xml, 'Charges')

# -- CONSISTANCE --
            consTab = ['codeConsistance', 'idSol', 'idSpeculation', 'libelle', 'libelleSol', 'libelleSpeculation']
            const = SubElement(middle_xml, 'Consistances')
            constElmnt = SubElement(const, 'Consistance')
            for cst in range(len(consTab)):
                constSubElmnt = SubElement(constElmnt, consTab[cst])
                if consTab[cst] == 'codeConsistance':
                    constSubElmnt.text = str(cnst[0][0])
                if consTab[cst] == 'idSol':
                    constSubElmnt.text = str(sol[0][0])
                if consTab[cst] == 'idSpeculation':
                    constSubElmnt.text = str(specl[0][0])
                if consTab[cst] == 'libelle':
                    constSubElmnt.text = cnst[0][1]
                if consTab[cst] == 'libelleSol':
                    constSubElmnt.text = sol[0][1]
                if consTab[cst] == 'libelleSpeculation':
                    constSubElmnt.text = specl[0][1]

        xml_write = minidom.parseString(ElementTree.tostring(top_xml, 'utf-8')).toprettyxml(indent="  ")
        try:
            filename = 'Toutes_les_parcelles.xml'
            filepath = os.path.join(os.path.join(os.path.expanduser('~')), 'desktop\IFE_PIECES\XML', filename)

            if not os.path.exists(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML')):
                os.makedirs(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\XML'))

            f = open(filepath, "w", encoding="utf-8")
            f.write(xml_write)
            f.close()
        except:
            msg = messagebox.showerror("XML", "Veuillez fermer le fichier")

#x = Export_Xml()
#x.xmlFile()