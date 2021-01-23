from threading import Timer
from laundromat import Laundromat, MachineState
from time import time
from typing import Dict, NoReturn

from flask.app import Flask
from flask.globals import request

from sensor import Sensor


class VibrationSensor(Sensor):
    TIMEFRAME: int = 30  # seconds before washer is considered empty

    def __init__(self) -> NoReturn:
        self.timers: Dict[str, Timer] = dict()

    def register(self, app: Flask, laundromats: Dict[str, Laundromat]) -> NoReturn:
        def vibrate() -> str:
            data: Dict = request.get_json()

            laundromat: Laundromat = laundromats[data['laundromat']]
            laundromat.set_washer(data['washer_id'], MachineState.RUNNING)

            # stop previous timer, if one exists
            old_timer: Timer = self.timers.get(laundromat.name + data['washer_id'], None)
            if old_timer is not None:
                old_timer.cancel()

            timer: Timer = Timer(self.TIMEFRAME, lambda: laundromat.set_washer(data['washer_id'], MachineState.EMPTY))
            self.timers[laundromat.name + data['washer_id']] = timer  # TODO: support dryers (overlap between washer #1 and dryer #1)
            timer.start()

            return 'ok'
        
        app.add_url_rule('/vibrate', 'vibrate', vibrate, methods=['POST'])

