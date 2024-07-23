# Importaciones
from flask import Flask, render_template
from src.routes.login import login_bp
from src.routes.logout import logout_bp
from src.routes.inicio import inicio_bp
from src.routes.edicion import informacion_bp, aprobacion_bp, filtrar_dias_bp, editar_dia_bp, elegir_recurso_edit_bp, editar_recurso_bp
from src.routes.configuracion import configuracion_bp, save_pass_bp
from src.routes.documentos import documentos_bp
from src.routes.save_date import save_date_bp, delete_date_bp, save_home_office_bp
from src.routes.days import estudio_bp, home_bp, ausencia_bp, vacaciones_bp
from src.routes.employee import choose_employee_bp, save_info_employee_bp, save_new_employee_bp
from src.routes.recursos import recursos_bp
from src.routes.descargas import descargas_bp, descargar_bp, descargar_nov_mens_bp
from src.routes.sistemas import sistemas_bp, reportar_a_sistemas_bp, modificar_ticket_bp, empleado_notificado_bp
from src.routes.resolucion_sol import aprobar_solicitud_bp, eliminar_solicitud_bp
from src.routes.rrhh import rrhh_bp
from src.routes.files import files_bp
from src.utils.before_request import before_request

# Configuración de app
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = False
app.config['SESSION_KEY_PREFIX'] = 'intranet'
app.secret_key = 'embrace_intranet'

# Registra el Blueprint en la aplicación
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(inicio_bp)
app.register_blueprint(informacion_bp)
app.register_blueprint(aprobacion_bp)
app.register_blueprint(estudio_bp)
app.register_blueprint(home_bp)
app.register_blueprint(ausencia_bp)
app.register_blueprint(vacaciones_bp)
app.register_blueprint(configuracion_bp)
app.register_blueprint(documentos_bp)
app.register_blueprint(save_pass_bp)
app.register_blueprint(save_date_bp)
app.register_blueprint(delete_date_bp)
app.register_blueprint(save_home_office_bp)
app.register_blueprint(choose_employee_bp)
app.register_blueprint(save_info_employee_bp)
app.register_blueprint(save_new_employee_bp)
app.register_blueprint(recursos_bp)
app.register_blueprint(elegir_recurso_edit_bp)
app.register_blueprint(descargas_bp)
app.register_blueprint(descargar_bp)
app.register_blueprint(descargar_nov_mens_bp)
app.register_blueprint(sistemas_bp)
app.register_blueprint(reportar_a_sistemas_bp)
app.register_blueprint(modificar_ticket_bp)
app.register_blueprint(empleado_notificado_bp)
app.register_blueprint(aprobar_solicitud_bp)
app.register_blueprint(eliminar_solicitud_bp)
app.register_blueprint(filtrar_dias_bp)
app.register_blueprint(editar_dia_bp)
app.register_blueprint(editar_recurso_bp)
app.register_blueprint(rrhh_bp)
app.register_blueprint(files_bp, url_prefix='/files')
app.before_request(before_request)

# Ruta inicial de la app
@app.route('/')
def index():
    return render_template('pages/index.html')

# Inicio de app
if __name__ == '__main__':
    app.run(port=8080)  # Cambia el número de puerto según sea necesario

