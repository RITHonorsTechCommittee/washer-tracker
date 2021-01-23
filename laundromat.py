from __future__ import annotations
from enum import Enum
from string import ascii_uppercase
from typing import Dict, NoReturn, Union


class MachineState(Enum):
    RUNNING = 1
    FULL = 2
    EMPTY = 3


Machines = Dict[str, MachineState]


class Laundromat:
    def __init__(self, name: str, washers: Machines, dryers: Machines) -> NoReturn:
        self.name: str = name
        self.washers: Machines = washers  # {machine number/letter: running/full/empty}
        self.dryers: Machines = dryers
    
    @classmethod
    def create(cls, name: str, num_washers: int, num_dryers: int) -> Laundromat:
        washers: Machines = {str(i): MachineState.EMPTY for i in range(1, num_washers + 1)}

        # dryers are 50% numbers, 50% letters for the IDs
        dryers: Machines = {str(i): MachineState.EMPTY for i in range(1, (num_washers // 2) + 1)}
        for i in ascii_uppercase[:(num_dryers // 2) + 1]:
            dryers[i] = MachineState.EMPTY

        return cls(name, washers, dryers)

    def get_washer(self, washer_id) -> Union[MachineState, None]:
        return self.washers.get(washer_id, None)

    def set_washer(self, washer_id: str, state: MachineState) -> NoReturn:
        self.washers[washer_id] = state

    def get_dryer(self, dryer_id) -> Union[MachineState, None]:
        return self.dryers.get(dryer_id, None)

    def set_dryer(self, dryer_id: str, state: MachineState) -> NoReturn:
        self.dryers[dryer_id] = state
