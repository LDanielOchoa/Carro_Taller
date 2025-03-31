import pyodbc

try:
    
    conn = pyodbc.connect(
    
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=192.168.90.64;'
        'DATABASE=UNOEE;'
        'UID=power-bi;'
        'PWD=Z1x2c3v4*'
    )
    cursor = conn.cursor()

    campo = 'F200_ID'  
    tabla = 'BI_W0550'  

    # Consulta para obtener el contenido del campo
    consulta = f"SELECT {campo} FROM {tabla};"
    cursor.execute(consulta)

    # Imprimir resultados
    print(f"Contenido del campo '{campo}':")
    for fila in cursor.fetchall():
        print(fila[0])

except Exception as e:
    print("Error al conectar o ejecutar la consulta:", e)
finally:
    if 'conn' in locals():
        conn.close()

