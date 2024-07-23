from ..database.conexion import conectar_db, cerrar_db

# Función para verificar si el usuario existe en la base de datos
def obtener_empleado(usuario):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        # Traer la información del empleado de la tabla nomina donde el mail sea igual al que se ingreso en el inicio de sesión
        consulta = "SELECT empleado FROM nomina WHERE mail = %s"
        cursor.execute(consulta, (usuario,))
        resultado = cursor.fetchone()

        if resultado:
            empleado = resultado[0]
        else:
            empleado = "No existe empleado con ese email"

        cursor.close()
    
    cerrar_db(conexion)

    return empleado

# Función para verificar si el usuario existe en la base de datos
def obtener_area(usuario):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        # Traer la información del area de la tabla nomina donde el mail sea igual al que se ingreso en el inicio de sesión
        consulta = "SELECT area FROM nomina WHERE mail = %s"
        cursor.execute(consulta, (usuario,))
        resultado = cursor.fetchone()

        if resultado:
            area = resultado[0]
        else:
            area = "No existe area con ese email"

        cursor.close()
    
    cerrar_db(conexion)

    return area

# Función para verificar si el usuario existe en la base de datos
def obtener_jerarquia(usuario):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        # Traer la información del jerarquia de la tabla nomina donde el mail sea igual al que se ingreso en el inicio de sesión
        consulta = "SELECT jerarquia FROM nomina WHERE mail = %s"
        cursor.execute(consulta, (usuario,))
        resultado = cursor.fetchone()

        if resultado:
            jerarquia = resultado[0]
        else:
            jerarquia = "No existe jerarquia con ese email"

        cursor.close()
    
    cerrar_db(conexion)

    return jerarquia

# Función para obtener los roles del usuario
def obtener_roles_empleado(empleado):
    roles = []

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        # Realizar consultas en cada tabla de roles para verificar si el empleado está asignado a algún rol
        tablas_roles = ["rol_analista_de_inventario", "rol_capacitador", "rol_ceo", "rol_jefe_de_area", "rol_operador","rol_recibos_de_sueldo", "rol_responsable_de_area", "rol_rrhh", "rol_sistemas", "rol_supervisor"]
        
        # Buscar tabla por tabla si está el nombre del empleado
        for tabla in tablas_roles:
            try:
                cursor.execute(f"SELECT * FROM {tabla} WHERE empleado = %s", (empleado,))
                resultados = cursor.fetchall()
                for resultado in resultados:
                    # Agregar el nombre del rol a la lista
                    roles.append(" ".join(tabla.split("_")[1:]))
            except Exception as e:
                # Manejar la excepción, por ejemplo, imprimir un mensaje de error
                print(f"Error al obtener roles del empleado: {str(e)}")
    
    except Exception as e:
        # Manejar la excepción de conexión a la base de datos, si es necesario
        print(f"Error de conexión a la base de datos: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conexion:
            cerrar_db(conexion)

    return roles



# Función para obtener todos los empleados con valor "SI" en la columna cuenta indicando que pertenecen a la empresa actualmente
def obtener_personal(area=None, jerarquia = None):
    empleados = []

    try:
        conexion = conectar_db()

        if conexion.is_connected():
            cursor = conexion.cursor()
            if area:
                # Se traen todos los empleados según el area que se ingreso por parametro y que tengan jerarquia menor al empleado que esta buscando
                consulta = "SELECT empleado FROM nomina WHERE area = %s AND cuenta = 'SI' AND jerarquia < %s ORDER BY empleado"
                cursor.execute(consulta, (area, jerarquia))
            else:
                # Se traen todos los empleados
                consulta = "SELECT empleado FROM nomina WHERE cuenta = 'SI' ORDER BY empleado"
                cursor.execute(consulta)

            resultados = cursor.fetchall()

            for resultado in resultados:
                empleados.append(resultado[0])
            
            cursor.close()

    finally:
        cerrar_db(conexion)

    return empleados

# Función para obtener todos las areas del empleado que esta buscando
def obtener_areas_por_empleado(empleado):
    areas = []

    try:
        conexion = conectar_db()

        if conexion.is_connected():
            cursor = conexion.cursor()
            # Traer las areas de la tabla de relación responsable-area donde el responsable sea el empleado que esta buscando 
            consulta = "SELECT area FROM relacion_responsable_y_area WHERE responsable = %s"
            cursor.execute(consulta, (empleado,))
            resultados = cursor.fetchall()
            # Se guarda en la variable area todos los valores encontrados uno por uno en una lista
            for resultado in resultados:
                areas.append(resultado[0])

            cursor.close()

    finally:
        cerrar_db(conexion)

    return areas

# Traer el personal de todas las areas luego de que se sepa las areas que son de cierto responsable de area
def obtener_personal_por_areas(areas):
    empleados_por_areas = []

    try:
        conexion = conectar_db()

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Construir la cadena de parámetros para la consulta SQL
            params = ','.join(['%s'] * len(areas))
            # Verificar si la lista de áreas no está vacía antes de ejecutar la consulta
            if areas:
                # Se busca todos los empleados cuya área se encuentra en los valores luego del IN
                consulta = f"SELECT empleado FROM nomina WHERE area IN ({params}) ORDER BY empleado"
                cursor.execute(consulta, areas)
                resultados = cursor.fetchall()
                # Se va guardando empleado por empleado en la variable empleados_por_areas
                for resultado in resultados:
                    empleados_por_areas.append(resultado[0])

            cursor.close()

    finally:
        cerrar_db(conexion)

    return empleados_por_areas


# Traer la informacion del empleado que se seleccionó
def get_employee_data(chosen_employee):
    info_employee = None

    try:
        conexion = conectar_db()

        if conexion.is_connected():
            cursor = conexion.cursor()
            # Traer todas las columnas mencionadas del empleado seleccionado
            consulta = "SELECT empleado, cuil, fecha_ingreso, legajo, mail, fecha_nacimiento, forma, turno, area, jerarquia, categoria, convenio, medife FROM nomina WHERE empleado = %s"
            cursor.execute(consulta, (chosen_employee,))
            
            # Obtener la fila resultante de la consulta
            row = cursor.fetchone()
            
            # Comprobar si se encontraron resultados
            if row:
                # Convertir la fila a un diccionario para poder manejar el acceso a los valores
                columns = [desc[0] for desc in cursor.description]
                info_employee = dict(zip(columns, row))

    except Exception as e:
        # En caso de error se imprime lo siguiente
        print("Error al obtener los datos del empleado:", e)

    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            cerrar_db(conexion)

    return info_employee

            