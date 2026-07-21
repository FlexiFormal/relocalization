import abc
import dataclasses
from typing import Iterable, TypeVar

from flexi.parsing.document import DocText, DocNode
from flexi.parsing.mast import MAst, G, M, MSeq, MI, Formula, MT, TermRef, X, TermDef, MathArg
from flexi.semconstr.conversion import finalized_convert, ConversionContext
from flexi.semconstr.logic import Expr, tptp_verify, Apply, Const, TptpConvCtx
from flexi.transform.astmatch import tagged, pattern_match
from flexi.transform.nldefcatalog import NlDefCatalog
from flexi.transform.utils import analyse_identifier, MastCheck, MastGen


T = TypeVar('T')
def not_none(x: T | None) -> T:
    assert x is not None
    return x


@dataclasses.dataclass
class RewritingContext:
    nl_def_catalog: NlDefCatalog = dataclasses.field(default_factory=NlDefCatalog)

    axioms: list[Expr] = dataclasses.field(default_factory=list)

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
            if (new := self.apply(node, ctx)) is not None:
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
            # ('~term_is_term_stmt#', [
            ('~term_is_kind_stmt#', [
                tagged('@any', 'precedent_subj'),
                # ('~quantified_nkind#', [
                #     '~indefinite_quantification#',
                #     ('~name_kind#', [
                        tagged('@any', 'kind'),
                #         '~no_idents_sg#',
                #     ])
                # ])
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

@dataclasses.dataclass
class VarChecker(abc.ABC):
    identifier: MAst
    expansion_notation_patterns : list[MAst] | None = None

    @classmethod
    def new(cls, m: MAst) -> VarChecker | None:
        if isinstance(m, M) and len(m) == 0 and m.omt == 'OMV' and len(m.notation_pattern) == 1:
            return SimpleVarChecker(m)
        if isinstance(m, M) and ':' not in m.value and m.omt == 'OMA':
            # might be sequence...
            if len(m) == 0:   # something like $\eseq!$
                raise NotImplementedError()
            elif len(m) == 1:
                # print(':::', m.notation_pattern)
                return SequenceVarChecker(m)
            else:
                raise NotImplementedError()   # tensors? (is that even supported by stex?)
        return None

    @abc.abstractmethod
    def matches(self, m: MAst) -> bool:
        pass

    @abc.abstractmethod
    def get_subst_for(self, m: MAst) -> MAst:
        pass

class SimpleVarChecker(VarChecker):
    """ plain identifier """

    def matches(self, m: MAst) -> bool:
        return m == self.identifier

    def get_subst_for(self, m: MAst) -> MAst:
        return MastGen.tuple(
            [
                M(
                    self.identifier.value + f'__{i}',
                    children=[],
                    notation_pattern=[self.expansion_notation_patterns[i]],
                    omt='OMV'
                )
                for i in range(len(self.expansion_notation_patterns))
            ]
        )

class SequenceVarChecker(VarChecker):
    """ indexed identifier """
    # TODO: Is the following even still true
    # self.identifier must have a notation for indexing (e.g. x_#1)

    def matches(self, m: MAst) -> bool:
        return isinstance(m, M) and self.identifier.value == m.value

    def get_subst_for(self, m: MAst) -> MAst:
        assert len(m) == 1   # TODO: What should we do otherwise? when is it even possible?
        m = MastGen.tuple(
            [
                M(
                    self.identifier.value + f'__{i}',
                    children=[m[0].clone()],
                    notation_pattern=[self.expansion_notation_patterns[i]],
                    omt='OMA'
                )
                for i in range(len(self.expansion_notation_patterns))
            ]
        )
        if 'avar' in str(m):
            print(m)
            raise Exception()
        return m
        return MI('mn', [MT('15')])


class RewriteTupleExpansion(RewriteRule):
    """
        for all c ∈ X×Y   ->   for all c1, c2 ∈ X×Y
        (this is also propagated for all other occurrences of c)
        Open problem: how to name the new identifiers...
    """
    applicable_to = G

    def __init__(self, restrict_to_var: VarChecker | None = None):
        self.var_checker = restrict_to_var

    # @classmethod
    # def is_var_check(cls, ident) -> bool:
    #     print(ident, ident.omt)
    #     return isinstance(ident, M) and len(ident) == 0 and ident.omt == 'OMV' and len(ident.notation_pattern) == 1

    def apply(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        is_match: bool = False
        var_checker = None
        blocked_paths: list[list[int]] = []   # in these paths, nothing should be substituted
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
                print('MATCH 1')
                if self.var_checker and not self.var_checker.matches(ident):
                    return None
                var_checker = self.var_checker or VarChecker.new(ident)
                if not var_checker:
                    return None
                if not isinstance(var_checker, SimpleVarChecker):
                    raise NotImplementedError()   # TODO

                is_match = True
                var_checker.expansion_notation_patterns = [
                    MI('msub', [ident.notation_pattern[0].clone(), MI('mn', [MT(str(i))])])
                    for i in range(len(sets))
                ]

            # sequence e_1, ..., e_n of edges
            case G(
                'kind2_to_kind',
                [
                    TermRef('http://mathhub.info?a=smglom/mv&p=mod&m=sequence&s=sequence'),
                    G(
                        'quantified_nkind', [
                            G('~indefinite_quantification#'),
                            (
                            G('~such_that_named_kind#', [G('name_kind', [kind, G('~no_idents_pl#') as idplace]), _])
                            | G('name_kind', [kind, G('~no_idents_pl#') as idplace])
                            )
                        ]
                    )
                ]
            ):
                # find identifiers of sequence by going up (to name_kind)
                node = None
                for parent in mast.parent_iter():
                    match parent:
                        case G('property_kind' | 'kind2_to_kind'):
                            continue
                        case G('name_kind'):
                            node = parent
                            break
                        case _:
                            break  # something else - abort
                if node is None:
                    return None

                node = node[1]   # identifier

                # now find identifier formula
                while True:
                    match node:
                        case G(
                            'cast_Identifiers_MaybeIdentifiers' | 'single_identifier' | 'formula_ident',
                            [child]
                        ) | Formula([child]):
                            node = child
                        case _:
                            break

                if self.var_checker and not self.var_checker.matches(node):
                    return None
                var_checker = self.var_checker or VarChecker.new(node)
                if not var_checker:
                    return None

                # raise Exception('MATCH2' + repr(node) + '  ' + repr(var_checker))
                is_match = True

                # arity/tuple size not known in this case (can only infer lower bound from existing projections)
                # instead, obtain it from definition. That also gives us better names for the components.

                # find referenced symbol
                if isinstance(kind, TermRef):
                    symbol = kind.value
                else:
                    # TODO: we might have search downwards a bit
                    return None

                # lookup definition
                for definition in ctx.nl_def_catalog.definitions.get(symbol, []):
                    if var_checker.expansion_notation_patterns:
                        break
                    for text in definition.find_children(lambda n: isinstance(n, DocText)):
                        if var_checker.expansion_notation_patterns:
                            break
                        assert isinstance(text, DocText)   # make linter happy
                        for sentence in text.sentences:
                            options: list[list[MAst] | None] = []   # options of how it can be written as a tuple
                            for reading in sentence:
                                termdef = reading.find_child(lambda x: isinstance(x, TermDef) and x.value == symbol)

                                # now: go up to definition root and then down to find relevant tuple representation

                                n = not_none(termdef.get_parent())
                                while True:
                                    match n.get_parent():
                                        case G('name_kind' | '~define_nkind_as_nkind#'):
                                            n = not_none(n.get_parent())
                                        case _:
                                            break

                                if n.value != '~define_nkind_as_nkind#':
                                    options.append(None)  # failure for this sentence
                                    break

                                n = n[0]

                                while True:
                                    match n:
                                        case G('~such_that_named_kind#'):
                                            n = n[0]
                                        case G('name_kind', [_,
                                            G('cast_Identifiers_MaybeIdentifiers', [
                                                G('single_identifier', [
                                                    G('formula_ident', [Formula([formula])])
                                                ])
                                            ])
                                        ]):
                                            n = formula
                                            break
                                        case _:
                                            raise NotImplementedError(n)

                                match n:
                                    case M('https://mathhub.info?a=smglom/sets&p=mod&m=cartesian-product&s=tuple', [MSeq(s)]):
                                        options.append(s)
                                    case _:
                                        raise NotImplementedError(n)



                            if not options or None in options:  # didn't work
                                continue
                            if not all(o == options[0] for o in options): # ambiguity
                                continue
                            option = options[0]
                            if not all(isinstance(o, M) and len(o) == 0 and ':' not in o.value for o in option):  # only accept if it is a list of plain variables
                                continue
                            var_checker.expansion_notation_patterns = [
                                MI('msub', [
                                    o.notation_pattern[0].clone() if len(o.notation_pattern) == 1 else MI('mrow', o.notation_pattern.clone()),
                                    MathArg('1')
                                ])
                                for o in option
                            ]

                            # we should not substitute the sequence declaration
                            block_node = mast
                            while True:
                                match block_node:
                                    case G('property_kind' | 'kind2_to_kind'):
                                        block_node = not_none(block_node.get_parent())
                                    case G('name_kind'):
                                        block_node = block_node[1]
                                        break
                                    case _:
                                        raise NotImplementedError(block_node)
                            blocked_paths.append(block_node.get_path())

                            # introduce e_i := (...)
                            mast_path = mast.get_path()
                            _clone = mast.get_root().clone()
                            kvar = M('__kvar', notation_pattern=[MI('mi', [MT('𝑘')])], children=[], omt='OMV')
                            c = var_checker.identifier.clone()
                            c._children = []
                            c.append_child(kvar)
                            _clone.follow_path(idplace.get_path()).replace_in_parent(
                                G('cast_Identifiers_MaybeIdentifiers', [
                                    G('single_identifier', [
                                        G('formula_idents', [Formula([
                                            MastGen.def_eq(
                                                c,
                                                var_checker.get_subst_for(c)
                                            )
                                        ], 'dollarmath'
                                        )])
                                    ])
                                ])
                            )
                            blocked_paths.append(idplace.get_path())
                            mast = _clone.follow_path(mast_path)

                if var_checker.expansion_notation_patterns:
                    is_match = True

                # TODO:
                #   insert e_k := (...) into `idplace`
                #   set notation_pattern
                # var_checker.expansion_notation_patterns = ...



        if not is_match:
            return None

        assert var_checker is not None
        clone = mast.get_root().clone()
        for n in clone.find_children(lambda n: isinstance(n, M)):
            if not var_checker.matches(n):
                continue
            npath = n.get_path()
            if any(path == npath[:len(path)] for path in blocked_paths):
                continue

            # TODO: When do we actually want this?
            # parent = n.get_parent()
            # if isinstance(parent, MSeq) and len(parent) == 1:
            #     # replace a sequence argument with the tuple elements
            #     parent.replace_in_parent(MSeq(parent.value, [v.clone() for v in new_vars]))

            # n.replace_in_parent(MastGen.tuple([v.clone() for v in new_vars]))
            n.replace_in_parent(var_checker.get_subst_for(n))

        return clone.get_root()

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
                        'http://mathhub.info?a=smglom/sets&p=mod&m=cartesian-product&s=projectionFN',
                        [MI('mn' | 'mi', [MT(indexStr)])]
                    ),
                    arg
                ]
            ):
                print('MATCH')
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
                if self.attempt_tuple_expansion and (var_checker := VarChecker.new(arg)):
                    print('TRIGGER TUPLE EXP')
                    # delegate to RewriteTupleExpansion
                    return RewriteTupleExpansion(restrict_to_var=var_checker).apply_somewhere_once(mast.get_root(), ctx)
        return None


class RewriteComprehensionReduction(RewriteRule):
    """
        element of {t | t is a foo}  ->  foo
    """

    applicable_to = G

    def apply(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        match mast:
            case G('kind2_to_kind', [
                TermRef('https://mathhub.info?a=smglom/sets&p=mod&m=set&s=element'),
                G('formula_term',[Formula([M(
                    'http://mathhub.info?a=smglom/sets&p=mod&m=set&s=set comprehension',
                    [
                        t1, t2, MI('mtext', [
                        # TODO: is the div always there?
                        X('div', [
                            # G('term_is_term_stmt', [
                            #     G('formula_term', [Formula([t3])]),
                            #     G('~quantified_nkind#', [
                            #         G('~indefinite_quantification#'),
                            #         G('name_kind', [kind, G('~no_idents_sg#')])
                            #     ])
                            # ])
                            G('term_is_kind_stmt', [
                                G('formula_term', [Formula([t3])]),
                                kind
                            ])
                        ])
                    ])
                    ]
                )])])
            ]):
                if t1 == t2 == t3:
                    clone = mast.clone_from_root()
                    clone.replace_in_parent(kind.clone())
                    return clone.get_root()
                return None


class RewriteAccumulateThatIsProperty(RewriteRule):
    """
       integer that is even that is positive -> integer that is even and positive
    """

    def apply(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        match mast:
            case G('nkind_that_is_property', [
                G('nkind_that_is_property', [nkind, pol1, prop1]),
                pol2,
                prop2
            ]):
                if pol1 != pol2:
                    return None
                clone = mast.clone_from_root()
                clone.replace_in_parent(
                    G('nkind_that_is_property_list', [
                        nkind.clone(),
                        pol1.clone(),
                        G('BasePropertyList', [prop1.clone(), prop2.clone()])
                    ])
                )
                return clone.get_root()


class RewriteEliminateRedundantInfo(RewriteRule):
    def __init__(self, variant: int = 0):
        self.variant = variant    # one node can potentially trigger multiple rewrite variants


    def apply(self, mast: MAst, ctx: RewritingContext) -> MAst | None:
        def check(m: MAst) -> bool:
            return tptp_verify(
                Apply.multi(Const.Equivalence, finalized_convert(mast.get_root(), ConversionContext()), finalized_convert(m, ConversionContext())),
                ctx.axioms,
                TptpConvCtx(time_out_as_fail=True),
            )

        match mast:
            case G('conj_stmt', [conj, a, b]):
                if self.variant == 0:
                    m = mast.clone_from_root().replace_in_parent(a.clone()).get_root()
                elif self.variant == 1:
                    m = mast.clone_from_root().replace_in_parent(b.clone()).get_root()
                else:
                    return None
                if check(m):
                    return m

        return None
