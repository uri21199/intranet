# logout.py

from flask import Blueprint, session, render_template

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout')
def logout():
    # Eliminar la sesión del usuario
    session.pop('user', None)
    # Redirigir a la página de inicio, ajusta la redirección según tu estructura de rutas
    return render_template('pages/index.html')
