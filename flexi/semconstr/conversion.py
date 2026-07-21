import dataclasses
import functools
import re
from typing import TypeAlias, Literal, Iterable

from torch._dynamo.polyfills import itertools

from flexi.parsing.mast import MAst, G, TermDef, Formula, M, MSeq, MI, MT, GfSymb, X
from flexi.semconstr.logic import Const, Var, Typ, Expr, Apply, Lambda, SimpleType
from flexi.utils import get_only_element, concat


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

    def __repr__(self):
        return f'{self.quantifier.quantifier} {self.var} {self.restriction}'


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
class ConversionContext:
    ...


class OtherMeaning:
    """ Meanings that are not `Expr` """

@dataclasses.dataclass
class NamedKindMeaning(OtherMeaning):
    """
        For quantification, we need to be able to access the name.

        Simple idea:
            It is therefore represented as a pair of the identifiers and the kind.
            For example, "even integers x, y" would be ([x, y], λe.even(e)∧integer(e)).

        Actual implementation:
            We also need to store the constraint.
            E.g. "even integers x, y ∈ S" becomes ([x, y], x∈S∧y∈S, λe.even(e)∧integer(e)).
            While it could be part of the kind, that would result in duplication and
            more awkward transforms to avoid ensure that all variables are introduced before the constraint.
    """
    identifiers: list[Var]
    constraint: Expr
    kind: Expr

    def __post_init__(self):
        assert isinstance(self.identifiers, list), self.identifiers


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
        constraint = Const.Truth
        if self.formula.typ == Typ.T:
            constraint = self.formula
        elif self.formula.typ != Typ.E:
            raise ValueError(f'Expected type T or E, got {self.formula.typ} for {self.formula}')
        return IdentifiersMeaning(
            identifiers=identifiers,
            constraint=constraint
        )


def finalized_convert(m: MAst, ctx: ConversionContext) -> Expr:
    """ like convert, but merges all open declarations """
    d, e = convert(m, ctx)
    assert isinstance(e, Expr)
    return decl_merge(d, e)


ConvMeaning: TypeAlias = tuple[list[Declaration], Expr | OtherMeaning]


def convert(m: MAst, ctx: ConversionContext) -> ConvMeaning:
    """
    Notes on types:
        NamedKind: a pair of identifiers and kind (see `NamedKindMeaning`).
        Term: (ι ⟶ o) ⟶ o (standard type raising for noun phrases)

    Other notes:
        Definitions: Translated into propositions, which could be considered "defining axioms" I guess...
    """
    conv = functools.partial(convert, ctx=ctx)

    if isinstance(m, G):
        fun = m.value.core
        if fun.startswith('lex_'):
            return [], _convert_lex_helper(fun)

        match (fun, list(m)):
            case ('stmt_sentence' | 'def_sentence' | 'plain_defcore', [a]):
                return conv(a)
            case ('formula_stmt', [formula]):
                d, f = conv(formula)
                assert isinstance(f, FormulaMeaning)
                return d, f.formula
            case ('subj_stmt' | 'conj_stmt', [subj, a, b]):
                return _convert_connective_application(subj.value, conv(a), conv(b))
            case ('term_is_property_stmt', [term, property]):
                term_decls, t = conv(term)
                property_decls, p = conv(property)
                return term_decls + property_decls, Apply(t, p)
            case ('quantified_nkind', [quant, nkind]):
                return _convert_quantify_nkind(quant.value, conv(nkind))
            case ('name_kind', [kind, maybe_identifiers]):
                decls, k = conv(kind)
                decls2, ids = conv(maybe_identifiers)
                assert isinstance(ids, IdentifiersMeaning)
                assert isinstance(k, Expr)
                # identifiers are ([], FormulaMeaning).
                # itentifiers cannot be declarations yet as they have no quantifier
                assert not decls2, f'Expected no declarations for maybe_identifiers, got {len(decls2)}'
                # if ids.constraint != Const.Truth:
                #     v = Var.fresh(Typ.E)
                #     k = Lambda(v, Apply.multi(Const.Conjunction, ids.constraint, Apply(k, v)))
                return decls, NamedKindMeaning(identifiers=ids.identifiers, constraint=ids.constraint, kind=k)
            case ('identifiers_as_nkind', [identifiers]):
                decls, ids = conv(identifiers)
                assert isinstance(ids, IdentifiersMeaning)
                assert not decls, f'Expected no declarations for maybe_identifiers, got {len(decls)}'
                return [], NamedKindMeaning(identifiers=ids.identifiers, constraint=ids.constraint, kind=Lambda(Var.fresh(Typ.E), Const.Truth))
            case ('prekind_to_kind', [prekind]):
                return conv(prekind)
            case ('cast_Identifiers_MaybeIdentifiers', [identifiers]):
                return conv(identifiers)
            case ('single_identifier', [identifier]):
                return conv(identifier)
            case ('formula_ident' | 'formula_idents', [math]):
                decls, f = conv(math)
                assert isinstance(f, FormulaMeaning)
                return decls, f.to_identifiers_meaning()
            case ('defcore_if_stmt', [core, stmt]):
                return _convert_connective_application('iff_subj', conv(core), conv(stmt))
            case ('define_nkind_prop', [nkind, property]):
                qnk_decls, qnk = _convert_quantify_nkind('indefinite_quantification', conv(nkind))
                property_decls, p = conv(property)
                return qnk_decls + property_decls, Apply(qnk, p)
            case ('define_ident_prop', [ident, property]):
                decls, ids = conv(ident)
                assert isinstance(ids, IdentifiersMeaning)
                assert not decls, f'Expected no declarations for maybe_identifiers, got {len(decls)}'
                property_decls, p = conv(property)
                nk = NamedKindMeaning(identifiers=ids.identifiers, constraint=ids.constraint, kind=Lambda(Var.fresh(Typ.E), Const.Truth))
                qnk_decls, qnk = _convert_quantify_nkind('indefinite_quantification', ([], nk))
                return qnk_decls + property_decls, Apply(qnk, p)
            case ('stmt_for_term', [stmt, term]):
                stmt_decls, s = conv(stmt)
                term_decls, t = conv(term)
                # TODO: are there cases where `t` has useful information?
                # Typical case:
                #   bar(x, y) for every foo x, y
                #   which gives something like
                #      term_decls = [(∀,x,foo(x)), (∀,y,foo(y))]
                #      t = λp.p(x) ∧ p(y)          (needed e.g. in "every foo x, y is bar")
                return [], decl_merge(stmt_decls + term_decls, s)
                # return [], decl_merge(stmt_decls + term_decls, Apply(t, Lambda(Var.fresh(Typ.E), s)))
            case ('exists_nkind', [nk]):
                qnk_decls, qnk = _convert_quantify_nkind('indefinite_quantification', conv(nk))
                return qnk_decls, Apply(qnk, Lambda(Var.fresh(Typ.E), Const.Truth))
                # merge is probably not right (x can be referenced after "there exists an x such that ...")
                # return [], decl_merge(qnk_decls, Apply(qnk, Lambda(Var.fresh(Typ.E), Const.Truth)))
            case ('such_that_named_kind', [nk, stmt]):
                nk_decls, nk = conv(nk)
                stmt_decls, stmt = conv(stmt)
                assert isinstance(nk, NamedKindMeaning)
                v = Var.fresh(Typ.E)
                # nk.kind = Lambda(v, Apply.multi(Const.Conjunction, Apply(nk.kind, v), stmt))
                nk.constraint = Apply.multi(Const.Conjunction, nk.constraint, stmt)
                return nk_decls + stmt_decls, nk

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
    elif isinstance(m, X):   # decorative tag (or unsupported annotation)
        if len(m) != 1:
            raise NotImplementedError(f'Expected exactly one term, got {len(m)}')
        return convert(m[0], ctx)

    raise NotImplementedError(f'Conversion for MAst {m} not implemented yet')


def _convert_connective_application(connective_fun: str, a: ConvMeaning, b: ConvMeaning) -> ConvMeaning:
    s = GfSymb(connective_fun).core
    a_decls, aa = a
    b_decls, bb = b
    if s == 'iff_subj':
        return [], decl_merge(
            existential_to_universal(a_decls),
            Apply.multi(Const.Equivalence, aa, decl_merge(b_decls, bb))
        )
    elif s == 'and_conj':
        return a_decls + b_decls, Apply.multi(Const.Conjunction, aa, bb)
    raise NotImplementedError(f'Conversion for {s} application not implemented yet')


def _convert_quantify_nkind(quant_fun: str, nkind: ConvMeaning) -> ConvMeaning:
    quant_map = {
        'indefinite_quantification': LQ.exists,
        'universal_quantification': LQ.forall,
    }
    quant_name = GfSymb(quant_fun).core
    if quant_name not in quant_map:
        raise NotImplementedError(f'Conversion for quantifier {quant_name} not implemented yet')
    extra_decls, nk = nkind
    assert isinstance(nk, NamedKindMeaning)
    p = Var.fresh(Typ.ET)
    body: Expr = Const.Truth
    for e in nk.identifiers:
        body = Apply.multi(Const.Conjunction, Apply(p, e), body)
    decls = [Declaration(quant_map[quant_name], v, Apply(nk.kind, v)) for v in nk.identifiers]
    # put constraint last to ensure that all identifiers it contains are in scope
    decls[-1].restriction = Apply.multi(Const.Conjunction, decls[-1].restriction, nk.constraint)
    r = (
        decls + extra_decls,
        Lambda(p, body)
    )
    return r


def _extract_refables(m: MAst, ctx: ConversionContext) -> list[Expr]:
    r"""
    Returns referenceable terms from a formula.

    Examples:
        * $x$ -> [x]
        * $x, y \in S$ -> [x, y]
        * $f(x) > 0$ -> [f(x)]
    """

    extract = functools.partial(_extract_refables, ctx=ctx)

    if isinstance(m, M):
        if m.value.startswith('http://') or m.value.startswith('https://'):
            if get_smglom_type(m.value).result_type() == Typ.T:
                return extract(m[0])
            else:   # a term?
                return [_convert_math_helper(m, ctx)]
        else:  # I guess it must be a variable (or possibly a constant...)
            return [Var(m.value, Typ.E, is_semantic=True)]
    elif isinstance(m, MSeq):
        return [e for c in m for e in extract(c) ]
    else:
        raise NotImplementedError(f'Cannot extract refables from {m}')


def funlist_to_pylist(c: Expr) -> Iterable[Expr]:
    match c:
        case Apply(Apply(cons, head), tail) if cons == Const.Cons:
            yield head
            yield from funlist_to_pylist(tail)
        case nil if nil == Const.Nil:
            return
        case _:
            raise ValueError(f'Cannot convert {c} to pylist')


def flex_reduce(c: Const, args: list[Expr]) -> Expr:
    default = Apply.multi(c, *args)   # no reduction
    ci = SMGLOM_CONSTS.get(c.name)
    if ci is None:
        return default
    shlist = ci.seqhandling
    if sum(sh is not None for sh in shlist) != 1:   # TODO: cover case > 1 (cannot be annotated in stex though)
        return default

    if c.name == 'http://mathhub.info?a=smglom/mv&p=mod&m=equal&s=equal':
        c = Const.Equal  # substitute with builtin equality
    else:
        c = Const(c.name + '+', ci.reduced_typ)

    # exactly 1 arg with special treatment
    pos, sh = get_only_element([(i, sh) for i, sh in enumerate(shlist) if sh is not None])
    listarg = list(funlist_to_pylist(args[pos]))
    if sh == 'conjunctwithrest':
        assert ci.typ.result_type() == Typ.T
        result = Const.Truth
        for arg in reversed(listarg):
            expr = Apply.multi(c, *[
                (a if i != pos else arg)
                for i, a in enumerate(args)
            ])
            result = Apply.multi(Const.Conjunction, expr, result)
        return result
    elif sh == 'pairwiseconjunct' and len(shlist) == 1:
        result = Const.Truth
        for a, b in itertools.pairwise(listarg):
            result = Apply.multi(Const.Conjunction, Apply.multi(c, a, b), result)
        return result
    elif sh == 'lassoc' and len(shlist) == 1 and listarg:  # need at least one argument (we do not know the neutral element)
        result = listarg[0]
        for arg in listarg[1:]:
            result = Apply.multi(c, result, arg)
        return result

    return default


def _convert_math_helper(m, ctx: ConversionContext) -> Expr:
    """ plain conversion of a formula """
    conv = functools.partial(_convert_math_helper, ctx=ctx)

    if isinstance(m, M):
        if m.value.startswith('http://') or m.value.startswith('https://'):
            t = get_smglom_type(m.value)
        else:
            t = Typ.E   # TODO: be smarter here
        return flex_reduce(Const(m.value, t), [conv(c) for c in m])
    elif isinstance(m, MSeq):
        args = [conv(c) for c in m]
        # TODO: could have other types than E
        l = Const.Nil
        for arg in reversed(args):
            l = Apply(Apply(Const.Cons, arg), l)
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


@dataclasses.dataclass
class ConstInfo:
    typ: SimpleType
    seqhandling: list[Literal[
                            'conjunctwithrest',     # a, b, c < d  -->  a < d ∧ b < d ∧ c < d
                            'pairwiseconjunct',     # a < b < c < d  -->  a < b ∧ b < c ∧ c < d   (arguably a misnomer, name from itertools.pairwise)
                            'lassoc',               # a * b * c * d  -->   ((a*b)*c)*d
                      ] | None] = None
    reduced_typ: SimpleType = None

    def __post_init__(self):
        if self.seqhandling is None:
            self.seqhandling = [None] * len(self.typ.get_argument_types())

        assert len(self.seqhandling) == len(self.typ.get_argument_types())

        if self.reduced_typ is None:
            self.reduced_typ = self.typ


SMGLOM_CONSTS: dict[str, ConstInfo] = {
    'https://stexmmt.mathhub.info/:sTeX?a=smglom/arithmetics&p=mod&m=intarith&s=greater than': ConstInfo(Typ.EET, ['conjunctwithrest', None]),
    'http://mathhub.info?a=smglom/mv&p=mod&m=equal&s=equal': ConstInfo(Typ.ET, ['pairwiseconjunct']),
    'http://mathhub.info?a=smglom/algebra&p=mod&m=magma/magma&s=operation': ConstInfo(Typ.EE, ['lassoc'], Typ.EEE),
    'http://mathhub.info?a=smglom/sets&p=mod&m=set&s=in': ConstInfo(Typ.EET, ['conjunctwithrest', None]),  # args `ai`
    'http://mathhub.info?a=smglom/algebra&p=mod&m=universe/universe&s=base set': ConstInfo(Typ.E),
    'http://mathhub.info?a=smglom/algebra&p=mod&m=monoid/monoid&s=unit': ConstInfo(Typ.E),
}

def get_smglom_type(uri: str) -> SimpleType:
    t = SMGLOM_CONSTS.get(uri)
    if t is None:
        raise NotImplementedError(f'Unknown type for {uri}')
    return t.typ
