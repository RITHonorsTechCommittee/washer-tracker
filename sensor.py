from abc import ABC, abstractmethod
from flask import Flask
from typing import Dict, NoReturn

from laundromat import Laundromat


class Sensor(ABC):
    """
    This abstract class specifies how the server should interact with a
    specific sensor.
    """

    @abstractmethod
    def register(self, app: Flask, laundromats: Dict[str, Laundromat]) -> NoReturn:
        """
        Optional method called at program start. You can use this to
        register Flask routes, if needed.
        """
        pass
