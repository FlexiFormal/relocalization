from typing import Iterable

from flexi.parsing.mast import MAst


def filter_readings(readings: Iterable[MAst]) -> Iterable[MAst]:
    yield from readings