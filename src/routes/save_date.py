# Importaciones
from flask import Blueprint, session, request, url_for, redirect
from ..utils.date_db import save_date_db, delete_date_db, save_home_office_db

#Creación de ruta para guardar las fechas cargadas
save_date_bp = Blueprint('save_date', __name__)

@save_date_bp.route('/save_date', methods=['POST'])
def save_date():
    if 'user' in session:
        empleado = session['empleado']
        area = session['area']
        jerarquia = session['jerarquia']

        type_of_day = request.form.get('typeOfDay')
        # Si el tipo de dia pedido es "ausencia" hay que tomar dos valores: startDate y endDate. Se realiza un condicional para esto
        if type_of_day in ['estudio', 'home']:
            date = request.form['requestedDay']
            save_date_db(empleado, date, area, jerarquia, type_of_day)
        if type_of_day in ['ausencia', 'vacaciones']:
            date = request.form['startDate']
            if type_of_day == 'ausencia':
                if request.form['endDate'] == '':
                    date_end = date
                else:
                    date_end = request.form['endDate']
            else:
                date_end = request.form['endDate']
            if type_of_day == 'ausencia':
                type_absent = request.form['typeAbsent']
                save_date_db(empleado, date, area, jerarquia, type_of_day, date_end=date_end, type_absent=type_absent)
            else:
                type_absent = ''
                save_date_db(empleado, date, area, jerarquia, type_of_day, date_end=date_end, type_absent=type_absent)



    # Redirección a la ruta de la que viene
    return redirect(f'/{type_of_day}')

delete_date_bp = Blueprint('delete_date', __name__)

@delete_date_bp.route('/delete_date', methods=['POST'])
def delete_date():
    if 'user' in session:
        empleado = session['empleado']

    if request.method == 'POST':
        date_to_delete = request.form.get('date')
        type_of_day = request.form.get('typeOfDay')

        delete_date_db(date_to_delete, empleado, type_of_day)
    
    return redirect(f'/{type_of_day}')

save_home_office_bp = Blueprint('save_home_office', __name__)

@save_home_office_bp.route('/save_home_office', methods=['POST'])
def save_home_office():
    if 'user' in session:
        empleado = session['empleado']

        month = request.form['month']
        days_of_week = request.form['daysOfWeek']
        employee_edit = request.form['employee_edit']
        area = request.form['area']
        hierarchy = request.form['hierarchy']

        save_home_office_db(empleado, month, days_of_week, employee_edit, area, hierarchy)
    
    # Aquí puedes devolver una respuesta o redirigir a otra página
    return redirect(url_for('edicion.edicion'))
