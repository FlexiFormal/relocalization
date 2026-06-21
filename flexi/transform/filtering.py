"""
Type A: Parsing might have yielded two equivalent ASTs. Remove AST if other one is included.
Type B: Remove nonsensical ASTs.

Notes:
    * Type A can also act as AST normalization
"""

import dataclasses
from typing import Iterable

from flexi.parsing.mast import MAst, G, TermRef


class FilterResult:
    pass

class Keep(FilterResult):
    pass

class Discard(FilterResult):
    pass

@dataclasses.dataclass
class DiscardIfAlso(FilterResult):
    """ Discard AST if another AST is also present

    We use repr to check for equality.
    This needs better design.
    Subtle differences are allowed (but those should be invisible in repr)
    """
    other_mast_repr: str | set[str]


@dataclasses.dataclass
class FilteringCtx:
    reckless: bool = False   # if true, some "DiscardIfAlso" are turned into Discard (more efficient)
    language: str | None = None   # e.g. Eng (GF language suffix)


def filter_readings(readings: Iterable[MAst], ctx: FilteringCtx) -> Iterable[MAst]:
    """ TODO: This needs a cleaner algorithm...

    For example: because of the `DiscardIfAlso`s, the result depends on the ordering of readings.
    At the moment, this is only avoided (in critical places) by careful construction of filtering rules...
    """
    counter_in = 0
    counter_out = 0
    discard_ifs: list[tuple[MAst, set[str]]] = []
    yielded_mast_reprs: set[str] = set()

    for reading in readings:
        counter_in += 1
        discard: bool = False
        discard_if_masts: set[str] = set()

        # TODO: this should be more like a priority queue (to prioritize discarding filters)
        for filter in [filter_conj_ambig, filter_unnecessarily_high_annos]:
            result = filter(reading, ctx)
            if isinstance(result, Discard):
                discard = True
                break
            elif isinstance(result, DiscardIfAlso):
                discard_if_masts |= result.other_mast_repr if isinstance(result.other_mast_repr, set) else {result.other_mast_repr}

        if discard:
            pass
        elif discard_if_masts:
            discard_ifs.append((reading, discard_if_masts))
        else:
            yielded_mast_reprs.add(repr(reading))
            counter_out += 1
            yield reading

    for mast, ifs in discard_ifs:
        discard = False
        for i in ifs:
            if i in yielded_mast_reprs:
                discard = True
                break
        if not discard:
            yielded_mast_reprs.add(repr(mast))
            counter_out += 1
            yield mast

    print(f'KEPT {counter_out}/{counter_in} READINGS')

    # for reading in readings:
    #     do_filter: bool = False
    #     for filter in [filter_conj_ambig]:
    #         if filter(reading, ctx):
    #             do_filter = True
    #             break
    #     if not do_filter:
    #         yield reading

def filter_conj_ambig(reading: MAst, ctx: FilteringCtx) -> FilterResult:
    """ Type A.
    remove "(X and Y) and Z" in favor of "X and (Y and Z)"
    """
    for node in reading.find_children(lambda x: isinstance(x, G)):
        match node:
            case G(
                '~conj_stmt#', [
                    G('~and_conj#'),
                    G('~conj_stmt#', [G('~and_conj#'), x, y]),
                    z
                ]
            ):
                if ctx.reckless:
                    return Discard()
                else:
                    return DiscardIfAlso(
                        repr(
                            node.clone_from_root().replace_in_parent(
                                G(
                                    'conj_stmt',
                                    [
                                        x.clone(),
                                        G('conj_stmt', [
                                            G('and_conj', [y.clone(), z.clone()])
                                        ])
                                    ]
                                )
                            ).get_root()
                        ),
                    )
    return Keep()

# def filter_conj_ambig(reading: MAst, ctx: FilteringCtx) -> bool:
#     """ Type A.
#     remove "(X and Y) and Z" in favor of "X and (Y and Z)"
#     """
#     for node in reading.find_children(lambda x: isinstance(x, G)):
#         match node:
#             case G(
#                 '~conj_stmt#', [
#                     G('~and_conj#'),
#                     G('~conj_stmt#', [G('~and_conj#'), _, _]),
#                     _
#                 ]
#             ):
#                 return True
#     return False



def filter_unnecessarily_high_annos(reading: MAst, ctx: FilteringCtx) -> FilterResult:
    """ Type A.
    e.g. removes ASTs where "edges" is annotated as a NamedKind (or indefinitely quantified Term), instead of a Kind
    """
    for node in reading.find_children(lambda x: isinstance(x, TermRef)):
        match node:
            case TermRef(
                uri, [
                    G('~quantified_nkind#', [
                          G('~indefinite_quantification#') as quant,  # add more if necessary
                          G('~name_kind#', [
                              kind,
                              G('~no_idents_pl') as identifiers  # add more if necessary
                          ]) as named_kind_node,
                    ])
                ]
            ):
                return DiscardIfAlso(
                    {
                        # wrapped around kind
                        repr(
                            node.clone_from_root().replace_in_parent(
                                G('quantified_nkind', [
                                    quant.clone(),
                                    G('name_kind', [
                                        TermRef(uri, [kind.clone()],
                                                'wrapped_kind'  # could also e.g. be wrapped_kind2
                                                ),
                                        identifiers.clone()
                                    ])
                                ])
                            ).get_root()
                        ),
                        # wrapped around named kind
                        repr(
                            node.clone_from_root().replace_in_parent(
                                G('quantified_nkind', [
                                    quant.clone(),
                                    TermRef(uri, [named_kind_node.clone()], 'wrapped_named_kind')
                                ])
                            ).get_root()
                        )
                    }
                )

    return Keep()
