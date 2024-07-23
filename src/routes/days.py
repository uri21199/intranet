from flask import Blueprint, session, render_template
from ..utils.date_db import bring_date_db

#Función que será reutilizada para traer el empleado, roles y personal. También traerá los dias aprobados, rechazados y solicitados de las distintas tablas de la base de datos. Se pasarán los valores que corresponda a través del render_template.
def get_data_and_render_template(template_name, type_of_day):
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']
        approved = bring_date_db(empleado, 'APROBADO', type_of_day)
        rejected = bring_date_db(empleado, 'RECHAZADO', type_of_day)
        required = bring_date_db(empleado, 'SOLICITADO', type_of_day)
        return render_template(template_name, empleado=empleado, roles=roles, personal=personal, rejected_days=rejected, approved_days=approved, waiting_days=required, type_of_day = type_of_day)

# Creación de ruta de estudio
estudio_bp = Blueprint('estudio', __name__)
@estudio_bp.route('/estudio')
def estudio():
    return get_data_and_render_template('pages/estudio.html', 'estudio')

# Creación de ruta de home
home_bp = Blueprint('home', __name__)
@home_bp.route('/home')
def home():
    return get_data_and_render_template('pages/home.html', 'home')

# Creación de ruta de ausencia
ausencia_bp = Blueprint('ausencia', __name__)
@ausencia_bp.route('/ausencia')
def ausencia():
    return get_data_and_render_template('pages/ausencia.html', 'ausencia')

vacaciones_bp = Blueprint('vacaciones', __name__)
@vacaciones_bp.route('/vacaciones')
def vacaciones():
    return get_data_and_render_template('pages/vacaciones.html', 'vacaciones')
