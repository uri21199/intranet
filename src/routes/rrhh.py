# Importaciones
from flask import Blueprint, session, render_template
# Se crea la ruta resources
rrhh_bp = Blueprint('rrhh', __name__)
@rrhh_bp.route('/rrhh')
def rrhh():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']
        
        return render_template('pages/rrhh.html', empleado = empleado, roles = roles, personal = personal)