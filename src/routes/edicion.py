from flask import Blueprint, session, render_template, request
from ..utils.aprobacion import obtener_dias_por_aprobar, obtener_dias_filtro, actualizar_dia 
from ..utils.date_db import bring_approved
from ..utils.recursos import obtener_recursos, obtener_info_de_recurso, actualizar_valor_recurso
import json

informacion_bp = Blueprint('informacion', __name__)
# Ruta para ir a informacion.html
@informacion_bp.route('/informacion')
def informacion():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        jerarquia = session['jerarquia']
        personal = session['personal']
        recursos = obtener_recursos()
        #print(recursos)
        dias_por_aprobar = []
        for empleado_ in personal:
            dia_por_empleado = obtener_dias_por_aprobar(empleado_)
            dias_por_aprobar.append(dia_por_empleado)
        if all(not dia_por_empleado for dia_por_empleado in dias_por_aprobar):
            dias_por_aprobar = False

        fechas_aprobadas_totales = {}
        for persona in personal:
            fechas_aprobadas = bring_approved(persona)
            fechas_aprobadas_totales[persona] = fechas_aprobadas
        fechas_aprobadas_json = json.dumps(fechas_aprobadas_totales)
        fechas_apro_fin = json.loads(fechas_aprobadas_json)
        #print(fechas_aprobadas_json)
        return render_template('pages/informacion.html', empleado = empleado, roles = roles, personal = personal, jerarquia=jerarquia, dias_por_aprobar=dias_por_aprobar, fechas_aprobadas=fechas_apro_fin, recursos=recursos)
    
aprobacion_bp = Blueprint('aprobacion', __name__)
# Ruta para ir a aprobacion.html
@aprobacion_bp.route('/aprobacion')
def aprobacion():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        jerarquia = session['jerarquia']
        personal = session['personal']
        recursos = obtener_recursos()
        #print(recursos)
        dias_por_aprobar = []
        for empleado_ in personal:
            dia_por_empleado = obtener_dias_por_aprobar(empleado_)
            dias_por_aprobar.append(dia_por_empleado)
        if all(not dia_por_empleado for dia_por_empleado in dias_por_aprobar):
            dias_por_aprobar = False

        fechas_aprobadas_totales = {}
        for persona in personal:
            fechas_aprobadas = bring_approved(persona)
            fechas_aprobadas_totales[persona] = fechas_aprobadas
        fechas_aprobadas_json = json.dumps(fechas_aprobadas_totales)
        fechas_apro_fin = json.loads(fechas_aprobadas_json)
        #print(fechas_aprobadas_json)
        return render_template('pages/aprobacion.html', empleado = empleado, roles = roles, personal = personal, jerarquia=jerarquia, dias_por_aprobar=dias_por_aprobar, fechas_aprobadas=fechas_apro_fin, recursos=recursos)
    
filtrar_dias_bp = Blueprint('filtrar_dias', __name__)
@filtrar_dias_bp.route('/filtrar_dias', methods=['GET', 'POST'])
def filtrar_dias():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']
        jerarquia = session['jerarquia']
        area = session['area']
        recursos = obtener_recursos()
        # Verificar si se recibió una solicitud POST
        if request.method == 'POST':
            empleado_ = request.form.get('empleado')
            concepto = request.form.get('concepto')
            fecha_inicio = request.form.get('fecha')
            fecha_fin = request.form.get('fecha_fin')
            print(empleado_, concepto, fecha_inicio, fecha_fin, area)
            # Obtener los días filtrados según los parámetros recibidos
            filtro_aplicado = obtener_dias_filtro(empleado_, concepto, fecha_inicio, fecha_fin, area)
            print(f"estos {filtro_aplicado}")
            # Obtener los días por aprobar para cada empleado
            dias_por_aprobar = []
            for empleado_ in personal:
                dia_por_empleado = obtener_dias_por_aprobar(empleado_)
                dias_por_aprobar.append(dia_por_empleado)
            if all(not dia_por_empleado for dia_por_empleado in dias_por_aprobar):
                dias_por_aprobar = False

            # Obtener las fechas aprobadas totales para cada empleado
            fechas_aprobadas_totales = {}
            for persona in personal:
                fechas_aprobadas = bring_approved(persona)
                fechas_aprobadas_totales[persona] = fechas_aprobadas
            fechas_aprobadas_json = json.dumps(fechas_aprobadas_totales)
            fechas_apro_fin = json.loads(fechas_aprobadas_json)

            # Renderizar la plantilla con los datos obtenidos
            return render_template('pages/aprobacion.html', empleado=empleado, roles=roles, personal=personal, jerarquia=jerarquia, dias_por_aprobar=dias_por_aprobar, fechas_aprobadas=fechas_apro_fin, dias_filtrados = filtro_aplicado, recursos=recursos)
        else:
            # Manejar el caso en que la solicitud no sea POST
            return "Método no permitido", 405

editar_dia_bp = Blueprint('editar_dia', __name__)
# Ruta para ir a editar_dia.html
@editar_dia_bp.route('/editar_dia', methods=['POST', 'GET'])
def editar_dia():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        jerarquia = session['jerarquia']
        personal = session['personal']
        recursos = obtener_recursos()
        dias_por_aprobar = []
        for empleado_ in personal:
            dia_por_empleado = obtener_dias_por_aprobar(empleado_)
            dias_por_aprobar.append(dia_por_empleado)
        if all(not dia_por_empleado for dia_por_empleado in dias_por_aprobar):
            dias_por_aprobar = False

        fechas_aprobadas_totales = {}
        for persona in personal:
            fechas_aprobadas = bring_approved(persona)
            fechas_aprobadas_totales[persona] = fechas_aprobadas
        fechas_aprobadas_json = json.dumps(fechas_aprobadas_totales)
        fechas_apro_fin = json.loads(fechas_aprobadas_json)
        #print(fechas_aprobadas_json)

        if request.method == 'POST':
            empleado_form = request.form.get('empleado')
            fecha_solicitud = request.form.get('fecha_solicitud')
            fecha_inicio = request.form.get('fecha_inicio')
            fecha_final = request.form.get('fecha_final')
            estado = request.form.get('estado')
            causa = request.form.get('causa')
            concepto = request.form.get('concepto')
            superior = request.form.get('superior')
            #print(concepto)
            actualizar_dia(empleado_form, fecha_solicitud, fecha_inicio, fecha_final, estado, causa, concepto, superior)
        return render_template('pages/aprobacion.html', empleado = empleado, roles = roles, personal = personal, jerarquia=jerarquia, dias_por_aprobar=dias_por_aprobar, fechas_aprobadas=fechas_apro_fin, recursos=recursos)
    
elegir_recurso_edit_bp = Blueprint('elegir_recurso_edit', __name__)
# Ruta para ir a elegir_recurso_edit.html
@elegir_recurso_edit_bp.route('/elegir_recurso_edit', methods=['POST'])
def elegir_recurso_edit():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        jerarquia = session['jerarquia']
        personal = session['personal']
        recursos = obtener_recursos()
        dias_por_aprobar = []
        for empleado_ in personal:
            dia_por_empleado = obtener_dias_por_aprobar(empleado_)
            dias_por_aprobar.append(dia_por_empleado)
        if all(not dia_por_empleado for dia_por_empleado in dias_por_aprobar):
            dias_por_aprobar = False

        fechas_aprobadas_totales = {}
        for persona in personal:
            fechas_aprobadas = bring_approved(persona)
            fechas_aprobadas_totales[persona] = fechas_aprobadas
        fechas_aprobadas_json = json.dumps(fechas_aprobadas_totales)
        fechas_apro_fin = json.loads(fechas_aprobadas_json)
        #print(fechas_aprobadas_json)

        if request.method == 'POST':
            recurso_a_editar = request.form.get('recurso_id')[2:7]
            causa = request.form.get('causa')
            recurso_ = obtener_info_de_recurso(recurso_a_editar, causa)
        return render_template('pages/informacion.html', empleado = empleado, roles = roles, personal = personal, jerarquia=jerarquia, dias_por_aprobar=dias_por_aprobar, fechas_aprobadas=fechas_apro_fin, recursos=recursos, recurso_=recurso_)
    
editar_recurso_bp = Blueprint('editar_recurso', __name__)
# Ruta para ir a editar_recurso.html
@editar_recurso_bp.route('/editar_recurso', methods=['POST'])
def editar_recurso():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        jerarquia = session['jerarquia']
        personal = session['personal']
        recursos = obtener_recursos()
        dias_por_aprobar = []
        for empleado_ in personal:
            dia_por_empleado = obtener_dias_por_aprobar(empleado_)
            dias_por_aprobar.append(dia_por_empleado)
        if all(not dia_por_empleado for dia_por_empleado in dias_por_aprobar):
            dias_por_aprobar = False

        fechas_aprobadas_totales = {}
        for persona in personal:
            fechas_aprobadas = bring_approved(persona)
            fechas_aprobadas_totales[persona] = fechas_aprobadas
        fechas_aprobadas_json = json.dumps(fechas_aprobadas_totales)
        fechas_apro_fin = json.loads(fechas_aprobadas_json)
        #print(fechas_aprobadas_json)
        if request.method == 'POST':
            id_recurso = request.form.get('id')
            form_data = request.form.to_dict()
            form_data.pop('csrf_token', None)
            print(id_recurso)
            for key, value in form_data.items():
                actualizar_valor_recurso(id_recurso, key, value)
                #print(f"Campo: {key}, Valor: {value}")

        return render_template('pages/informacion.html', empleado = empleado, roles = roles, personal = personal, jerarquia=jerarquia, dias_por_aprobar=dias_por_aprobar, fechas_aprobadas=fechas_apro_fin, recursos=recursos)