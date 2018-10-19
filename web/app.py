import json
import os
from json import JSONEncoder

from flask import Flask, jsonify, render_template, request
from multisearch import MultiSearch

app = Flask('Allegro Multisearch', template_folder='web/templates/')

app.static_folder = os.path.join(app.root_path, 'web', 'static')



@app.route('/')
def index():
    # api_key = os.environ.get('ALLEGRO_API_KEY', 'no api key')
    return render_template('main.html')


@app.route('/search', methods=['POST'])
def search():
    # phrases = request.form.getlist('search')
    # phrases = list(filter(None, [item.get('search') for item in request.json]))
    phrases = list(filter(None, request.json))


    try:
        api_key = os.environ['ALLEGRO_API_KEY']
    except KeyError:
        return json.dumps('No API key provided'), 404

    tool = MultiSearch(api_key=api_key)
    tool.fetch_results({'search': phrases})
    items = tool.match_uid()


    res = {}
    for uid, its in items.items():
        res[uid] = [i._data for i in its]

    return jsonify(res)


def run(debug=True, host='0.0.0.0', port=8000):
    app.run(debug=debug, host=host, port=port)
