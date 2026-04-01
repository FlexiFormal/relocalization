import abc
from typing import Iterable

from flexi.parsing.mast import MAst, G
from flexi.transform.astmatch import tagged, pattern_match
from flexi.transform.utils import analyse_identifier


class RewritingContext:
    pass


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




# For all v0 , ( if v0 is a class then for all v1 , ... ) .
#
#
# (stmt_sentence (
#
# for_term_stmt (bracketed_stmt (
#
# if_then_stmt_v1 (term_is_term_stmt (cast_term (identifier_term (v0 ))) (quantified_nkind (indefinite_quantification ) (name_kind (class__verb0 ) (no_idents_sg ))))
#
# ...)
#
#
# (quantified_nkind (universal_quantification_v1 ) (identifiers_as_nkind (single_identifier (cast_identifier (cast_restricted_identifier (v0 ))))))))



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
        print('HERE')
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
        # copy.follow_path(antecedent.get_path()).replace_in_parent(
        #     G('name_kind', [nkind.clone(), quant_ids.clone()])
        # )

        return copy



'''
def rewrite_pull_kind_into_univ_quant(mast: MAst) -> Iterable[MAst]:
    """
    "for every x, if x is a foo then φ" ⟶ "for every foo x, φ"
    """
    for node in mast.find_children(lambda n: isinstance(n, G)):
        match node:
            case G(
                '~for_term_stmt#',
                [
                    stmt,
                    G(
                        '~quantified_nkind#', [
                            G('~universal_quantification#'),
                            G('identifiers_as_nkind', [identifers])
                        ]
                    ),
                ]
            ):
                f, s = dewrap(stmt)
                if not isinstance(s, G) and s.value == '~if_then_stmt#':
                    continue
'''

