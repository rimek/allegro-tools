from flask import Flask, request

app = Flask('Allegro Multisearch')


@app.route('/')
def index():
    return 'index'


@app.route('/search', methods=['POST'])
def search():
    res = 'search for the '
    for val in request.form['search']:
        res += val + ' | '

    return res

def run(debug=True, host='0.0.0.0', port=9000):
    app.run(debug=debug, host=host, port=port)
