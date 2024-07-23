# Importaciones
from flask import Blueprint, render_template, session
from ..utils.tablas_inicio import obtener_cumpleanios, obtener_claves
from ..utils.date_db import bring_approved, obtener_feriados
import json

# Crea un objeto Blueprint
inicio_bp = Blueprint('inicio', __name__)

# Define la ruta para la página de inicio de sesión
@inicio_bp.route('/inicio')
def inicio():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        area = session['area']
        jerarquia = session['jerarquia']
        personal = session['personal']
        print(roles)
        cumpleanios = obtener_cumpleanios()
        claves = obtener_claves(area)
        fechas_aprobadas_totales = {}
        # Verificar si personal es una lista
        if isinstance(personal, list):
            for persona in personal:
                fechas_aprobadas = bring_approved(persona)
                fechas_aprobadas_totales[persona] = fechas_aprobadas
        else:
            fechas_aprobadas = bring_approved(personal)
            fechas_aprobadas_totales[personal] = fechas_aprobadas

        fechas_aprobadas_json = json.dumps(fechas_aprobadas_totales)
        #print(fechas_aprobadas_json)
        feriados = obtener_feriados()
        print(feriados)

        return render_template('pages/inicio.html', empleado=empleado, roles=roles, cumpleanios=cumpleanios, area=area, claves=claves, fechas_aprobadas=fechas_aprobadas_json, jerarquia=jerarquia)