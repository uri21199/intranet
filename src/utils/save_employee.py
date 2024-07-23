from ..database.conexion import conectar_db, cerrar_db
import re

# Función para verificar si el usuario existe en la base de datos
def save_info_employee_db(empleado_a_editar, cuil, fecha_ingreso, legajo, mail, forma, turno, area, fecha_nacimiento, categoria, convenio, medife):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        # Traer la información del empleado de la tabla nomina donde el mail sea igual al que se ingreso en el inicio de sesión
        consulta = "UPDATE nomina SET empleado = %s, cuil = %s, fecha_ingreso = %s, legajo = %s, mail = %s, forma = %s, turno = %s, area = %s, fecha_nacimiento = %s, categoria = %s, convenio = %s, medife = %s WHERE empleado = %s"
        cursor.execute(consulta, (empleado_a_editar, cuil, fecha_ingreso, legajo, mail, forma, turno, area, fecha_nacimiento, categoria, convenio, medife, empleado_a_editar))
        conexion.commit()

        cursor.close()
        return True
    
    cerrar_db(conexion)

    return False

# Función para verificar si el usuario existe en la base de datos
def save_new_employee_db(empleado_nuevo, cuil, fecha_ingreso, finaliza_pp_str, legajo, mail, cuenta, genero, fecha_nacimiento, forma, turno, area, jerarquia, categoria, convenio, medife, roles_seleccionados):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        # Insertar un nuevo empleado en la tabla nomina
        insert_new_employee_nomina(cursor, empleado_nuevo, cuil, fecha_ingreso, finaliza_pp_str, legajo, mail, cuenta, genero, fecha_nacimiento, forma, turno, area, jerarquia, categoria, convenio, medife)
        # Insertar empleado en la tabla contrasena
        insert_new_employee_contrasena(cursor, empleado_nuevo, mail, cuil)
        # Insertar empleado en la tabla de los roles
        insert_new_employee_roles(cursor, empleado_nuevo, roles_seleccionados)
        conexion.commit()
        cursor.close()
        return True
    
    cerrar_db(conexion)

    return False

def insert_new_employee_nomina(cursor, empleado_nuevo, cuil, fecha_ingreso, finaliza_pp_str, legajo, mail, cuenta, genero, fecha_nacimiento, forma, turno, area, jerarquia, categoria, convenio, medife):
    consulta_nomina = "INSERT INTO nomina (empleado, cuil, fecha_ingreso, finaliza_pp, legajo, mail, cuenta, genero, fecha_nacimiento, forma, turno, area, jerarquia, categoria, convenio, medife) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    if convenio == 'Si':
        convenio = 'CONVENIO COMERCIO ADMINISTRATIVO C'
    elif convenio == 'No':
        convenio = 'FUERA DE CONVENIO'

    datos_empleado = (empleado_nuevo, cuil, fecha_ingreso, finaliza_pp_str, legajo, mail, cuenta, genero, fecha_nacimiento, forma, turno, area, jerarquia, categoria, convenio, medife)
    cursor_ = cursor
    cursor_.execute(consulta_nomina, datos_empleado)

    return True

def insert_new_employee_contrasena(cursor, empleado, mail, cuil):
     consulta_contrasena = "INSERT INTO contrasena (empleado, mail, contrasena) VALUES (%s, %s, %s)"
     cursor.execute(consulta_contrasena, (empleado, mail, cuil))

     return True

def insert_new_employee_roles(cursor, empleado_nuevo, roles_seleccionados):
    for rol in roles_seleccionados:
        consulta = f"INSERT INTO rol_{rol} (empleado) VALUES ('{empleado_nuevo}')"
        cursor.execute(consulta)
    
    return True
"""
def validate_cuil(cursor, cuil):
    try:
        consulta = "SELECT cuil FROM nomina WHERE cuil = %s"
        cursor.execute(consulta, (cuil,))
        resultado = cursor.fetchone()
        
        if resultado:  # Si se encontró un registro con el mismo cuil devuelve false
            return False
        else:
            return True
    except Exception as e:
        print("Error al validar CUIL:", e)
        return False

def validate_email_format(email):
    # Expresión regular para validar el formato del MAIL
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_hierarchy_rol(jerarquia, roles_seleccionados):
    if jerarquia == '2' and 'supervisor' not in roles_seleccionados:
        return False
    elif jerarquia == '3' and 'jefe_de_area' not in roles_seleccionados:
        return False
    elif jerarquia == '4' and 'responsable_de_area' not in roles_seleccionados:
        return False
    elif jerarquia == '5' and 'ceo' not in roles_seleccionados:
        return False
    else: 
        return True
"""