import functools
from typing import Callable


def get_only_element[T](l: list[T]) -> T:
    if len(l) != 1:
        raise RuntimeError(f'Expected exactly one element but got {len(l)}')
    return l[0]


def concat[**P, R1, R2](f1: Callable[[R1], R2]):
    def decorator(f2: Callable[P, R1]) -> Callable[P, R2]:
        @functools.wraps(f2)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R2:
            return f1(f2(*args, **kwargs))
        return wrapper
    return decorator
