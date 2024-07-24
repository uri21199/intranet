# Importaciones
from flask import Blueprint, session, request, redirect, url_for
from ..utils.aprobacion import aprobar_dias, eliminar_dias

# Se crea la ruta resources
aprobar_solicitud_bp = Blueprint('aprobar_solicitud', __name__)
@aprobar_solicitud_bp.route('/aprobar_solicitud', methods=['GET', 'POST'])
def aprobar_solicitud():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']

        if request.method == 'POST':
            solicitudes = request.form.getlist('solicitudes')
            for solicitud in solicitudes:
                empleado_sol, fecha, concepto = solicitud.split('|')
                
                if concepto == 'Home Office':
                    concepto = 'dia_home'
                elif concepto == 'Día de estudio':
                    concepto = "dia_estudio"
                elif concepto == 'Vacaciones':
                    concepto = "dia_vacaciones"
                elif concepto == 'Ausencia':
                    concepto = "dia_ausencia"
                
                aprobar_dias(empleado_sol, fecha, concepto, empleado)

            # Redirigir a una página de confirmación o a la misma página de origen
            return redirect(url_for('aprobacion.aprobacion'))
        else:
            return "Método no permitido", 405

    # Se crea la ruta resources
eliminar_solicitud_bp = Blueprint('eliminar_solicitud', __name__)
@eliminar_solicitud_bp.route('/eliminar_solicitud', methods=['GET', 'POST'])
def eliminar_solicitud():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']
        if request.method == 'POST':
            # Obtener los datos del formulario
            empleado_sol = request.form.get('empleado')
            fecha = request.form.get('fecha')
            concepto = request.form.get('concepto')
            if concepto == 'Home Office':
                concepto = 'dia_home'
            elif concepto == 'Día de estudio':
                concepto = "dia_estudio"
            elif concepto == 'Vacaciones':
                concepto = "dia_vacaciones" 
            elif concepto == 'Ausencia':
                concepto = "dia_ausencia"
            # Realizar la lógica de aprobación aquí
            eliminar_dias(empleado_sol, fecha, concepto, empleado)
            # Redirigir a una página de confirmación o a la misma página de origen
            return redirect(url_for('aprobacion.aprobacion'))
        else:
            # Manejar el caso en que la solicitud no sea POST
            return "Método no permitido", 405