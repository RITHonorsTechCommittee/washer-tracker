from collections import defaultdict
from time import time
from typing import Dict, NoReturn

from flask.app import Flask
from flask.globals import request
from flask.templating import render_template

from sensor import Sensor, WasherState


class QRSensor(Sensor):
    # {cycle name: time in seconds}
    CYCLES: Dict[str, int] = {
        'WASHER_PERM_PRESS': 24 * 60,
        'WASHER_COOL': 27 * 60,

        'DRYER_DELICATES': 40 * 60,
        'DRYER_MEDIUM': 42 * 60
    }

    def __init__(self) -> NoReturn:
        # {washer id: finish time}
        self.washers: Dict[int, int] = defaultdict(lambda: -1)

    def register(self, app: Flask) -> NoReturn:
        def scan(washer_id: int) -> str:
            if request.method == 'POST':
                data: Dict = request.get_json()

                new_state: WasherState = WasherState[data['state']]
                if new_state == WasherState.RUNNING:
                    end_time: int = time() + self.CYCLES[data['cycle']]
                    self.washers[washer_id] = end_time
                elif new_state == WasherState.EMPTY:
                    # set to magic "empty" number
                    self.washers[washer_id] = -1

                return 'ok'
            else:  # request.method == 'GET'
                return render_template('scan.html')

        app.add_url_rule('/scan/<int:washer_id>', 'scan', scan, methods=['GET', 'POST'])

    def get_washer(self, id: int) -> WasherState:
        try:
            if self.washers[id] == -1:  # magic "empty" number
                return WasherState.EMPTY
            if time() > self.washers[id]:  # done but not emptied yet
                return WasherState.FULL
            else:  # still running
                return WasherState.RUNNING
        except KeyError:
            return WasherState.EMPTY
