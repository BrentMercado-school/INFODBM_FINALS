import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DESKTOP-OV838G7\SQLEXPRESS;"
        "Database=INFODBM_FINALS;"
        "Trusted_Connection=yes;"
    )

    return conn