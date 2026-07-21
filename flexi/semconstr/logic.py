import abc
import dataclasses
import functools
from typing import Literal

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

    @abc.abstractmethod
    def result_type(self) -> 'AtomicType':
        ...

    @abc.abstractmethod
    def get_argument_types(self) -> list['SimpleType']:
        ...



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

    def result_type(self) -> 'AtomicType':
        return self.b.result_type()

    def get_argument_types(self) -> list['SimpleType']:
        return [self.a] + self.b.get_argument_types()


@dataclasses.dataclass
class AtomicType(SimpleType):
    label: str

    def __str__(self):
        return self.label

    def __eq__(self, other) -> bool:
        return isinstance(other, AtomicType) and self.label == other.label

    def __le__(self, other) -> bool:
        return self == other or isinstance(other, UnitType)

    def result_type(self) -> 'AtomicType':
        return self

    def get_argument_types(self) -> list['SimpleType']:
        return []


class UnitType(AtomicType):
    """
    We probably don't need this, but I had it already from the old implementation...
    """
    def __eq__(self, other):
        return isinstance(other, UnitType)

    def __str__(self):
        return '⊤'

    def __le__(self, other):
        return isinstance(other, UnitType)


class Typ:
    T = AtomicType('ο')
    E = AtomicType('ι')
    ET = E ** T
    ET_T = ET ** T
    TTT = T ** (T ** T)
    TT = T ** T
    EET = E ** (E ** T)
    EE = E ** E
    EEE = E ** (E ** E)


##############
# Logic
# (a sort of higher-order logic implemented in a simply-typed lambda calculus)
##############

class Expr:
    """ abstract """
    def __init__(self, typ: SimpleType):
        self.typ = typ

    def beta_reduced(self) -> 'Expr':
        if isinstance(self, Apply):
            func = self.func.beta_reduced()
            arg = self.arg.beta_reduced()
            if isinstance(func, Lambda):
                return func.body.substituted(func.var, arg).beta_reduced()
            else:
                return Apply(func, arg)
        elif isinstance(self, Lambda):
            return Lambda(self.var, self.body.beta_reduced())
        else:  # constant or variable
            return self

    def substituted(self, var: 'Var', value: 'Expr') -> 'Expr':
        if self == var:
            return value
        elif isinstance(self, Apply):
            return Apply(self.func.substituted(var, value), self.arg.substituted(var, value))
        elif isinstance(self, Lambda):
            if self.var == var:
                return self  # variable is bound -> do not recurse
            else:
                return Lambda(self.var, self.body.substituted(var, value))
        else:  # constant or other variable
            return self

    def simplified(self) -> 'Expr':
        expr = self.beta_reduced()
        changed_something: bool = True

        def _helper(e: Expr) -> Expr:
            nonlocal changed_something
            if isinstance(e, Apply):
                match e:
                    case Apply(Apply(Const.Conjunction, a), Const.Truth) | Apply(Apply(Const.Conjunction, Const.Truth), a):
                        changed_something = True
                        return a
                return Apply(_helper(e.func), _helper(e.arg))
            elif isinstance(e, Lambda):
                return Lambda(e.var, _helper(e.body))
            else:
                return e

        while changed_something:
            changed_something = False
            expr = _helper(expr)

        return expr


class Apply(Expr):
    __match_args__ = ('func', 'arg')

    def __init__(self, func: Expr, arg: Expr):
        assert isinstance(func.typ, Arrow) and arg.typ <= func.typ.a, (
            'Type mismatch:\n'
            f'{func.typ} @ {arg.typ}\n'
            f'({func})    @    ({arg})'
        )
        super().__init__(func.typ.b)
        self.func = func
        self.arg = arg

    @classmethod
    def multi(cls, func: Expr, *args: Expr) -> 'Apply':
        result = func
        for arg in args:
            result = cls(result, arg)
        return result

    def __str__(self):
        match self:
            case Apply(Apply(c, a), b) if c in [
                Const.Implication, Const.Equivalence, Const.Conjunction, Const.Disjunction, Const.Equal, Const.Cons,
            ]:
                assert isinstance(c, Const)
                return f'({a} {c.name} {b})'
        return f'({self.func} {self.arg})'


class Var(Expr):
    __match_args__ = ('name',)
    _freshvar_counter = 1

    def __init__(self, name: str, typ: SimpleType, is_semantic: bool):
        super().__init__(typ)
        self.name = name
        self.is_semantic = is_semantic

    @classmethod
    def fresh(cls, typ: SimpleType) -> 'Var':
        name = f'?{cls._freshvar_counter}'
        cls._freshvar_counter += 1
        # should we mark fresh variables too?
        return cls(name, typ, is_semantic=False)

    def __str__(self):
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, Var) and self.name == other.name:
            assert self.typ == other.typ
            return True
        return False


class Const(Expr):
    __match_args__ = ('name',)

    Forall: 'Const'
    Exists: 'Const'
    Negation: 'Const'
    Implication: 'Const'
    Equivalence: 'Const'
    Conjunction: 'Const'
    Disjunction: 'Const'
    Truth: 'Const'
    Equal: 'Const'
    Nil: 'Const'
    Cons: 'Const'

    def __init__(self, name: str, typ: SimpleType):
        super().__init__(typ)
        self.name = name

    def __str__(self):
        if self.name.startswith('http://') or self.name.startswith('https://') and '&s=' in self.name:
            return f'<...&s={self.name.split("&s=")[-1]}>'
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, Const) and self.name == other.name:
            assert self.typ == other.typ
            return True
        return False


Const.Forall = Const('∀', Typ.ET_T)
Const.Exists = Const('∃', Typ.ET_T)
Const.Negation = Const('¬', Typ.TT)
Const.Implication = Const('⇒', Typ.TTT)
Const.Equivalence = Const('⇔', Typ.TTT)
Const.Conjunction = Const('∧', Typ.TTT)
Const.Disjunction = Const('∨', Typ.TTT)
Const.Truth = Const('T', Typ.T)
Const.Equal = Const('=', Typ.EET)
# list constructors
Const.Nil = Const('nil', Typ.E)
Const.Cons = Const('::', Typ.EEE)



class Lambda(Expr):
    __match_args__ = ('var', 'body',)
    def __init__(self, var: 'Var', body: Expr):
        super().__init__(var.typ.to(body.typ))
        self.var = var
        self.body = body

    def __str__(self):
        return f'(λ{self.var}.{self.body})'


@dataclasses.dataclass
class TptpConvCtx:
    format: Literal['fof'] = 'fof'


def to_tptp_name(
        expr: Var | Const
) -> str:
    if isinstance(expr, Const) and expr.name.startswith('http://') or expr.name.startswith('https://'):
        return expr.name.rstrip('+').split('=')[-1].replace(' ', '_')
    else:
        return expr.name


def expr_to_tptp(
        expr: Expr,
        ctx: TptpConvCtx,
) -> str:
    c = functools.partial(expr_to_tptp, ctx=ctx)

    if isinstance(expr, Apply):
        # uncurry
        args = [expr.arg]
        remainder = expr.func
        while isinstance(remainder, Apply):
            args.append(remainder.arg)
            remainder = remainder.func
        args = list(reversed(args))
        head = remainder
        if isinstance(head, Const):
            if head in [Const.Forall, Const.Exists]:
                assert len(args) == 1
                symb = '!' if head == Const.Forall else '?'
                return f'( {symb} {c(args[0])} )'
            if head in [
                Const.Conjunction, Const.Disjunction, Const.Implication, Const.Equivalence, Const.Equal
            ]:
                assert len(args) == 2
                if head == Const.Implication:
                    op = '=>'
                elif head == Const.Equivalence:
                    op = '<=>'
                elif head == Const.Conjunction:
                    op = '&'
                elif head == Const.Disjunction:
                    op = '|'
                elif head == Const.Equal:
                    op = '='
                else:
                    raise RuntimeError()
                return f'({c(args[0])} {op} {c(args[1])})'
            elif head == Const.Negation:
                assert len(args) == 1
                return f'( ~ {c(args[0])})'
            else:
                sname = to_tptp_name(head)
        elif isinstance(head, Var):
            sname = to_tptp_name(head)
        elif isinstance(head, Lambda):
            raise NotImplementedError('did you forget to simplify?')
        else:
            raise RuntimeError()
        return f'{sname}(' + ', '.join(c(arg) for arg in args) + ')'
    elif isinstance(expr, Const) or isinstance(expr, Var):
        return to_tptp_name(expr)
    elif isinstance(expr, Lambda):
        return f'[{expr.var}] : {c(expr.body)}'
    else:
        raise RuntimeError()




if __name__ == '__main__':
    # some quick tests for the logic implementation
    x = Var('x', Typ.T, is_semantic=True)
    y = Var('y', Typ.T, is_semantic=True)
    print(Apply.multi(Const.Implication, x, y))
