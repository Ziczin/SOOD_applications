import pyodbc
from dotenv import load_dotenv

def drop():
    load_dotenv()

    db_username='python'
    db_password='000000000'
    db_server='192.168.200.38'
    db_name='Applications_Django_Python'

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};' +\
                        f'SERVER={db_server};' +\
                        f'DATABASE={db_name};' +\
                        f'UID={db_username};' +\
                        f'PWD={db_password}'

    conn = pyodbc.connect(connection_string)

    cursor = conn.cursor()

    cursor.execute("EXEC DROPALL")

    conn.commit()
    cursor.close()
    conn.close()
