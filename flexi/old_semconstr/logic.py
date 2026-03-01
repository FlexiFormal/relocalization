import abc
import dataclasses
from copy import deepcopy
from typing import Iterable


class SimpleType(abc.ABC):
    """
    An improvised simple type theory.
    It is only used for sanity checks in the semantics construction.
    It's limited enough that we can use equality for subtyping.
    """

    def __pow__(self, other) -> Arrow:
        """
        Constructor for arrow types.
        It's silly to use `**`, but that's the only right-associative binary operator in Python...
        """
        assert isinstance(other, SimpleType)
        return Arrow(self, other)

    def to(self, other) -> Arrow:
        return self ** other

    @abc.abstractmethod
    def __le__(self, other):
        """
        Subtyping relation.
        """



@dataclasses.dataclass
class Arrow(SimpleType):
    a: SimpleType
    b: SimpleType

    def __str__(self):
        return f'({self.a} ⟶ {self.b})'

    def __eq__(self, other) -> bool:
        return isinstance(other, Arrow) and self.a == other.a and self.b == other.b

    def __le__(self, other) -> bool:
        if not isinstance(other, Arrow):
            return isinstance(other, UnitType)
        return other.a <= self.a and self.b <= other.b


@dataclasses.dataclass
class AtomicType(SimpleType):
    label: str

    def __str__(self):
        return self.label

    def __eq__(self, other) -> bool:
        return isinstance(other, AtomicType) and self.label == other.label

    def __le__(self, other) -> bool:
        return self == other or isinstance(other, UnitType)


class UnitType(SimpleType):
    """ More of a placeholder (or unspecified type that shouldn't be checked) to be honest... """
    def __eq__(self, other):
        return isinstance(other, UnitType)

    def __str__(self):
        return '?'

    def __le__(self, other):
        return isinstance(other, UnitType)


class Typ:
    Any = UnitType()
    T = AtomicType('ο')
    E = AtomicType('ι')
    ET = E ** T
    ET_T = ET ** T


class QLF(abc.ABC):
    """ Quasi-Logical Formula """
    typ: SimpleType

    @abc.abstractmethod
    def children(self) -> Iterable[QLF]:
        ...

    @abc.abstractmethod
    def with_substitution(self, var: Var, val: QLF) -> QLF:
        """
        Returns a copy of this formula with all occurrences of `var` replaced by `val`.
        Currently just a placeholder implementation.
        More work is needed to handle shadowing correctly for DRSs.
        """


class Var(QLF):
    """ abstract """

    def children(self) -> Iterable[QLF]:
        yield from ()

    def with_substitution(self, var: Var, val: QLF) -> QLF:
        return deepcopy(self) if self != var else val


class NewVar(Var):
    counter = 0

    def __init__(self, typ: SimpleType):
        self.no = NewVar.counter
        NewVar.counter += 1
        self.typ = typ

    def __str__(self):
        return f'X{self.no}'


class NamedVar(Var):
    def __init__(self, name: str, typ: SimpleType, is_semantic: bool):
        self.name = name
        self.typ = typ
        self.is_semantic = is_semantic   # $n$ vs $\nvar$

    def __str__(self):
        return self.name


class Const(QLF):
    def __init__(self, name: str, typ: SimpleType):
        self.name = name
        self.typ = typ

    def __str__(self):
        return self.name

    def children(self) -> Iterable[QLF]:
        yield from ()

    def with_substitution(self, var: Var, val: QLF) -> QLF:
        return deepcopy(self)


class Lambda(QLF):
    def __init__(self, var: Var, body: QLF):
        self.var = var
        self.body = body
        self.typ = var.typ.to(body.typ)

    @classmethod
    def multi(cls, *args: Var, body: QLF) -> Lambda:
        for var in reversed(args):
            body = cls(var, body)
        return body

    def children(self) -> Iterable[QLF]:
        yield self.var
        yield self.body

    def __str__(self):
        return f'(λ{self.var}.{self.body})'

    def with_substitution(self, var: Var, val: QLF) -> QLF:
        if self.var == var:
            return deepcopy(self)
        else:
            return Lambda(self.var, self.body.with_substitution(var, val))

class Apply(QLF):
    def __init__(self, func: QLF, arg: QLF):
        self.func = func
        self.arg = arg
        if isinstance(func.typ, Arrow) and arg.typ <= func.typ.a:
            # if arg.typ is unit type, we use it more as a placeholder than anything else...
            self.typ = func.typ.b
        elif isinstance(func.typ, UnitType) or (isinstance(func.typ, Arrow) and isinstance(arg.typ, UnitType)):
            self.typ = UnitType()
        else:
            raise TypeError(f'Cannot apply {func} : {func.typ} to {arg} : {arg.typ}')

    def children(self) -> Iterable[QLF]:
        yield self.func
        yield self.arg

    @classmethod
    def multi(cls, func: QLF, *args: QLF) -> Apply:
        for arg in args:
            func = cls(func, arg)
        return func

    def __str__(self):
        return f'({self.func} {self.arg})'

    def force_single_beta_reduction(self) -> QLF:
        assert isinstance(self.func, Lambda), f'Cannot force beta reduction of non-lambda {self.func}'
        var = self.func.var
        val = self.arg
        value = deepcopy(self.func.body)
        return value.with_substitution(var, val)

    def with_substitution(self, var: Var, val: QLF) -> QLF:
        return Apply(self.func.with_substitution(var, val), self.arg.with_substitution(var, val))

class Seq(QLF):
    """ for stex argument sequences in formulae (corresponding to MSeq in MAst) """
    def __init__(self, *args: QLF):
        self.args = args
        self.typ = Typ.Any

    def __str__(self):
        return ', '.join(str(arg) for arg in self.args)

    def children(self) -> Iterable[QLF]:
        yield from self.args

    def with_substitution(self, var: Var, val: QLF) -> QLF:
        return Seq(*[arg.with_substitution(var, val) for arg in self.args])


class DRS(QLF):
    def __init__(self, referents: list[Var], conditions: list[QLF]):
        self.referents = referents
        self.conditions = conditions
        self.typ = Typ.T

    def __str__(self):
        refs = ', '.join(str(r) for r in self.referents)
        conds = ', '.join(str(c) for c in self.conditions)
        return f'[{refs} | {conds}]'

    def children(self) -> Iterable[QLF]:
        yield from self.referents
        yield from self.conditions

    def with_substitution(self, var: Var, val: QLF) -> QLF:
        if var in self.referents:
            return deepcopy(self)
        else:
            return DRS(self.referents, [c.with_substitution(var, val) for c in self.conditions])


class BinConnective(QLF):
    def __init__(self, left: QLF, right: QLF, symbol: str):
        self.left = left
        self.right = right
        if left.typ != Typ.T or right.typ != Typ.T:
            raise TypeError(f'Cannot form binary connective {symbol!r} of {left} : {left.typ} and {right} : {right.typ}')
        self.typ = Typ.T
        self.symbol = symbol

    def __str__(self):
        return f'({self.left} {self.symbol} {self.right})'

    def children(self) -> Iterable[QLF]:
        yield self.left
        yield self.right

    def with_substitution(self, var: Var, val: QLF) -> QLF:
        return type(self)(self.left.with_substitution(var, val), self.right.with_substitution(var, val), self.symbol)

class Iff(BinConnective):
    def __init__(self, left: QLF, right: QLF):
        super().__init__(left, right, '⇔')


class And(BinConnective):
    def __init__(self, left: QLF, right: QLF):
        super().__init__(left, right, '∧')

class TRUE(QLF):
    def __init__(self):
        self.typ = Typ.T

    def __str__(self):
        return '⊤'

    def children(self) -> Iterable[QLF]:
        yield from ()

    def with_substitution(self, var: Var, val: QLF) -> QLF:
        return deepcopy(self)



class HOL:
    """
    higher-order logic expression

    We use the simple type theory from above.
    All we need is lambdas, (function) constants, and applications.
    For simplicity, there is no distinction between constants and variables.
    """
    typ: SimpleType


class HolConst(HOL):
    def __init__(self, name: str, typ: SimpleType):
        self.name = name
        self.typ = typ

    def __str__(self):
        return self.name


class HolApply(HOL):
    def __init__(self, func: HOL, arg: HOL):
        self.func = func
        self.arg = arg
        if isinstance(func.typ, Arrow) and arg.typ <= func.typ.a:
            # if arg.typ is unit type, we use it more as a placeholder than anything else...
            self.typ = func.typ.b
        elif isinstance(func.typ, UnitType) or (isinstance(func.typ, Arrow) and isinstance(arg.typ, UnitType)):
            self.typ = UnitType()
        else:
            raise TypeError(f'Cannot apply {func} : {func.typ} to {arg} : {arg.typ}')

    def __str__(self):
        return f'({self.func} {self.arg})'


class HolLambda(HOL):
    def __init__(self, var: HolConst, body: HOL):
        self.var = var
        self.body = body
        self.typ = var.typ.to(body.typ)

    def __str__(self):
        return f'(λ{self.var}.{self.body})'
