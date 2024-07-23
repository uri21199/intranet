import mysql.connector

# Función para conectar a la base de datos
def conectar_db():
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="intranet"
        )
        return conexion
    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

#Función para cerrar la base de datos
def cerrar_db(conexion):
    if conexion:
        conexion.close()
