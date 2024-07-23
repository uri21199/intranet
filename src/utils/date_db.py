# Importaciones
from ..database.conexion import conectar_db, cerrar_db
from datetime import datetime, timedelta
from flask import flash

# Función para insertar los datos en la tabla que corresponda
def save_date_db(empleado, date, area, jerarquia, type_of_day, date_end=None, type_absent=None):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        # Variable para guardar la fecha actual en el formato deseado
        fecha_modificacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        # Verificar si ya existe un registro con los mismos valores
        if type_of_day in ['estudio', 'home']:
            consulta_check = f"SELECT COUNT(*) FROM dia_{type_of_day} WHERE empleado = %s AND fecha_inicio = %s AND area = %s AND jerarquia = %s"
            cursor.execute(consulta_check, (empleado, date, area, jerarquia))
        elif type_of_day in ['ausencia', 'vacaciones']:
            consulta_check = f"SELECT COUNT(*) FROM dia_{type_of_day} WHERE empleado = %s AND fecha_inicio = %s AND fecha_final = %s AND area = %s AND jerarquia = %s"
            cursor.execute(consulta_check, (empleado, date, date_end, area, jerarquia))
        
        # Obtener el resultado de la verificación
        resultado_check = cursor.fetchone()[0]

        if resultado_check > 0:
            cursor.close()
            cerrar_db(conexion)
            flash('La fecha ya fue cargada', 'error')  # Usar Flash messages para mostrar alerta en el navegador
            return False
        else:
            # Si no existe duplicado, insertar el nuevo registro
            if type_of_day in ['estudio', 'home']:
                consulta = f"INSERT INTO dia_{type_of_day} (empleado, fecha_inicio, area, jerarquia, fecha_solicitud, estado) VALUES (%s, %s, %s, %s, %s, 'SOLICITADO')"
                cursor.execute(consulta, (empleado, date, area, jerarquia, fecha_modificacion))
            elif type_of_day in ['ausencia', 'vacaciones']:
                consulta = f"INSERT INTO dia_{type_of_day} (empleado, fecha_inicio, fecha_final, area, jerarquia, fecha_solicitud, causa, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, 'SOLICITADO')"
                cursor.execute(consulta, (empleado, date, date_end, area, jerarquia, fecha_modificacion, type_absent))
            
            conexion.commit()
            cursor.close()
            cerrar_db(conexion)
            return True

    return False

# Función para traer las fechas de las distintas tablas segun corresponda
def bring_date_db(empleado, estado, type_of_day):
    try:
        conexion = conectar_db()
        dates = []

        if conexion.is_connected():
            cursor = conexion.cursor() 

            fecha_actual = datetime.now()
            if estado == 'RECHAZADO':
                fecha_mes_atras = fecha_actual - timedelta(days=15)
            else:
                fecha_mes_atras = fecha_actual - timedelta(days=30)
            fecha_mas_adelante = fecha_actual + timedelta(days=30)

            fecha_un_mes_atras_str = fecha_mes_atras.strftime('%Y-%m-%d')
            fecha_un_mes_adelante_str = fecha_mas_adelante.strftime('%Y-%m-%d')

            # Si es dia de ausencia tiene fecha_inicio y fecha_final por lo que se realiza un condicional para esta diferencia
            if type_of_day != 'ausencia':
                if estado == 'RECHAZADO':
                    consulta = f"SELECT fecha_inicio, causa_rechazo FROM dia_{type_of_day} WHERE empleado = %s AND estado = %s AND fecha_inicio BETWEEN '{fecha_un_mes_atras_str}' AND '{fecha_un_mes_adelante_str}' ORDER BY fecha_inicio ASC"
                else:
                    consulta = f"SELECT fecha_inicio FROM dia_{type_of_day} WHERE empleado = %s AND estado = %s AND fecha_inicio BETWEEN '{fecha_un_mes_atras_str}' AND '{fecha_un_mes_adelante_str}' ORDER BY fecha_inicio ASC"

            if type_of_day in ['ausencia', 'vacaciones']:
                if estado == 'RECHAZADO':
                    consulta = f"SELECT fecha_inicio, fecha_final, causa_rechazo FROM dia_{type_of_day} WHERE empleado = %s AND estado = %s AND fecha_inicio BETWEEN '{fecha_un_mes_atras_str}' AND '{fecha_un_mes_adelante_str}' ORDER BY fecha_inicio ASC"
                else:
                    consulta = f"SELECT fecha_inicio, fecha_final FROM dia_{type_of_day} WHERE empleado = %s AND estado = %s AND fecha_inicio BETWEEN '{fecha_un_mes_atras_str}' AND '{fecha_un_mes_adelante_str}' ORDER BY fecha_inicio ASC"
            
            cursor.execute(consulta, (empleado, estado))
            
            resultados = cursor.fetchall()
            
            # Se guarda cada fecha en la lista dates. Si es ausencia va a tener dos valores (fecha inicio y fecha fin). Se hace un condicional para esta diferencia
            for resultado in resultados:
                if estado == 'RECHAZADO':
                    if type_of_day in ['ausencia', 'vacaciones']:
                        dates.append([resultado[0], resultado[1], resultado[2]])  # fecha_inicio, fecha_final, causa_rechazo
                    else:
                        dates.append([resultado[0], resultado[1]])  # fecha_inicio, causa_rechazo
                else:
                    if type_of_day in ['ausencia', 'vacaciones']:
                        dates.append([resultado[0], resultado[1]])  # fecha_inicio, fecha_final
                    else:
                        dates.append(resultado[0])  # fecha_inicio
                
            conexion.commit()
            cursor.close()
            cerrar_db(conexion)

            return dates
    except Exception as e:
        # Manejar el error, por ejemplo, imprimir un mensaje de error
        print(f"Error al traer las fechas de la base de datos: {str(e)}")
        # Puedes devolver un valor predeterminado o None para indicar que no se pudieron obtener las fechas
        return None

    
def bring_approved(empleado):
    # Obtener fechas aprobadas para cada tipo de día
    ausencias_aprobadas = bring_date_db(empleado, "APROBADO", "ausencia")
    estudios_aprobados = bring_date_db(empleado, "APROBADO", "estudio")
    home_office_aprobados = bring_date_db(empleado, "APROBADO", "home")
    vacaciones_aprobadas = bring_date_db(empleado, "APROBADO", "vacaciones")
    
    # Retornar un diccionario anidado de fechas aprobadas
    return {
        "Ausencia": ausencias_aprobadas,
        "Estudio": estudios_aprobados,
        "Home Office": home_office_aprobados,
        "Vacaciones": vacaciones_aprobadas
    }

def obtener_feriados():
    conexion = conectar_db()
    feriados_laborables = []
    feriados_no_laborables = []

    if conexion.is_connected():
        cursor = conexion.cursor()

        try:
            # Consulta para los días feriados laborables
            consulta_laborables = "SELECT fecha_inicio, fecha_final, causa FROM dia_feriado WHERE laborable = 'SI'"
            cursor.execute(consulta_laborables)
            feriados_laborables = cursor.fetchall()

            # Consulta para los días feriados no laborables
            consulta_no_laborables = "SELECT fecha_inicio, fecha_final, causa FROM dia_feriado WHERE laborable = 'NO'"
            cursor.execute(consulta_no_laborables)
            feriados_no_laborables = cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener los feriados: {e}")

        finally:
            cursor.close()
            cerrar_db(conexion)

    return feriados_laborables, feriados_no_laborables

        

    
# Función para insertar los datos en la tabla que corresponda
def delete_date_db(date_to_delete, empleado, type_of_day):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        if type_of_day in ['home', 'estudio']:
            consulta = f"DELETE FROM dia_{type_of_day} WHERE fecha_inicio = %s AND empleado = %s"
            cursor.execute(consulta, (date_to_delete, empleado))
        if type_of_day in ['ausencia', 'vacaciones']:
            consulta = f"DELETE FROM dia_{type_of_day} WHERE fecha_inicio = %s AND empleado = %s"
            cursor.execute(consulta, (date_to_delete, empleado))

        
        conexion.commit()
        cursor.close()
        cerrar_db(conexion)

def save_home_office_db(empleado, month, days_of_week, employee_edit, area, hierarchy):
    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()

        modification_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        fechas = day_of_week_of_month(int(month), int(days_of_week))
        for fecha in fechas:
            consulta = "INSERT INTO dia_home (empleado, fecha_inicio, area, jerarquia, fecha_cambio_estado, estado, superior) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (employee_edit, fecha, area, hierarchy, modification_date, 'APROBADO', empleado)
            cursor.execute(consulta, valores)

        conexion.commit()
        cursor.close()
        cerrar_db(conexion)

def day_of_week_of_month(month, day):
    dates = []
    current_date = datetime(2024, month, 1)
    days_in_month = (current_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    while current_date <= days_in_month:
        if current_date.weekday() == day:
            dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return dates