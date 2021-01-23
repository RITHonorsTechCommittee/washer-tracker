from typing import Dict
from flask.templating import render_template
from sensors import QRSensor
from flask.json import jsonify
from sensor import Sensor
from laundromat import Laundromat, MachineState

from flask import Flask


laundromats: Dict[str, Laundromat] = {
    'Gibson': Laundromat.create('Gibson', 8, 8),
    'Sol': Laundromat.create('Sol', 20, 20),
    'Ellingson': Laundromat.create('Ellingson', 20, 20),
    'Gleason': Laundromat.create('Gleason', 22, 22)
}

app: Flask = Flask(__name__)

sensor: Sensor = QRSensor()
sensor.register(app, laundromats)


@app.route('/', methods=['GET'])
def index() -> str:
    return render_template('index.html', **{
        'washers': laundromats['Gibson'].washers,
        'MachineState': MachineState  # lets us use enum equality checks
    })


@app.route('/washers', methods=['GET'])
def washers() -> str:
    return jsonify({k: v.name for k, v in laundromats['Gibson'].washers.items()})


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
