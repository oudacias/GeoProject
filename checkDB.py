import os
from Log_in import createDB

PATH =os.path.abspath(os.curdir) + '/Connection/ConnectionFile.py'

if os.path.isfile(PATH):
    from Log_in import Login




if __name__ == "__main__":
    PATH = os.path.abspath(os.curdir) + '\\Connection\\ConnectionFile.py'

    filename = 'Parcelle_ZN3.docx'
    filepath = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\IFE_PIECES\ZN3', filename)

    # print(filepath)


    if os.path.isfile(PATH):
        app = Login.FrameWindow()
        app.mainloop()
    else:
        app = createDB.FrameWindow()
        app.mainloop()

