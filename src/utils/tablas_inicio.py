from ..database.conexion import conectar_db, cerrar_db
from datetime import datetime
# Funcion para traer los cumpleaños del mes
def obtener_cumpleanios():
    cumpleanios = []

    conexion = conectar_db()

    if conexion.is_connected():
        cursor = conexion.cursor()
        # Trae la columna empleado, fecha_nacimiento de la tabla nomina donde el mes de la columna fecha_nacimiento coincide con el mes actual y a su vez tengan "SI" en la columna cuenta indicando que es empleado de la empresa
        consulta = "SELECT empleado, fecha_nacimiento FROM nomina WHERE MONTH(STR_TO_DATE(fecha_nacimiento, '%d/%m/%Y')) = MONTH(CURDATE()) AND cuenta = 'SI'"
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        # Guardo en la variable cumpleanios la fecha de cumpleaños de cada empleado
        for resultado in resultados:
            empleado = resultado[0]
            fecha_nacimiento = resultado[1]
            fecha_nacimiento_dt = datetime.strptime(fecha_nacimiento, '%d/%m/%Y')
    
            dia = fecha_nacimiento_dt.day
            mes = fecha_nacimiento_dt.month

            cumpleanios.append({'empleado': empleado, 'dia': dia, 'mes': mes})

            # Ordenar la lista por la columna 'dia'
        cumpleanios = sorted(cumpleanios, key=lambda x: x['dia'])

        cursor.close()

    cerrar_db(conexion)

    return cumpleanios

# Traer las claves por area
def obtener_claves(area):
    #Traigo los mails que puede ver cada area
    mails = mails_por_area(area)

    claves = []
    # Traigo las claves de cada mail del listado anterior
    for mail in mails:
        clave = buscar_clave_por_mail(mail)
        if clave:
            claves.extend(clave)
    return claves

# Traigo los mails por area
def mails_por_area(area):
    mails = []

    try:
        conexion = conectar_db()

        if conexion.is_connected():
            cursor = conexion.cursor()
            # Traigo los mails de la tabla de relacion claves-area que coincida con el area pasada por parametro
            consulta = "SELECT mail FROM relacion_claves_y_area WHERE area = %s"
            cursor.execute(consulta, (area,))
            resultados = cursor.fetchall()

            for resultado in resultados:
                mails.append(resultado[0])  # Agregar solo el primer elemento del resultado

            cursor.close()

    except Exception as e:
        # En caso de error se imprime lo siguiente
        print(f"Error al buscar correos electrónicos para el área {area}: {str(e)}")

    finally:
        cerrar_db(conexion)
    #print(mails)
    return mails

# Busco las claves de cada mail una vez ya se sepa los mails que puede ver cada area
def buscar_clave_por_mail(mail):
    claves = []

    try:
        conexion = conectar_db()

        if conexion.is_connected():
            cursor = conexion.cursor()
            # Traigo las columnas plataforma, mail y clave de la tabla clave donde el valor de la columna mail coincida con el mail pasado por parametro
            consulta = "SELECT plataforma, mail, clave FROM claves WHERE mail = %s"
            cursor.execute(consulta, (mail,))
            resultados = cursor.fetchall()
            # Se guarda en forma de diccionario la plataforma, mail y clave para luego ser leida en el HTML
            for resultado in resultados:
                plataforma, mail_, clave_ = resultado
                claves.append({'plataforma': plataforma, 'mail': mail_, 'clave': clave_})

            cursor.close()

    except Exception as e:
        # En caso de error se imprime lo siguiente
        print(f"Error al buscar la clave para el correo electrónico {mail}: {str(e)}")

    finally:
        cerrar_db(conexion)

    return claves
