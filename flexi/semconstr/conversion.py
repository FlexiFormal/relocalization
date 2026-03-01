import dataclasses
import functools
import re

from flexi.parsing.mast import MAst, G, TermDef, Formula, M, MSeq, MI, MT
from flexi.semconstr.logic import Const, Var, Typ, Expr, Apply, Lambda, SimpleType


class LQ:
    """ "Linguistic quantifier" """
    def __init__(
            self,
            quantifier: Const,
            connective: Const,
    ):
        self.quantifier = quantifier
        self.connective = connective
        assert quantifier.typ == Typ.ET_T
        assert connective.typ == Typ.TTT

LQ.forall = LQ(Const.Forall, Const.Implication)
LQ.exists = LQ(Const.Exists, Const.Conjunction)


class Declaration:
    def __init__(self, quantifier: LQ, var: Var, restriction: Expr):
        self.quantifier = quantifier
        self.var = var
        self.restriction = restriction
        assert self.restriction.typ == Typ.T  # we capture the variable


def existential_to_universal(decls: list[Declaration]) -> list[Declaration]:
    result = []
    for decl in decls:
        if decl.quantifier == LQ.exists:
            result.append(Declaration(LQ.forall, decl.var, decl.restriction))
        else:
            result.append(decl)
    return result


def decl_merge(decls: list[Declaration], stmt: Expr) -> Expr:
    result = stmt
    for decl in reversed(decls):
        result = Apply(
            decl.quantifier.quantifier,
            Lambda(
                decl.var,
                Apply.multi(decl.quantifier.connective, decl.restriction, result)
            )
        )
    return result


@dataclasses.dataclass
class Context:
    ...


def strip_variant_suffix(fun: str) -> str:
    if not isinstance(fun, str):
        raise ValueError(f'Expected fun to be a string, got {fun} of type {type(fun)}')
    if match := re.match(r'(.*)_v[0-9]+$', fun):
        return match.group(1)
    return fun


class OtherMeaning:
    """ Meanings that are not `Expr` """

@dataclasses.dataclass
class NamedKindMeaning(OtherMeaning):
    """
        For quantification, we need to be able to access the name.
        It is therefore represented as a pair of the identifiers and the kind.
        For example, "even integers x, y" would be ([x, y], λe.even(e)∧integer(e)).
    """
    identifiers: list[Var]
    kind: Expr


@dataclasses.dataclass
class IdentifiersMeaning(OtherMeaning):
    identifiers: list[Var]
    constraint: Expr


@dataclasses.dataclass
class FormulaMeaning(OtherMeaning):
    referenceables: list[Expr]
    formula: Expr

    def to_identifiers_meaning(self) -> IdentifiersMeaning:
        identifiers: list[Var] = []
        for r in self.referenceables:
            if isinstance(r, Var):
                identifiers.append(r)
            else:
                raise ValueError(f'Expected all referenceables to be Vars, got {r}')
        return IdentifiersMeaning(
            identifiers=identifiers,
            constraint=self.formula
        )


def convert(m: MAst, ctx: Context) -> tuple[list[Declaration], Expr | OtherMeaning]:
    """
    Notes on types:
        NamedKind: a pair of identifiers and kind (see `NamedKindMeaning`).
        Term: (ι ⟶ o) ⟶ o (standard type raising for noun phrases)
    """
    conv = functools.partial(convert, ctx=ctx)

    if isinstance(m, G):
        fun = strip_variant_suffix(m.value)
        if fun.startswith('lex_'):
            return [], _convert_lex_helper(fun)

        match (fun, list(m)):
            case ('stmt_sentence', [stmt]):
                return conv(stmt)
            case ('formula_stmt', [formula]):
                d, f = conv(formula)
                assert isinstance(f, FormulaMeaning)
                return d, f.formula
            case ('subj_stmt' | 'conj_stmt', [subj, a, b]):
                s = strip_variant_suffix(subj.value)
                a_decls, aa = conv(a)
                b_decls, bb = conv(b)
                if s == 'iff_subj':
                    return [], decl_merge(
                        existential_to_universal(a_decls),
                        Apply.multi(Const.Equivalence, aa, decl_merge(b_decls, bb))
                    )
                raise NotImplementedError(f'Conversion for subj_stmt/conj_stmt with subj {s} not implemented yet')
            case ('term_is_property_stmt', [term, property]):
                term_decls, t = conv(term)
                property_decls, p = conv(property)
                return term_decls + property_decls, Apply(t, p)
            case ('quantified_nkind', [quant, nkind]):
                quant_map = {
                    'indefinite_quantification': LQ.exists,
                    'universal_quantification': LQ.forall,
                }
                quant_name = strip_variant_suffix(quant.value)
                if quant_name not in quant_map:
                    raise NotImplementedError(f'Conversion for quantifier {quant_name} not implemented yet')
                extra_decls, nk = conv(nkind)
                assert isinstance(nk, NamedKindMeaning)
                p = Var.fresh(Typ.ET)
                body: Expr = Const.Truth
                for e in nk.identifiers:
                    body = Apply.multi(Const.Conjunction, Apply(p, e), body)
                return (
                    [Declaration(quant_map[quant_name], v, Apply(nk.kind, v)) for v in nk.identifiers] + extra_decls,
                    Lambda(p, body)
                )
            case ('name_kind', [kind, maybe_identifiers]):
                decls, k = conv(kind)
                decls2, ids = conv(maybe_identifiers)
                assert not decls2, f'Expected no declarations for maybe_identifiers, got {len(decls2)}'
                return decls, NamedKindMeaning(identifiers=ids.identifiers, kind=k)
            case ('prekind_to_kind', [prekind]):
                return conv(prekind)
            case ('cast_Identifiers_MaybeIdentifiers', [identifiers]):
                return conv(identifiers)
            case ('single_identifier', [identifier]):
                return conv(identifier)
            case ('formula_ident', [math]):
                decls, f = conv(math)
                assert isinstance(f, FormulaMeaning)
                return decls, f.to_identifiers_meaning()
    elif isinstance(m, TermDef):
        if m.wrapfun == 'wrapped_property':
            typ = Typ.ET
        elif m.wrapfun == 'wrapped_sentence':
            typ = Typ.T
        else:
            raise NotImplementedError(f'Unknown wrapfun {m.wrapfun} in TermDef')
        return [], Const(m.value, typ)
    elif isinstance(m, Formula):
        assert len(m) == 1
        return [], FormulaMeaning(
            referenceables=_extract_refables(m[0], ctx),
            formula=_convert_math_helper(m[0], ctx)
        )
    elif isinstance(m, TermDef):
        if m.wrapfun == 'wrapped_property':
            typ = Typ.ET
        elif m.wrapfun == 'wrapped_sentence':
            typ = Typ.T
        else:
            raise NotImplementedError(f'Unknown wrapfun {m.wrapfun} in TermDef')
        return [], Const(m.value, typ)

    raise NotImplementedError(f'Conversion for MAst {m} not implemented yet')



def _extract_refables(m: MAst, ctx: Context) -> list[Expr]:
    """
    Returns referenceable terms from a formula.

    Examples:
        * $x$ -> [x]
        * $x, y \in S$ -> [x, y]
        * $f(x) > 0$ -> [f(x)]
    """

    extract = functools.partial(_extract_refables, ctx=ctx)

    if isinstance(m, M):
        if m.value.startswith('http://') or m.value.startswith('https://'):
            if get_smglom_type(m.value) == Typ.T:
                return extract(m[0])
            else:   # a term?
                return [_convert_math_helper(m, ctx)]
        else:  # I guess it must be a variable (or possibly a constant...)
            return [Var(m.value, Typ.E, is_semantic=True)]
    elif isinstance(m, MSeq):
        return [_convert_math_helper(c, ctx) for c in m]
    else:
        raise NotImplementedError(f'Cannot extract refables from {m}')


def _convert_math_helper(m, ctx: Context) -> Expr:
    """ plain conversion of a formula """
    conv = functools.partial(_convert_math_helper, ctx=ctx)

    if isinstance(m, M):
        if m.value.startswith('http://') or m.value.startswith('https://'):
            t = get_smglom_type(m.value)
        else:
            t = Typ.E   # TODO: be smarter here
        return Apply.multi(Const(m.value, t), *[conv(c) for c in m])
    elif isinstance(m, MSeq):
        args = [conv(c) for c in m]
        # TODO: could have other types than E
        l = Const('nil', Typ.E)
        for arg in reversed(args):
            l = Apply(Apply(Const('cons', Typ.EEE), arg), l)
        return l
    elif isinstance(m, MI):
        assert len(m) == 1
        assert isinstance(m[0], MT)
        # TODO: what about constants?...
        return Var(m[0].value, Typ.E, is_semantic=False)
    else:
        raise NotImplementedError(f'Cannot convert math node {m} to QLF')

def _convert_lex_helper(lex: str) -> Expr:
    """
    Hard-coded conversion for a few lexical entries.
    This is only intended as an initial solution to get off the ground.
    """
    match lex:
        case 'lex_integer':
            return Const('integer', Typ.ET)

    raise NotImplementedError(f'Conversion for lexical item {lex} not implemented yet')



SMGLOM_TYPES: dict[str, SimpleType] = {
    'https://stexmmt.mathhub.info/:sTeX?a=smglom/arithmetics&p=mod&m=intarith&s=greater than': Typ.EET
}

def get_smglom_type(uri: str) -> SimpleType:
    t = SMGLOM_TYPES.get(uri)
    if t is None:
        raise NotImplementedError(f'Unknown type for {uri}')
    return t
