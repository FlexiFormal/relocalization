import re
from copy import deepcopy

from flexi.parsing.mast import MAst, G, Formula, M, MSeq, TermDef, MI, MT
from flexi.semconstr.logic import QLF, Apply, Lambda, NewVar, Iff, DRS, Typ, And, Const, NamedVar, Seq, Var, TRUE


def convert_1(m: MAst) -> QLF:
    """
    Step 1 in the conversion (MAst -> QLF)

    Note on types:
        * T/E for propositions/entities, but rendered as ο/ι because I prefer that :)
        * NPs ('Term' in Magma) are type-raised in the usual way, i.e. (ι ⟶ ο) ⟶ ο.
        * Identifiers are (ι ⟶ ο) ⟶ ο, with the return value being a DRS with the identifiers/variables as referents

    Other thoughts:
        * We could have separate functions depending on the syntactic category of the MAst.
          Not sure if that makes things tidier or more convoluted...
    """
    conv = convert_1
    if isinstance(m, G):
        fun = m.value
        # strip variant sufix
        if match := re.match(r'(.*)_v[0-9]+$', fun):
            fun = match.group(1)

        if fun.startswith('lex_'):
            return _convert_1_lex_helper(fun)

        match (fun, list(m)):
            case ('stmt_sentence', [stmt]):
                return conv(stmt)
            case ('formula_stmt', [formula]):
                return Apply(conv(formula), Lambda(NewVar(Typ.E), TRUE()))
            case ('subj_stmt', [subj, a, b]):
                return Apply.multi(conv(subj), conv(a), conv(b))
            case ('iff_subj', []):
                return Lambda.multi(a := NewVar(Typ.T), b := NewVar(Typ.T), body=Iff(a, b))
            case ('term_is_property_stmt', [term, property]):
                return Apply(conv(term), conv(property))
            case ('quantified_nkind', [quant, nkind]):
                nk = conv(nkind)
                assert isinstance(nk, DRS)
                return _convert_1_quant_helper(quant, nk)
            case ('name_kind', [kind, maybe_identifiers]):
                k = conv(kind)
                ids = conv(maybe_identifiers)
                # we need to beta reduce to get a DRS (so that the DRS is top-level for quantification)
                result = Apply(ids, k).force_single_beta_reduction()
                assert isinstance(result, DRS)
                return result

                # assert isinstance(result, DRS)
                # for ref in result.referents:
                #     result.conditions.append(Apply(k, ref))
            case ('prekind_to_kind', [prekind]):
                return conv(prekind)
            case ('cast_Identifiers_MaybeIdentifiers', [identifiers]):
                return conv(identifiers)
            case ('single_identifier', [identifier]):
                return conv(identifier)
                # drs = conv(identifier)
                # assert isinstance(drs, DRS)
                # if not len(drs.referents) == 1:
                #     raise ValueError(f'Expected exactly one referent for single_identifier, got {len(drs.referents)}')
                # return drs
            case ('formula_ident', [math]):
                return conv(math)
    elif isinstance(m, Formula):
        assert len(m) == 1
        refables = _extract_refables(m[0])
        formula = _convert_1_math_helper(m[0])
        p = NewVar(Typ.ET)

        return Lambda(
            p,
            DRS(
                [r for r in refables if isinstance(r, Var)],
                [
                    Apply(p, r) for r in refables if not isinstance(r, Var)
                ] + [
                    formula
                ]
            )
        )
    elif isinstance(m, TermDef):
        if m.wrapfun == 'wrapped_property':
            typ = Typ.ET
        elif m.wrapfun == 'wrapped_sentence':
            typ = Typ.T
        else:
            raise NotImplementedError(f'Unknown wrapfun {m.wrapfun} in TermDef')
        return Const(m.value, typ)



        # return conv(m[0])
    # elif isinstance(m, M):  # semantic math node
    #     if m.value.startswith('http://') or m.value.startswith('https://'):
    #         ...
    #     else:  # it must be a variable (I suppose)
    #         ...

    raise NotImplementedError(f'Conversion for {m} not implemented yet')


def _extract_refables(m) -> list[QLF]:
    """
    Returns referenceable terms from a formula.

    Examples:
        * $x$ -> [x]
        * $x, y \in S$ -> [x, y]
        * $f(x) > 0$ -> [f(x)]
    """

    extract = _extract_refables

    if isinstance(m, M):
        if m.value.startswith('http://') or m.value.startswith('https://'):
            if is_relation(m.value):
                return extract(m[0])
            else:   # a term?
                return [_convert_1_math_helper(m)]
        else:  # I guess it must be a variable (or possibly a constant...)
            return [NamedVar(m.value, Typ.E, is_semantic=True)]
    elif isinstance(m, MSeq):
        return [_convert_1_math_helper(c) for c in m]
    else:
        raise NotImplementedError(f'Cannot extract refables from {m}')

def _convert_1_math_helper(m) -> QLF:
    """ plain conversion of a formula to a QLF expression """
    conv = _convert_1_math_helper

    if isinstance(m, M):
        return Apply.multi(Const(m.value, Typ.Any), *[conv(c) for c in m])
    elif isinstance(m, MSeq):
        return Seq(*[conv(c) for c in m])
    elif isinstance(m, MI):
        assert len(m) == 1
        assert isinstance(m[0], MT)
        # TODO: what about constants?...
        return NamedVar(m[0].value, Typ.E, is_semantic=False)
    else:
        raise NotImplementedError(f'Cannot convert math node {m} to QLF')

def _convert_1_quant_helper(quantification: str, nkind: DRS) -> QLF:
    """
    quantifies referents from (top-level) DRS nkind
    """
    match quantification:
        case G('indefinite_quantification', []):
            p = NewVar(Typ.ET)
            body = nkind
            for ref in nkind.referents:
                body = And(body, Apply(p, ref))
            return Lambda(p, body)

    raise NotImplementedError(f'Conversion for quantification {quantification} not implemented yet')

def _convert_1_lex_helper(lex: str) -> QLF:
    """
    Hard-coded conversion for a few lexical entries.
    This is only intended as an initial solution to get off the ground.
    """
    match lex:
        case 'lex_integer':
            return Const('integer', Typ.ET)

    raise NotImplementedError(f'Conversion for lexical item {lex} not implemented yet')


def is_relation(uri: str) -> bool:
    """
    Temporary hack until we can get the signature from FLAMS or something like that
    """
    return (uri in {
        'https://stexmmt.mathhub.info/:sTeX?a=smglom/arithmetics&p=mod&m=intarith&s=greater than',
    })
