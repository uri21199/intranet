# Importaciones
from flask import Blueprint, session, render_template
from ..utils.recursos import obtener_recursos_empleado

# Se crea la ruta resources
recursos_bp = Blueprint('recursos', __name__)
@recursos_bp.route('/recursos')
def recursos():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']
        recurso_asignado = obtener_recursos_empleado(empleado)
        
        return render_template('pages/recursos.html', empleado = empleado, roles = roles, personal = personal, recurso_asignado=recurso_asignado)