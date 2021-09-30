import sys
import os
import comtypes.client

wdFormatPDF = 17

in_file = "C:/Users/LAILA/PycharmProjects/EpGis2/AdminAPP/hello1.docx"
out_file = "C:/Users/LAILA/PycharmProjects/EpGis2/AdminAPP/hello1.pdf"

word = comtypes.client.CreateObject('Word.Application')
doc = word.Documents.Open(in_file)
doc.SaveAs(out_file, FileFormat=wdFormatPDF)
print("hello")
doc.Close()
word.Quit()