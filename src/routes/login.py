from flask import Blueprint, redirect, url_for, request, session
from ..utils.autenticacion import autenticar_usuario

# Crea un objeto Blueprint
login_bp = Blueprint('login', __name__)

# Define la ruta para la página de inicio de sesión
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Traer el email y password ingresado en el portal
    if request.method == 'POST':
        email = request.form.get('email') 
        password = request.form.get('password')

        # Realizar la autenticación de datos
        if autenticar_usuario(email, password):
            session['user'] = email
            return redirect(url_for('inicio.inicio'))
        else:
            print("Credenciales incorrectas")
            return redirect(url_for('index'))
    else:
        # Si la solicitud es GET, simplemente renderiza el formulario de inicio de sesión
        return redirect(url_for('index'))

