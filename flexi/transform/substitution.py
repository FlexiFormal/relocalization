import dataclasses
from copy import deepcopy

from flexi.parsing.mast import MAst, TermRef, M, MI, MT, G, Formula
from flexi.transform.utils import get_new_var_id, MastGen


@dataclasses.dataclass
class SubstitutionContext:
    existing_vars: set[str]     # variables in the original MAst (the `data-ftml-head`s)


def substitute(mast: MAst, substitutions: dict[str, list[MAst]]) -> MAst:

    existing_vars: set[str] = set()
    for node in mast.find_children(lambda x: isinstance(x, M) and x.omt == 'OMV'):
        existing_vars.add(node.value)

    ctx = SubstitutionContext(existing_vars)
    return substitute_actual(mast.clone_from_root(), substitutions, ctx)


def _rename_new_vars(mast: MAst, ctx: SubstitutionContext):
    subst: dict[str, str] = {}
    for node in mast.find_children(lambda x: isinstance(x, M) and x.omt == 'OMV'):
        if node.value in ctx.existing_vars:
            if node.value not in subst:
                subst[node.value] = get_new_var_id()
            node.value = subst[node.value]
            # TODO: should we also update the notation/presentation?



def substitute_actual(mast: MAst, substitutions: dict[str, list[MAst]], ctx: SubstitutionContext) -> MAst:
    """ modifies the mast in place """

    # check if the current node must be modified
    if isinstance(mast, TermRef) and mast.value in substitutions:
        parent = mast.get_parent()
        value = substitutions[mast.value][0]   # TODO: cover all variants
        if isinstance(parent, G):
            # if it's a Kind...
            if (parent.value, mast.get_parent_pos()) in [
                ('name_kind', 0),   # TODO: more options
            ]:
                if isinstance(value, M):
                    # replace it with "element of ..." as Kinds are sets
                    return mast.clone_from_root().replace_in_parent(
                        # TODO: most of this should go into MastGen
                        G(
                            'kind2_to_kind',
                            [
                                TermRef(
                                    'https://mathhub.info?a=smglom/sets&p=mod&m=set&s=element',
                                    [
                                        # TODO: this is just the verbalization from `automata.lexion`
                                        G('http://mathhub.info?a=smglom/sets&p=mod&m=relation&s=element__verb0')
                                    ],
                                    wrapfun='wrapped_kind2',
                                ),
                                G('formula_term', [Formula([value.clone()], 'dollarmath')])
                            ]
                        )
                    )

        # print(mast)
        # print(mast.get_parent())
        # print(value)
        raise NotImplementedError()   # TODO

    elif isinstance(mast, M) and mast.value in substitutions:
        value = substitutions[mast.value][0]   # TODO: cover all variants
        if isinstance(value, M):
            value = deepcopy(value)
            _rename_new_vars(value, ctx)
            # TODO: we don't always need parentheses
            value.notation_pattern = [MI('mo', [MT('(')])] + value.notation_pattern + [MI('mo', [MT(')')])]
            children = [child.clone() for child in mast]
            for child in children:
                value = MastGen.apply(value, child)
            if mast.is_root():
                return value
            else:
                mast.replace_in_parent(value)
        else:
            raise NotImplementedError()

    else:
        for child in mast:
            substitute_actual(child, substitutions, ctx)

    return mast


