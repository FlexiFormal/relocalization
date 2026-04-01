import dataclasses
import traceback
from typing import Callable

from flexi.parsing.mast import MAst, G


_WRAPPING_NODES = {'bracketed_stmt'}  # TODO: add more wraps here


def dewrap(mast: MAst) -> tuple[Callable[[MAst], MAst], MAst]:
    """
    e.g. (bracketed_stmt x) -> (lambda ast: (bracketed_stmt ast), x)
    """
    if isinstance(mast, G):
        if mast.value.core in _WRAPPING_NODES:
            # might have to nest unwraps

            child = next(iter(mast))
            f, c = dewrap(child)
            return lambda ast: G(mast.value, [f(ast)]), c.clone()

    return lambda ast: ast, mast




@dataclasses.dataclass
class tagged:
    pattern: str
    tag: str

    def __post_init__(self):
        assert isinstance(self.pattern, str)
        assert isinstance(self.tag, str)


@dataclasses.dataclass
class PatternMatch:
    tag_to_mast: dict[str, MAst]


class _NoMatch(Exception):
    pass


def pattern_match(mast: MAst, pattern) -> PatternMatch | None:

    tag_to_mast: dict[str, MAst] = {}

    # track = mast.value == 'for_term_stmt'
    track = False

    def _rec(mast: MAst, pattern):
        # for now, we only match G nodes
        if not isinstance(mast, G):
            raise _NoMatch

        prnt = lambda s: (print(len(traceback.format_stack()), s) if track else None)
        # prnt = lambda s: None

        prnt(f'Trying {pattern}')
        prnt(f'At {mast.value}')

        try:
            if isinstance(pattern, str):
                if mast.value != pattern:
                    prnt(f'Raise 1   {mast.value} - {pattern!r}')
                    raise _NoMatch()
            elif isinstance(pattern, tagged):
                if mast.value != pattern.pattern:
                    prnt('Raise 2')
                    raise _NoMatch()
                # the following check is too naive (might have added something to `tag_to_mast` in unsuccessful
                # recursion
                # # if pattern.tag in tag_to_mast:
                # #     raise ValueError(f'The tag {pattern.tag!r} occurs multiple times in the pattern')
                tag_to_mast[pattern.tag] = mast
            elif isinstance(pattern, tuple):  # have children
                if not len(pattern) == 2:
                    raise ValueError(f'Unexpected pattern: {pattern}')
                _rec(mast, pattern[0])
                prnt('matched')
                if len(pattern[1]) != len(mast):
                    prnt(f':: {pattern}')
                    prnt(f':: {mast}')
                    if mast.value.core in _WRAPPING_NODES:
                        raise _NoMatch
                    raise ValueError(f'Number of children in pattern does not match mast node {mast.value}')
                for m, p in zip(mast, pattern[1]):
                    _rec(m, p)
            else:
                raise ValueError(f'Unexpected pattern: {type(pattern)}')
        except _NoMatch as e:
            prnt('OOPS')
            if mast.value.core in _WRAPPING_NODES:
                c = list(mast)
                assert len(c) == 1
                prnt('unwrap')
                _rec(c[0], pattern)
                prnt('unwrap succ')
            else:
                prnt('reraise')
                raise e


    try:
        if track:
            print('TRYING', mast)
        _rec(mast, pattern)
        if track: print('YES')
        return PatternMatch(tag_to_mast)
    except _NoMatch:
        if track: print('NO')
        return None



