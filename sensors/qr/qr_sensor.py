from threading import Timer
from time import time
from typing import Dict, List, NoReturn

from flask.app import Flask
from flask.globals import request
from flask.templating import render_template

from sensor import Sensor
from laundromat import MachineState, Laundromat


class QRSensor(Sensor):
    # {cycle name: time in seconds}
    CYCLES: Dict[str, int] = {
        'WASHER_PERM_PRESS': 24 * 60,
        'WASHER_COOL': 27 * 60,

        'DRYER_DELICATES': 40 * 60,
        'DRYER_MEDIUM': 42 * 60
    }  

    def register(self, app: Flask, laundromats: Dict[str, Laundromat]) -> NoReturn:
        def scan(laundromat: str, washer_id: str) -> str:
            if request.method == 'POST':
                data: Dict = request.get_json()

                new_state: MachineState = MachineState[data['state']]
                if new_state == MachineState.RUNNING:
                    print('running now...')
                    laundromats[laundromat].set_washer(washer_id, MachineState.RUNNING)
                    Timer(self.CYCLES[data['cycle']], lambda: laundromats[laundromat].set_washer(washer_id, MachineState.FULL)).start()
                elif new_state == MachineState.EMPTY:
                    print('emptying now...')
                    laundromats[laundromat].set_washer(washer_id, MachineState.EMPTY)
                else:
                    print('what the frick')
                
                return 'ok'
            else:  # request.method == 'GET'
                return render_template('scan.html', **{
                    'washer_id': washer_id,
                    'for_washer': True,  # TODO: support dryers
                    'current_state': laundromats[laundromat].get_washer(washer_id),
                    'MachineState': MachineState  # lets us use enum equality checks
                })
        
        app.add_url_rule('/scan/<laundromat>/<washer_id>', 'scan', scan, methods=['GET', 'POST'])
