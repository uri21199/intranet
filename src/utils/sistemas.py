# Importaciones
from ..database.conexion import conectar_db, cerrar_db
from datetime import datetime, timedelta

# Función para insertar los datos en la tabla que corresponda
def guardar_reporte_a_sistemas(categoria, subcategoria, tipo_problema, descripcion_problema, id_equipo, empleado):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        #Variable para guardar la fecha actual en el formato deseado
        fecha_modificacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        consulta = f"INSERT INTO ticket_sistemas (categoria_problema, subcategoria_problema, tipo_de_problema, descripcion_problema, id_equipo, estado, fecha_creacion, prioridad, empleado, reportado_a) VALUES (%s, %s, %s, %s, %s, 'Notificado', %s, 'Normal', %s, 'Bustos Lautaro')"
        cursor.execute(consulta, (categoria, subcategoria, tipo_problema, descripcion_problema, id_equipo, fecha_modificacion, empleado))

        conexion.commit()
        cursor.close()
        cerrar_db(conexion)

        return True
    
    return False

def obtener_empleados_sistemas():
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()


        consulta = f"SELECT empleado FROM rol_sistemas"
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        empleados = [empleado[0] for empleado in resultados]
        conexion.commit()
        cursor.close()
        cerrar_db(conexion)

        return empleados
    
    return False

def obtener_reportes_a_sistemas():
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        consulta = "SELECT id, categoria_problema, subcategoria_problema, tipo_de_problema, descripcion_problema, id_equipo, estado, fecha_creacion, prioridad, empleado, reportado_a FROM ticket_sistemas WHERE estado != 'Cerrado' AND estado != 'Empleado notificado'"
        cursor.execute(consulta)

        # Obtener todos los resultados de la consulta
        resultados = cursor.fetchall()

        filas = []

        for fila in resultados:
            ticket = {
                'id': fila[0],
                'categoria_problema': fila[1],
                'subcategoria_problema': fila[2],
                'tipo_de_problema': fila[3],
                'descripcion_problema': fila[4],
                'id_equipo': fila[5],
                'estado': fila[6],
                'fecha_creacion': fila[7],
                'prioridad': fila[8],
                'empleado': fila[9],
                'reportado_a': fila[10]
            }
            filas.append(ticket)
        # Cerrar cursor y conexión
        cursor.close()
        cerrar_db(conexion)

        # Devolver los resultados
        return filas

    # Si no se pudo conectar a la base de datos, devolver None
    return None

def actualizar_ticket(id, estado, prioridad, reportado_a, cerrado=False):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        #Variable para guardar la fecha actual en el formato deseado
        fecha_modificacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        if cerrado == 'Si':
            consulta = "UPDATE ticket_sistemas SET estado = %s, prioridad = %s, reportado_a = %s, fecha_actualizacion = %s, fecha_cierre = %s WHERE id = %s"
            cursor.execute(consulta, (estado, prioridad, reportado_a, fecha_modificacion, fecha_modificacion, id))
        elif cerrado == 'Fin':
            consulta = "UPDATE ticket_sistemas SET estado = 'Empleado notificado', fecha_actualizacion = %s, fecha_cierre = %s WHERE id = %s"
            cursor.execute(consulta, (fecha_modificacion, fecha_modificacion, id))
        else:
            consulta = "UPDATE ticket_sistemas SET estado = %s, prioridad = %s, reportado_a = %s, fecha_actualizacion = %s WHERE id = %s"
            cursor.execute(consulta, (estado, prioridad, reportado_a, fecha_modificacion, id))

        if cerrado != 'Fin':
            consulta_mod = "INSERT INTO ticket_sistemas_mod (id, estado, prioridad, reportado_a, fecha_actualizacion, fecha_cierre) VALUES (%s,%s, %s, %s, %s, %s)"
            cursor.execute(consulta_mod, (id, estado, prioridad, reportado_a, fecha_modificacion, fecha_modificacion))
        else:
            consulta_mod = "INSERT INTO ticket_sistemas_mod (id, estado, prioridad, reportado_a, fecha_actualizacion, fecha_cierre) VALUES (%s,'Empleado notificado', %s, %s, %s, %s)"
            cursor.execute(consulta_mod, (id, prioridad, reportado_a, fecha_modificacion, fecha_modificacion))

        conexion.commit()
        cursor.close()
        cerrar_db(conexion)

        return True
    
    return False

def obtener_tickets_sistemas(empleado):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        consulta = "SELECT id, categoria_problema, subcategoria_problema, tipo_de_problema, descripcion_problema, id_equipo, estado, fecha_creacion, prioridad, empleado, reportado_a FROM ticket_sistemas WHERE empleado = %s AND estado != 'Empleado notificado'"
        cursor.execute(consulta, (empleado,))

        resultados = cursor.fetchall() 
        filas = []

        for fila in resultados:
            ticket = {
                'id': fila[0],
                'categoria_problema': fila[1],
                'subcategoria_problema': fila[2],
                'tipo_de_problema': fila[3],
                'descripcion_problema': fila[4],
                'id_equipo': fila[5],
                'estado': fila[6],
                'fecha_creacion': fila[7],
                'prioridad': fila[8],
                'empleado': fila[9],
                'reportado_a': fila[10]
            }
            filas.append(ticket)

        conexion.commit()
        cursor.close()
        cerrar_db(conexion)
        print(filas)
        return filas
    
    return False