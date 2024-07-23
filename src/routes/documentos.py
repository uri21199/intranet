from flask import Blueprint, session, render_template, request, flash, redirect, url_for

documentos_bp = Blueprint('documentos', __name__)
@documentos_bp.route('/documentos')
def documentos():
    if 'user' in session:
        empleado = session['empleado']
        roles = session['roles']
        personal = session['personal']
        lista_documentos = [
            {"nombre": "Assisto Paraguay - CCGG", "enlace": "https://drive.google.com/drive/folders/1IOMGhMxwCk4HoPfHlT1HcKomMinD_R9b"},
            {"nombre": "Assist 365 - Login", "enlace": "https://docs.google.com/document/d/1YrkLYWA5CdY9KjGcko6mPbJdEDWWRXhzY83KZJGaviU/edit"},
            
            # Agrega más documentos aquí si es necesario
        ]


        return render_template('pages/documentos.html', empleado = empleado, roles = roles, personal = personal, lista_documentos=lista_documentos)