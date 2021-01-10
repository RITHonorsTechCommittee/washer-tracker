from abc import ABC, abstractmethod
from enum import Enum
from flask import Flask
from typing import NoReturn


class WasherState(Enum):
    RUNNING = 1
    FULL = 2
    EMPTY = 3


class Sensor(ABC):
    """
    This abstract class specifies how the server should interact with a
    specific sensor.
    """

    def register(self, app: Flask) -> NoReturn:
        """
        Optional method called at program start. You can use this to
        register Flask routes, if needed.
        """
        pass

    @abstractmethod
    def get_washer(self, id: int) -> WasherState:
        """
        Get the current state of the washer with given ID.

        Parameters:
        - id (int): The ID of the washer to check

        Returns: The state of the washer
        """
        raise NotImplementedError
