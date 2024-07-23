from flask import Blueprint, send_from_directory, render_template, url_for
import os

# Crea el blueprint
files_bp = Blueprint('files_bp', __name__, template_folder='templates')

# Configura la ruta donde se almacenan los archivos
current_dir = os.path.dirname(os.path.abspath(__file__))
FILE_DIRECTORY = os.path.join(current_dir, '../../static/files')

def list_items(directory):
    items = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path):
            items.append({'type': 'folder', 'name': name})
        else:
            items.append({'type': 'file', 'name': name})
    return items

@files_bp.route('/')
@files_bp.route('/<path:subdir>')
def files(subdir=''):
    directory = os.path.join(FILE_DIRECTORY, subdir)
    items = list_items(directory)
    return render_template('pages/files.html', items=items, subdir=subdir)

@files_bp.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(FILE_DIRECTORY, filename)
