import os

from flask import Flask, render_template, request, jsonify

app = Flask('Allegro Multisearch', template_folder='web/templates/')

app.static_folder = os.path.join(app.root_path, 'web', 'static')



@app.route('/')
def index():
    return render_template('main.html')


@app.route('/search', methods=['POST'])
def search():
    phrases = request.form.getlist('search')

    return jsonify({'phrases': phrases})


def run(debug=True, host='0.0.0.0', port=9000):
    app.run(debug=debug, host=host, port=port)
