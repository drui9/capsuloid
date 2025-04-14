import os
import secrets
from flask import (
    Flask,
    request,
    render_template,
    render_template_string
)

app = Flask(__name__)

# configuration
app.config['SECRET_KEY'] = secrets.token_hex(16).upper()
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

artists = [
    'Taylor Swift',
    'Katty Perry',
    'Celine Dion',
    'Mark Ronson',
    'Magic',
    'Drake',
    'Popcaan',
]

@app.route('/search')
def search():
    q = request.args.get('q', ' ')
    results = [i for i in artists if q in i]
    return render_template_string('''
    {% for res in r %}
        <td>
            <tr>{{ loop.index }}</tr>
            <tr>{{ res }}</tr>
        </td>
    {% endfor %}
    ''', r=results)

if __name__ == '__main__':
    dl_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(dl_folder):
        os.mkdir(dl_folder)
    app.run(debug=True, port=8000)

