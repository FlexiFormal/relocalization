from collections import defaultdict
from copy import deepcopy

from flexi.parsing.mast import MAst


class Placeholder(MAst):
    _id_counter = 0
    value: str

    def __init__(self, value: str | None):
        super().__init__(value=value or f'?{Placeholder._id_counter}')
        if value is None:
            Placeholder._id_counter += 1


class PlaceholderExpression:
    def __init__(self, expression: MAst, placeholders: list[Placeholder | list[Placeholder]]):
        # placeholders[i] is a list if a placeholder occurs in multiple places
        # (copies should be made via Placeholder.clone)
        self.expression = expression
        if self.expression.get_path():
            raise ValueError('Placeholder expression should be root')
        self.placeholders: list[list[Placeholder]] = [([ph] if isinstance(ph, Placeholder) else ph) for ph in placeholders]
        self.placeholders_by_value = defaultdict(list)
        for placeholderset in self.placeholders:
            for placeholder in placeholderset:
                self.placeholders_by_value[placeholder.value].append(placeholder)

    def instantiate(self, args: list[MAst] | dict[str, MAst]) -> MAst:
        # TODO: Return new PlaceholderExpression for partial instantiation

        copy = self.expression.clone()

        if isinstance(args, list):
            if len(args) != len(self.placeholders):
                raise ValueError('Length of expression must be equal to length of placeholders')

            for arg, placeholders in zip(args, self.placeholders):
                for ph in placeholders:
                    path = ph.get_path()
                    if not path:  # expression is just the placeholder:
                        return arg.clone()
                    copy.follow_path(path).replace_in_parent(arg)
        else:
            for value, arg in args.items():
                if value not in self.placeholders_by_value:
                    raise ValueError(f'No placeholder with value {value!r} in expression')
                for ph in self.placeholders_by_value[value]:
                    path = ph.get_path()
                    if not path:  # expression is just the placeholder:
                        return arg.clone()
                    copy.follow_path(path).replace_in_parent(arg)

        return copy





