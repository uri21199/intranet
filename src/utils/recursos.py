from ..database.conexion import conectar_db, cerrar_db
import mysql.connector
# Función para verificar que la contraseña ingresada sea igual a la actual
def obtener_recursos_empleado(empleado):
    conexion = conectar_db()
    recursos_asignados = []
    try:
        if conexion.is_connected():
            cursor = conexion.cursor()

            # Verificar que la contraseña sea la misma
            consulta = "SELECT id, tipo_de_equipo, nro_serie, marca, modelo  FROM recursos WHERE usuario = %s"
            cursor.execute(consulta, (empleado,))
            resultados = cursor.fetchall()

            for resultado in resultados:
                recurso = {
                    'id': resultado[0],
                    'tipo_de_equipo': resultado[1],
                    'nro_serie': resultado[2],
                    'marca': resultado[3],
                    'modelo': resultado[4]
                }
                recursos_asignados.append(recurso)
            cursor.close()
            cerrar_db(conexion)
            return recursos_asignados
    except mysql.connector.Error as e:
        print(f"Error de MySQL: {e}")
        return None

def obtener_recursos():
    conexion = conectar_db()
    recursos_totales = []
    try:
        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = "SELECT id FROM recursos"
            cursor.execute(consulta)
            resultados = cursor.fetchall()

            # Iterar sobre los resultados y extraer los valores de las tuplas
            for resultado in resultados:
                recurso = resultado# Extraer el valor de la tupla
                recursos_totales.append(recurso)

            cursor.close()
            cerrar_db(conexion)
            return recursos_totales
    except mysql.connector.Error as e:
        print(f"Error de MySQL: {e}")
        return None


def obtener_info_de_recurso(recurso, causa):
    conexion = conectar_db()

    try:
        if conexion.is_connected():
            cursor = conexion.cursor()

            if causa == 'informacion':
                consulta = "SELECT id, tipo_de_equipo, usuario, anydesk, nro_serie, marca, modelo, ficha, comentarios FROM recursos WHERE id = %s"
            elif causa == 'estado':
                consulta = "SELECT id, tipo_de_equipo, estado, ubicacion, usuario, area, cliente, comentarios FROM recursos WHERE id = %s"
            elif causa == 'asignacion':
                consulta = "SELECT id, tipo_de_equipo, ubicacion, usuario, area, cliente, comentarios FROM recursos WHERE id = %s"
            else:
                # Manejo de causa no válida
                return None

            cursor.execute(consulta, (recurso,))
            resultado = cursor.fetchone()

            if resultado:
                if causa == 'informacion':
                    recurso_final = {
                        'id': resultado[0],
                        'tipo_de_equipo': resultado[1],
                        'usuario': resultado[2],
                        'anydesk': resultado[3],
                        'nro_serie': resultado[4],
                        'marca': resultado[5],
                        'modelo': resultado[6],
                        'ficha': resultado[7],
                        'comentarios': resultado[8]
                    }
                elif causa == 'estado':
                    recurso_final = {
                        'id': resultado[0],
                        'tipo_de_equipo': resultado[1],
                        'estado': resultado[2],
                        'ubicacion': resultado[3],
                        'usuario': resultado[4],
                        'area': resultado[5],
                        'cliente': resultado[6],
                        'comentarios': resultado[7]
                    }
                elif causa == 'asignacion':
                    recurso_final = {
                        'id': resultado[0],
                        'tipo_de_equipo': resultado[1],
                        'ubicacion': resultado[2],
                        'usuario': resultado[3],
                        'area': resultado[4],
                        'cliente': resultado[5],
                        'comentarios': resultado[6]
                    }
                print(f"Este es: {recurso_final}")
                return recurso_final
            else:
                # Manejo de recurso no encontrado
                return None

    except mysql.connector.Error as e:
        print(f"Error de MySQL: {e}")
        return None
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def actualizar_valor_recurso(id_, columna, valor):
    conexion = conectar_db()
    try:
        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = f"UPDATE recursos SET {columna} = %s WHERE id = %s"
            cursor.execute(consulta, (valor, id_))

            conexion.commit()
            cursor.close()
            cerrar_db(conexion)
    except mysql.connector.Error as e:
        print(f"Error de MySQL: {e}")
        return None