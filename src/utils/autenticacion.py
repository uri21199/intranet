from ..database.conexion import conectar_db, cerrar_db

# Función para verificar si el usuario existe en la base de datos
def autenticar_usuario(email, password):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        # Traer la contrasena de la tabla contrasena donde el mail sea igual al que se ingreso en el inicio de sesión
        consulta = "SELECT contrasena FROM contrasena WHERE mail = %s"
        cursor.execute(consulta, (email,))
        resultado = cursor.fetchone()

        # Si la password ingresada es igual a la contrasena se devuelve True
        if resultado is not None and resultado[0] == password:
            return True

        cursor.close()
    
    cerrar_db(conexion)