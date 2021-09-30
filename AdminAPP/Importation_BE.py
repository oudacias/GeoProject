import os
import xlrd
import sys
sys.path.append(".")
PATH = os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    from Connection.ConnectionFile import Connection
class Importation:

                                    # ----------------------------- IMPORT TITRES / REQUISITIONS --------------------------
#TXT
    def titReqs_txt(self, filetxt):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        file = open(filetxt, "r")
        text_content = file.readlines()
        for p in text_content:
            tab = p.split()
            tit_rqs = tab[1]+tab[2]+"/"+tab[3]
            if tab[1] == 'R':
                cur.execute("UPDATE parcelles SET requisition='"+tit_rqs+"' WHERE id_parcelle="+tab[0]+"")
                conn.commit()
            elif tab[1] == 'T':
                cur.execute("UPDATE parcelles SET titre='"+tit_rqs+"' WHERE id_parcelle=" + tab[0] + "")
                conn.commit()

#EXCEL
    def titReqs_xsl(self, loadfile):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        excel_wb = xlrd.open_workbook(loadfile)
        excel_sheet = excel_wb.sheet_by_index(0)
        sheet_content = excel_sheet.cell(0, 0)

        nbr_ligne = excel_sheet.nrows
        for L in range(nbr_ligne):
            if excel_sheet.cell_value(L, 1) == 'T':
                x = cur.execute("UPDATE parcelles SET titre = '"+str(excel_sheet.cell_value(L, 1))+""+str(int(excel_sheet.cell_value(L, 2)))+"/"+str(int(excel_sheet.cell_value(L, 3)))+"' where id_parcelle ="+str(int(excel_sheet.cell_value(L, 0)))+";")
                conn.commit()
            elif excel_sheet.cell_value(L, 1) == 'R':
                x = cur.execute("UPDATE parcelles SET requisition = '"+str(excel_sheet.cell_value(L, 1))+""+str(int(excel_sheet.cell_value(L, 2)))+"/"+str(int(excel_sheet.cell_value(L, 3)))+"' where id_parcelle ="+str(int(excel_sheet.cell_value(L, 0)))+";")
                conn.commit()


# ----------------------------------------------------------------------------------------------------------------------
                                        # ----------------------------- IMPORT COORDINATES X Y -------------------------
#TXT
    def coordXY_txt(self, filetxt):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        file = open(filetxt, "r")
        text_content = file.readlines()
        for p in text_content:
            tab = p.split()
            cur.execute("UPDATE points SET x_def = "+tab[1].replace(",", ".")+", y_def = "+tab[2].replace(",", ".")+", reference = '"+tab[3]+"' WHERE id_point = '"+tab[0]+"';")
            conn.commit()


#EXCEL
    def coordXY_xsl(self, loadfile):
        connection = Connection()
        conn = connection.connect()
        cur = conn.cursor()
        excel_wb = xlrd.open_workbook(loadfile)
        excel_sheet = excel_wb.sheet_by_index(0)
        sheet_content = excel_sheet.cell(0, 0)
        nbr_ligne = excel_sheet.nrows

        for L in range(nbr_ligne):
            coord_x = "{}".format(excel_sheet.cell(L, 1).value)
            coord_y = "{}".format(excel_sheet.cell(L, 2).value)
            id_point = int(excel_sheet.cell(L, 0).value)

            cur.execute("UPDATE points SET X_def = "+coord_x+" , Y_def = "+coord_y+" , reference = '"+excel_sheet.cell(L, 3).value+"' WHERE id_point = '"+str(id_point)+"';")

            conn.commit()
