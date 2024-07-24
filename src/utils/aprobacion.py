from ..database.conexion import conectar_db, cerrar_db
from datetime import datetime, timedelta

def obtener_dias_por_aprobar(empleado):
    dias_solicitados = []
    tablas = ['dia_ausencia', 'dia_home', 'dia_estudio', 'dia_vacaciones']
    conceptos = {
        'dia_home': 'Home Office',
        'dia_ausencia': 'Ausencia',
        'dia_vacaciones': 'Vacaciones',
        'dia_estudio': 'Día de estudio'
    }

    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        for tabla in tablas:
            if tabla in ['dia_ausencia', 'dia_vacaciones']:
                consulta = f"SELECT empleado, fecha_inicio, fecha_final, fecha_solicitud, estado, causa FROM {tabla} WHERE estado = 'SOLICITADO' AND empleado = %s"
                cursor.execute(consulta, (empleado,))
            else:
                consulta = f"SELECT empleado, fecha_inicio, fecha_solicitud, estado FROM {tabla} WHERE estado = 'SOLICITADO' AND empleado = %s"
                cursor.execute(consulta, (empleado,))
            resultados = cursor.fetchall()
            for resultado in resultados:
                concepto = conceptos.get(tabla, 'Otro')
                resultado_obj = {
                    'empleado': resultado[0],
                    'fecha_inicio': resultado[1],
                    'fecha_fin': resultado[2] if len(resultado) >= 6 else '',
                    'fecha_solicitud': resultado[3] if len(resultado) >= 6 else resultado[2],
                    'estado': resultado[4] if len(resultado) >= 6 else resultado[3],
                    'causa': resultado[5] if len(resultado) >= 6 else '',
                    'concepto': concepto
                }
                dias_solicitados.append(resultado_obj)

        cursor.close()
        cerrar_db(conexion)
    
    return dias_solicitados

def obtener_dias_filtro(empleado_, concepto, fecha_inicio_, fecha_fin, area):
    dias_filtro = []

    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        try:
            consulta = f"SELECT empleado, fecha_inicio, fecha_final, fecha_solicitud, estado, causa FROM {concepto} WHERE 1=1"
            parametros = []

            if empleado_ != 'todos':
                consulta += " AND empleado = %s"
                parametros.append(empleado_)

            if len(fecha_fin) < 1:
                consulta += " AND fecha_inicio = %s"
                parametros.append(fecha_inicio_)
            else:
                consulta += " AND fecha_inicio BETWEEN %s AND %s"
                parametros.append(fecha_inicio_)
                parametros.append(fecha_fin)

            if area != 'RRHH':
                consulta += " AND area = %s"
                parametros.append(area)

            # Calcular la fecha de hace 30 días
            hace_30_dias = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            consulta += " AND fecha_inicio >= %s"
            parametros.append(hace_30_dias)

            cursor.execute(consulta, parametros)
            resultados = cursor.fetchall()

            for resultado in resultados:
                empleado = resultado[0]
                fecha_inicio = resultado[1]
                fecha_final = resultado[2] if len(resultado) > 5 else ''
                fecha_solicitud = resultado[3] if len(resultado) > 5 else resultado[2]
                estado = resultado[4] if len(resultado) > 5 else resultado[3]
                causa = resultado[5] if len(resultado) > 5 else resultado[4]

                dia_filtro = {
                    'empleado': empleado,
                    'fecha_inicio': fecha_inicio,
                    'fecha_final': fecha_final,
                    'fecha_solicitud': fecha_solicitud,
                    'estado': estado,
                    'causa': causa,
                    'concepto': concepto 
                }

                dias_filtro.append(dia_filtro)
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
            cerrar_db(conexion)
    
    return dias_filtro


def aprobar_dias(empleado_sol, fecha, concepto, empleado):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()
        fecha_modificacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        if concepto in ['dia_ausencia', 'dia_vacaciones']:
            consulta = f"UPDATE {concepto} SET estado = 'APROBADO', fecha_cambio_estado = %s, superior = %s WHERE empleado = %s AND fecha_inicio = %s"      
        else:
            consulta = f"UPDATE {concepto} SET estado = 'APROBADO', fecha_cambio_estado = %s, superior = %s WHERE empleado = %s AND fecha_inicio = %s"
        cursor.execute(consulta, (fecha_modificacion, empleado, empleado_sol, fecha))
        
        # Confirmar los cambios en la base de datos
        conexion.commit()

        # Verificar si se afectaron filas en la base de datos
        if cursor.rowcount > 0:
            return True
        else:
            return False
    else:
        return False

def eliminar_dias(empleado_sol, fecha, concepto, empleado):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()
        fecha_modificacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        if concepto in ['dia_ausencia', 'dia_vacaciones']:
            consulta = f"UPDATE {concepto} SET estado = 'RECHAZADO', fecha_cambio_estado = %s, superior = %s WHERE empleado = %s AND fecha_inicio = %s"      
        else:
            consulta = f"UPDATE {concepto} SET estado = 'RECHAZADO', fecha_cambio_estado = %s, superior = %s WHERE empleado = %s AND fecha_inicio = %s"
        cursor.execute(consulta, (fecha_modificacion, empleado, empleado_sol, fecha))
        
        # Confirmar los cambios en la base de datos
        conexion.commit()

        # Verificar si se afectaron filas en la base de datos
        if cursor.rowcount > 0:
            return True
        else:
            return False
    else:
        return False
    
def actualizar_dia(empleado_form, fecha_solicitud, fecha_inicio, fecha_final, estado, causa, concepto, superior):
    try:
        conexion = conectar_db()

        if conexion.is_connected():
            cursor = conexion.cursor()
            fecha_modificacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            concepto_ = concepto
            if concepto_ in ['dia_ausencia', 'dia_vacaciones']:
                consulta = f"UPDATE {concepto} SET fecha_inicio = %s, fecha_final = %s, estado = %s, causa = %s, fecha_cambio_estado = %s, superior = %s WHERE empleado = %s AND fecha_solicitud = %s"      
                cursor.execute(consulta, (fecha_inicio, fecha_final, estado, causa, fecha_modificacion, superior, empleado_form, fecha_solicitud))
            else:
                consulta = f"UPDATE {concepto} SET fecha_inicio = %s, estado = %s, fecha_cambio_estado = %s, superior = %s WHERE empleado = %s AND fecha_solicitud = %s"
                cursor.execute(consulta, (fecha_inicio, estado, fecha_modificacion, superior, empleado_form, fecha_solicitud))
            
            # Confirmar los cambios en la base de datos
            conexion.commit()

            # Verificar si se afectaron filas en la base de datos
            if cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(f"Error al actualizar el día: {e}")
        return False

