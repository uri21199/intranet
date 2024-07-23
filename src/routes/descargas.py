# Importaciones
from flask import Blueprint, session, render_template, request, send_file
from src.utils.descargas import descargar_nomina, descargar_nomina_bajas, descargar_inventario_recursos, obtener_dias_empleado, generar_excel
from openpyxl import Workbook
from io import BytesIO
# Se crea la ruta resources
descargas_bp = Blueprint('descargas', __name__)

@descargas_bp.route('/descargas')
def descargas():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']
        print(personal)
        return render_template('pages/descargas.html', empleado = empleado, roles = roles, personal = personal)

descargar_bp = Blueprint('descargar', __name__)
@descargar_bp.route('/descargar')    
def descargar():
    # Obtener el parámetro 'accion' de la URL
    accion = request.args.get('accion')
    personal = session['personal']
    area = session['area']
    # Determinar qué acción realizar según el valor del parámetro 'accion'
    if accion == 'nomina':
        return descargar_nomina(personal)
    elif accion == 'nomina_bajas':
        return descargar_nomina_bajas(area)
    elif accion == 'inventario_recursos':
        return descargar_inventario_recursos()
    else:
        # Acción no válida, redirigir a alguna página de error o manejarla de otra manera
        return 'Acción no válida'
    
descargar_nov_mens_bp = Blueprint('descargar_nov_mens', __name__)
@descargar_nov_mens_bp.route('/descargar_nov_mens', methods=['GET', 'POST'])    
def descargar_nov_mens():
    personal = session.get('personal', [])
    mes = int(request.form.get('mes'))
    print(personal)
    novedades = []

    for empleado in personal:
        novedades.append(obtener_dias_empleado(empleado, mes))

    output = generar_excel_novs(novedades)

    # Devolver el archivo Excel como respuesta
    return send_file(
        output,
        as_attachment=True,
        download_name="novedades_mensuales.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def generar_excel_novs(novedades):
    # Crear un nuevo libro de trabajo
    wb = Workbook()
    # Seleccionar la primera hoja del libro de trabajo
    ws = wb.active
    # Establecer los encabezados de las columnas
    ws.append(['Empleado', 'Fecha Inicio', 'Fecha Final', 'Estado', 'Concepto', ' Causa', 'Fecha solicitud', 'Fecha cambio de estado', 'Superior', 'Area'])
    
    for lista_novedades in novedades:
        for novedad in lista_novedades:
            concepto = novedad.get('concepto', '')
            empleado = novedad.get('empleado', '')
            if concepto in ['dia_ausencia', 'dia_vacaciones']:
                fecha_inicio = novedad.get('fecha_inicio', '')
                fecha_final = novedad.get('fecha_final', '')
                estado = novedad.get('estado', '')
            elif concepto in ['dia_home', 'dia_estudio']:
                fecha_inicio = novedad.get('fecha_inicio', '')
                fecha_final = ''
                estado = novedad.get('estado', '')
            fecha_solicitud = novedad.get('fecha_solicitud', '')
            fecha_cambio_estado = novedad.get('fecha_cambio_estado', '')
            superior = novedad.get('superior', '')
            area = novedad.get('area', '')
            causa = novedad.get('causa', '')
            if concepto == 'dia_ausencia':
                concepto = 'Ausencia'
            elif concepto == 'dia_vacaciones':
                concepto = 'Vacaciones'
            elif concepto == 'dia_home':
                concepto = 'Home Office'
            elif concepto == 'dia_estudio':
                concepto = 'Estudio'

            # Agregar una fila con los datos de la novedad actual
            ws.append([empleado, fecha_inicio, fecha_final, estado, concepto, causa, fecha_solicitud, fecha_cambio_estado, superior, area])

    # Crear un objeto de bytes en memoria para almacenar el archivo Excel
    output = BytesIO()
    # Guardar el libro de trabajo en el objeto de bytes
    wb.save(output)
    # Reiniciar el cursor del objeto de bytes al inicio para permitir su lectura
    output.seek(0)

    return output

