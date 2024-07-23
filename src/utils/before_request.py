# Importaciones
from flask import session
from src.utils.obtener_empleado import obtener_empleado, obtener_area, obtener_jerarquia, obtener_roles_empleado, obtener_personal, obtener_areas_por_empleado, obtener_personal_por_areas

# Se guardan estas variables en la sesion para ser reutilizada en otras secciones
def before_request():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        session['empleado'] = empleado
        area = obtener_area(usuario)
        session['area'] = area
        jerarquia = obtener_jerarquia(usuario)
        session['jerarquia'] = jerarquia
        roles = obtener_roles_empleado(empleado)
        session['roles'] = roles
        if jerarquia == '1':
            personal = session['empleado']
        # Si la jerarquia es 2 o 3 se va a traer el personal por area y menor a la jerarquia
        elif jerarquia in ['2', '3']:
            personal = obtener_personal(area, jerarquia)
        # Si la jerarquia es 4 significa que es responsable de area por lo que va a traer todos los empleados de las areas que dependen de dicha persona
        elif jerarquia == '4':
            employees_for_area = []
            areas_empleado = obtener_areas_por_empleado(empleado)
            employees_for_area.extend(obtener_personal_por_areas(areas_empleado))
            personal = employees_for_area
        # Sino trae todo el personal
        elif jerarquia == '5' or 'rrhh' in roles:
            personal = obtener_personal()
        else:
            personal = []
        session['personal'] = personal
        #print(session['personal'])