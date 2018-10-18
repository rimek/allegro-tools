import os

from flask import Flask, jsonify, render_template, request

app = Flask('Allegro Multisearch', template_folder='web/templates/')

app.static_folder = os.path.join(app.root_path, 'web', 'static')


@app.route('/')
def index():
    # api_key = os.environ.get('ALLEGRO_API_KEY', 'no api key')
    return render_template('main.html')


@app.route('/search', methods=['POST'])
def search():
    phrases = request.form.getlist('search')

    return jsonify({'phrases': phrases})


def run(debug=True, host='0.0.0.0', port=8000):
    app.run(debug=debug, host=host, port=port)
