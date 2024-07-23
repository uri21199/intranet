# Importaciones
from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from ..utils.guardar_contrasena import verify_pass, change_pass, secure_pass

# Se crea la ruta configuracion
configuracion_bp = Blueprint('configuracion', __name__)

@configuracion_bp.route('/configuracion')
def configuracion():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']

        return render_template('pages/configuracion.html', empleado = empleado, roles = roles, personal = personal)

# Se crea la ruta para guardar la contraseña
save_pass_bp = Blueprint('save_pass', __name__)
@save_pass_bp.route('/save_pass', methods=['POST'])
def save_pass():
    if 'user' in session:
        empleado = session['empleado']
        old_pass = request.form['oldPass']
        new_pass = request.form['newPass']
        confirm_pass = request.form['confirmPass']

        # Se verifica la contraseña
        if verify_pass(empleado, old_pass):
            # La contraseña nueva tiene que coincidir en los dos campos que se ingreso
            if new_pass == confirm_pass:
                # Verificación de si la contraseña cumple la seguridad establecida
                if secure_pass(new_pass):
                    # Si se cambio la contraseña y cumple se guarda
                    if change_pass(empleado, new_pass):
                        flash('Se guardó con éxito', 'success')
                        return redirect(url_for('configuracion.configuracion'))
                    else:
                        return "Error al cambiar la contraseña"
                else:
                    return "La nueva contraseña no cumple con los requisitos de seguridad"                
            else:
                return "Las contraseñas no coinciden"
        else:
            return "La contraseña actual es incorrecta"
        
    else:
        return redirect(url_for('index'))