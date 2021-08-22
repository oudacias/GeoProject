import comtypes.client
import os

wordFile = 'P' + '2' + '_ZN1.docx'
pdfFile = 'P' + '2' + '_ZN1.pdf'


in_file = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\ZN1', wordFile)
out_file = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\ZN1', pdfFile)
print(in_file)
wdFormatPDF = 17
word = comtypes.client.CreateObject('Word.Application')
print("loading")
doc = word.Documents.Open(in_file)
doc.SaveAs(out_file, FileFormat=wdFormatPDF)
print('waiting')
doc.close()
word.Quit()
print('done')
