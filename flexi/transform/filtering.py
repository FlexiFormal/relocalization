"""
Type A: Parsing should have yielded two equivalent ASTs.
We remove one of them (but do not check that the other one actually exists).

Type B: Remove nonsensical ASTs.
"""

import dataclasses
from typing import Iterable

from flexi.parsing.mast import MAst, G


@dataclasses.dataclass
class FilteringCtx:
    pass


def filter_readings(readings: Iterable[MAst], ctx: FilteringCtx) -> Iterable[MAst]:
    for reading in readings:
        do_filter: bool = False
        for filter in [filter_conj_ambig]:
            if filter(reading, ctx):
                do_filter = True
                break
        if not do_filter:
            yield reading


def filter_conj_ambig(reading: MAst, ctx: FilteringCtx) -> bool:
    """ Type A.
    remove "(X and Y) and Z" in favor of "X and (Y and Z)"
    """
    for node in reading.find_children(lambda x: isinstance(x, G)):
        match node:
            case G(
                '~conj_stmt#', [
                    G('~and_conj#'),
                    G('~conj_stmt#', [G('~and_conj#'), _, _]),
                    _
                ]
            ):
                return True
    return False




