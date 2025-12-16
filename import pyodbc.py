import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=hassel.database.windows.net;"
    "DATABASE=schooldb;"
    "UID=your-hasse;"
    "PWD=your-Darthvader12!;"
)

cursor = conn.cursor()
