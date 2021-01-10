from collections import defaultdict
from time import time
from typing import Dict, NoReturn

from flask.app import Flask
from flask.globals import request

from sensor import Sensor, WasherState


class VibrationSensor(Sensor):
    TIMEFRAME: int = 30  # seconds before washer is considered empty

    def __init__(self) -> NoReturn:
        self.washers: Dict[int, int] = defaultdict(int)

    def register(self, app: Flask) -> NoReturn:
        def vibrate() -> str:
            data: Dict = request.get_json()
            # add "seconds since epoch" to data
            self.washers[int(data['washer_id'])] = int(time())
            return 'ok'
        app.add_url_rule('/vibrate', 'vibrate', vibrate, methods=['POST'])

    def get_washer(self, id: int) -> WasherState:
        try:
            last_vibration: int = self.washers[id]
            if time() - last_vibration < self.TIMEFRAME:
                return WasherState.FULL
            else:
                return WasherState.EMPTY
        except KeyError:
            return WasherState.EMPTY
