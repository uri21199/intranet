from ..database.conexion import conectar_db, cerrar_db
# Función para verificar que la contraseña ingresada sea igual a la actual
def verify_pass(empleado, old_pass):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        # Verificar que la contraseña sea la misma
        consulta = "SELECT contrasena FROM contrasena WHERE empleado = %s"
        cursor.execute(consulta, (empleado,))
        resultado = cursor.fetchone()

        if resultado is not None and resultado[0] == old_pass:
            return True
        
        cursor.close()
    
    cerrar_db(conexion)

    return False

# Función para cambiar la contraseña en la tabla contrasena
def change_pass(empleado, new_pass):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        consulta = "UPDATE contrasena SET contrasena = %s WHERE empleado = %s"
        cursor.execute(consulta, (new_pass, empleado))
        conexion.commit()

        cursor.close()
        return True
    
    cerrar_db(conexion)

    return False

# Función que establece una minima exigencia a la hora de registrar la contraseña nueva
def secure_pass(new_pass):
    large = False
    mayus = False
    number = False
    # Si la longitud es mayor a 8 devolver true
    if len(new_pass) > 8:
        large = True
    for i in range(len(new_pass)):
        # Si hay una mayuscula en la contraseña nueva devolver true
        if new_pass[i].isupper():
            mayus = True
        # Si hay un número en la contraseña nueva devolver true
        if new_pass[i].isnumeric():
            number = True
    # Si large, mayus y number son true devolver True para poder seguir trabajando sino devolver False y detener el cambio de contraseña. Si devuelve False es porque no se paso por los requerimientos anteriores
    if large and mayus and number:
        return True
    else:
        return False