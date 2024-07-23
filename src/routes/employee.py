# Importaciones
from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from ..utils.obtener_empleado import get_employee_data
from ..utils.save_employee import save_info_employee_db, save_new_employee_db
from ..utils.aprobacion import obtener_dias_por_aprobar
from ..utils.date_db import bring_approved
import json

#Creación de ruta para elegir el empleado
choose_employee_bp = Blueprint('choose_employee', __name__)

@choose_employee_bp.route('/choose_employee', methods=['POST'])
def choose_employee():
    if request.method == 'POST':
        chosen_employee = request.form.get('employee')

        if chosen_employee:
            if 'user' in session:
                empleado = session['empleado']
                roles = session['roles']
                personal = session['personal']
                jerarquia = session['jerarquia']
                info_employee = get_employee_data(chosen_employee)
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

                return render_template('pages/informacion.html', empleado = empleado, roles = roles, personal = personal, jerarquia=jerarquia, info_employee=info_employee, dias_por_aprobar=dias_por_aprobar, fechas_aprobadas=fechas_apro_fin)
            
#Creación de ruta para guardar la información cambiada del empleado        
save_info_employee_bp = Blueprint('save_info_employee', __name__)
@save_info_employee_bp.route('/save_info_employee', methods=['POST'])
def save_info_employee():
    if request.method == 'POST':
        empleado_a_editar = request.form.get('empleado')
        cuil = request.form.get('cuil')
        fecha_ingreso = request.form.get('fecha_ingreso')
        legajo = request.form.get('legajo')
        mail = request.form.get('mail')
        forma = request.form.get('forma')
        turno = request.form.get('turno')
        area = request.form.get('area')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        categoria = request.form.get('categoria')
        convenio = request.form.get('convenio')
        medife = request.form.get('medife')

        save_info_employee_db(empleado_a_editar, cuil, fecha_ingreso, legajo, mail, forma, turno, area, fecha_nacimiento, categoria, convenio, medife)

    return redirect(url_for('edicion.edicion'))

#Creación de ruta para guardar la información del empleado nuevo       
save_new_employee_bp = Blueprint('save_new_employee', __name__)
@save_new_employee_bp.route('/save_new_employee', methods=['POST'])
def save_new_employee():
    if request.method == 'POST':
        empleado_nuevo = request.form.get('empleado')
        cuil = request.form.get('cuil')
        fecha_ingreso = request.form.get('fecha_ingreso')
        fecha_ingreso_dt = datetime.strptime(fecha_ingreso, '%Y-%m-%d')
        fecha_ingreso_formateada = fecha_ingreso_dt.strftime('%d/%m/%Y')
        finaliza_pp = fecha_ingreso_dt + timedelta(days=3*30)
        finaliza_pp_str = finaliza_pp.strftime('%Y-%m-%d')
        finaliza_pp_formateada = finaliza_pp.strftime('%d/%m/%Y')
        legajo = request.form.get('legajo')
        mail = request.form.get('mail')
        cuenta = 'SI'
        genero = request.form.get('genero')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        fecha_nacimiento_dt = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        fecha_nacimiento_formateada = fecha_nacimiento_dt.strftime('%d/%m/%Y')
        forma = request.form.get('forma')
        turno = request.form.get('turno')
        area = request.form.get('area')
        jerarquia = request.form.get('jerarquia')
        categoria = request.form.get('categoria')
        convenio = request.form.get('convenio')
        medife = request.form.get('medife')
        roles_seleccionados = request.form.getlist('roles[]')

        save_new_employee_db(empleado_nuevo, cuil, fecha_ingreso_formateada, finaliza_pp_formateada, legajo, mail, cuenta, genero, fecha_nacimiento_formateada, forma, turno, area, jerarquia, categoria, convenio, medife, roles_seleccionados)
        flash('¡Empleado guardado correctamente!', 'success')

    return redirect(url_for('edicion.edicion'))



