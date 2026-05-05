import abc
import dataclasses
from typing import Iterable

from flexi.parsing.mast import MAst, G, M, MSeq, MI, Formula, MT
from flexi.transform.astmatch import tagged, pattern_match
from flexi.transform.utils import analyse_identifier, MastCheck, MastGen


@dataclasses.dataclass
class RewritingContext:


    # the following ones are used to control the behavior of specific rules

    focus_var: str | None = None


class RewriteRule(abc.ABC):
    # none means applicable to all MAst nodes
    # in some settings, this can be used for optimization (only calling apply if it could be applicable)
    applicable_to: type[MAst] | None = None

    @abc.abstractmethod
    def apply(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        """ Applies the rewrite rule to the node mast (does not search recursively) """

    def apply_somewhere(self, mast: MAst, ctx: RewritingContext) -> Iterable[MAst]:
        for node in mast.find_children(
                filter=lambda n: (isinstance(n, self.applicable_to) if self.applicable_to else True),
                recurse_on_match=True,
        ):
            if new := self.apply(node, ctx):
                yield new

    def apply_somewhere_once(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        try:
            return next(iter(self.apply_somewhere(mast, ctx)))
        except StopIteration:
            return None




class RewritePullKindIntoUnivQuant(RewriteRule):
    """
    "for every x, if x is a foo then φ" ⟶ "for every foo x, φ"
    """
    applicable_to = G

    _pattern = ('~for_term_stmt#', [
        (tagged('~if_then_stmt#', 'body'), [
            ('~term_is_term_stmt#', [
                tagged('@any', 'precedent_subj'),
                ('~quantified_nkind#', [
                    '~indefinite_quantification#',
                    ('~name_kind#', [
                        tagged('@any', 'kind'),
                        '~no_idents_sg#',
                    ])
                ])
            ]),
            tagged('@any', 'antecedent')
        ]),
        ('~quantified_nkind#', [
            '~universal_quantification#',
            (tagged('~identifiers_as_nkind#', 'nkind'), [('~single_identifier#', [tagged('@any', 'quant_ids')])])
        ])
    ])

    def apply(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        if not (pm := pattern_match(mast, self._pattern)):
            return None
        precedent_subj = pm.tag_to_mast['precedent_subj']
        quant_ids = pm.tag_to_mast['quant_ids']

        p_analysis = analyse_identifier(precedent_subj)
        q_analysis = analyse_identifier(quant_ids)

        if p_analysis is None or q_analysis is None:
            return None

        if p_analysis.restriction or q_analysis.restriction:
            return None   # TODO: support this

        if sorted(p_analysis.identifiers) != sorted(q_analysis.identifiers):
            return None

        # let's rewrite
        copy = mast.get_root().clone()
        body = pm.tag_to_mast['body']
        antecedent = pm.tag_to_mast['antecedent']
        nkind = pm.tag_to_mast['nkind']
        kind = pm.tag_to_mast['kind']
        copy.follow_path(body.get_path()).replace_in_parent(antecedent)
        copy.follow_path(nkind.get_path()).replace_in_parent(
            G('name_kind', [kind.clone(), G('cast_Identifiers_MaybeIdentifiers', [G('single_identifier', [quant_ids.clone()])])])
        )

        return copy


class RewriteBetaReduction(RewriteRule):
    applicable_to = M

    def apply(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        match mast:
            case M(
                'http://mathhub.info?a=FTML/meta&m=Metatheory&s=apply', [
                    M('http://mathhub.info?a=smglom/sets&p=mod&m=functions&s=assign', [vars_, body]),
                    arg
                ]
            ):
                # pre-process vars
                if MastCheck.is_var(vars_):
                    processed_vars = [vars_]
                elif (
                        isinstance(vars_, MI)
                        and vars_.value == 'mrow'
                        and all(MastCheck.is_comma(c) for c in list(vars_)[1::2])
                        and all(MastCheck.is_var(c) for c in list(vars_)[::2])
                ):
                    processed_vars = list(vars_)[::2]
                else:
                    return None

                # pre-process arg
                if isinstance(arg, MSeq):
                    processed_args = list(arg)
                else:
                    processed_args = [arg]

                if len(processed_args) == 1 and len(processed_vars) > 1:
                    # use projections
                    processed_args = [
                        MastGen.apply(MastGen.projection(i + 1), processed_args[0].clone()) for i in range(len(processed_vars))
                    ]

                if len(processed_args) != len(processed_vars):
                    return None

                # perform substitution
                if mast.is_root():
                    copy = body.clone()
                else:
                    copy = mast.get_root().clone()
                    copy.follow_path(mast.get_path()).replace_in_parent(
                        copy.get_root().follow_path((body.get_path()))   # replace function application with function body
                    )
                    copy = copy.follow_path((mast.get_path()))

                # now copy should point to the body in a clone

                for v in copy.find_children(MastCheck.is_var):
                    for var, arg in zip(processed_vars, processed_args):
                        if v == var:
                            v.replace_in_parent(arg)
                return copy.get_root()

            case _:
                return None


class RewriteTupleExpansion(RewriteRule):
    """
        for all c ∈ X×Y   ->   for all c1, c2 ∈ X×Y
        (this is also propagated for all other occurrences of c)
        Open problem: how to name the new identifiers...
    """
    applicable_to = G

    def __init__(self, restrict_to_var: str | None = None):
        self.restrict_to_var = restrict_to_var

    @classmethod
    def is_var_check(cls, ident) -> bool:
        return isinstance(ident, M) and len(ident) == 0 and ident.omt == 'OMV' and len(ident.notation_pattern) == 1

    def apply(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        match mast:
            case G(
                'quantified_nkind',
                [
                    _quantifier,
                    G('identifiers_as_nkind', [G('single_identifier', [G('formula_ident', [Formula([
                        M('http://mathhub.info?a=smglom/sets&p=mod&m=set&s=in',
                          [MSeq([ident]), M('http://mathhub.info?a=smglom/sets&p=mod&m=cartesian-product&s=Cartesian product', [MSeq(sets)])
                    ])])])])])
                ]
            ):
                print('YAY')
                if not (self.is_var_check(ident) and (self.restrict_to_var is None or ident.value == self.restrict_to_var)):
                    return None
                new_vars = [
                    M(
                        ident.value + f'__{i}',
                        children=[],
                        notation_pattern=[
                            MI('msub', [ident.notation_pattern[0].clone(), MI('mn', [MT(str(i))])])
                        ],
                        omt='OMV'
                    )
                    for i in range(len(sets))
                ]

                # substitute every (as sequence if current var single element in MSeq, otherwise as tuple)
                def _equals_ident(i):
                    return isinstance(i, M) and i.omt == ident.omt and i.value == ident.value

                clone = mast.get_root().clone()
                for n in clone.find_children(lambda n: isinstance(n, M)):
                    if not _equals_ident(n):
                        continue
                    parent = n.get_parent()

                    # TODO: When do we actually want this?
                    # if isinstance(parent, MSeq) and len(parent) == 1:
                    #     # replace a sequence argument with the tuple elements
                    #     parent.replace_in_parent(MSeq(parent.value, [v.clone() for v in new_vars]))

                    n.replace_in_parent(MastGen.tuple([v.clone() for v in new_vars]))

                return clone.get_root()

        return None


class RewriteProjectionReduction(RewriteRule):
    """
        π_1(⟨a,b⟩)  ->  a

        If attempt_tuple_expansion is true, and we have, e.g., π_1(c)
        then RewriteTupleExpansion is called in the hope of replace c with a tuple.
    """

    applicable_to = M

    def __init__(self, attempt_tuple_expansion: bool):
        self.attempt_tuple_expansion = attempt_tuple_expansion

    def apply(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        match mast:
            case M(
                'http://mathhub.info?a=FTML/meta&m=Metatheory&s=apply',
                [
                    M(
                        'http://mathhub.info?a=smglom/sets&amp;p=mod&amp;m=cartesian-product&amp;s=projectionFN',
                        [MI('mn', [MT(indexStr)])]
                    ),
                    arg
                ]
            ):
                if not indexStr.isdigit():
                    return None
                index = int(indexStr) - 1
                match arg:
                    case M(
                        'http://mathhub.info?a=smglom/sets&p=mod&m=cartesian-product&s=tuple',
                        [MSeq(tuplecontents)]
                    ):
                        if index not in range(len(tuplecontents)):
                            return None
                        clone = mast.clone_from_root()
                        clone.replace_in_parent(tuplecontents[index].clone())
                        return clone.get_root()
                if self.attempt_tuple_expansion and RewriteTupleExpansion.is_var_check(arg):
                    print('TRIGGER TUPLE EXP')
                    # delegate to RewriteTupleExpansion
                    return RewriteTupleExpansion(restrict_to_var=arg.value).apply_somewhere_once(mast.get_root(), ctx)
        return None
