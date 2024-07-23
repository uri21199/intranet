from flask import Blueprint, session, render_template, request, redirect, url_for
from ..utils.sistemas import guardar_reporte_a_sistemas, obtener_reportes_a_sistemas, actualizar_ticket, obtener_empleados_sistemas, obtener_tickets_sistemas
from ..utils.outlook import enviar_correo
# Se crea la ruta resources
sistemas_bp = Blueprint('sistemas', __name__)

@sistemas_bp.route('/sistemas')
def sistemas():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']
        area = session['area']
        reportes_a_sistemas = obtener_reportes_a_sistemas()
        empleados_sistemas = obtener_empleados_sistemas()
        obtener_tickets = obtener_tickets_sistemas(empleado)
        
        return render_template('pages/sistemas.html', empleado = empleado, roles = roles, personal = personal, area=area, reportes_a_sistemas=reportes_a_sistemas, empleados_sistemas=empleados_sistemas, obtener_tickets=obtener_tickets)
    
reportar_a_sistemas_bp = Blueprint('reportar_a_sistemas', __name__)
@reportar_a_sistemas_bp.route('/reportar_a_sistemas', methods=['GET', 'POST'])
def reportar_a_sistemas():
    if 'user' in session:
        empleado = session['empleado']
        if request.method == 'POST':
            categoria = request.form.get('categoria')
            subcategoria = request.form.get('subcategoria')
            tipo_problema = request.form.get('tipo_problema')
            descripcion_problema = request.form.get('descripcion_problema')
            id_equipo = request.form.get('id_equipo')

            guardar_reporte_a_sistemas(categoria, subcategoria, tipo_problema, descripcion_problema, id_equipo, empleado)

            # Llamar a la función para enviar el correo electrónico
            enviar_correo(categoria, subcategoria, tipo_problema, descripcion_problema, id_equipo, empleado)

            return redirect(url_for('sistemas.sistemas'))
        
        return redirect(url_for('sistemas.sistemas'))
    else:
        return redirect(url_for('login'))

modificar_ticket_bp = Blueprint('modificar_ticket', __name__)
@modificar_ticket_bp.route('/modificar_ticket/<int:id>', methods=['POST'])
def modificar_ticket(id):
    if request.method == 'POST':
        estado = request.form.get('estado')
        prioridad = request.form.get('prioridad')
        reportado_a = request.form.get('reportado_a')

        if estado == 'Cerrado':
            actualizar_ticket(id, estado, prioridad, reportado_a, cerrado='Si')
        else:
            actualizar_ticket(id, estado, prioridad, reportado_a, cerrado=False)

        return redirect(url_for('sistemas.sistemas'))
    else:
        pass

empleado_notificado_bp = Blueprint('empleado_notificado', __name__)
@empleado_notificado_bp.route('/empleado_notificado', methods=['POST'])
def empleado_notificado():
    if request.method == 'POST':
        id = request.form.get('id')
        estado = request.form.get('estado')
        prioridad = request.form.get('prioridad')
        reportado_a = request.form.get('reportado_a')

        actualizar_ticket(id, estado, prioridad, reportado_a, cerrado='Fin')
        return redirect(url_for('sistemas.sistemas'))
    else:
        pass