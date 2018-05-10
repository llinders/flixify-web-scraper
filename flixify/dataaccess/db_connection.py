import pyodbc
import platform
print(platform.node())
# Specifying the ODBC driver, server name, database, etc. directly
cnxn = 0
if(platform.node() == "HP-Pav"):
    print("Martijn")
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=HP-PAV;DATABASE=FLIXIFY_MOVIES;UID=sa;PWD=6836PT')
else:
    print("Luc")
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=FLIXIFY_MOVIES;UID=weetikhet;PWD=nice')

cursor = cnxn.cursor()

