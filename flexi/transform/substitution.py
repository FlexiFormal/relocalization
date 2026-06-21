import dataclasses
from copy import deepcopy

from flexi.parsing.mast import MAst, TermRef, M, MI, MT, G, Formula
from flexi.transform.utils import get_new_var_id, MastGen


@dataclasses.dataclass
class SubstitutionContext:
    existing_vars: set[str]     # variables in the original MAst (the `data-ftml-head`s)


def substitute(mast: MAst, substitutions: dict[str, list[MAst]]) -> MAst:
    # print('-'*10)
    # for k, v in substitutions.items():
    #     print(k, '⟶', v)
    # print('-'*10)

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


def _is_property(mast: MAst) -> bool:
    match mast:
        case G('property2_to_property'):
            return True
        case TermRef(_, [x]):
            return _is_property(x)
    # TODO: other cases
    return False



def substitute_actual(mast: MAst, substitutions: dict[str, list[MAst]], ctx: SubstitutionContext) -> MAst:
    """ modifies the mast in place """

    # TODO: This function already grows unreasonably large.
    # We need to factor out different substitution cases into separate functions or something like that

    # check if the current node must be modified
    if isinstance(mast, TermRef) and mast.value in substitutions:
        # print('YES', mast.value)
        parent = mast.get_parent()
        value = substitutions[mast.value][0]   # TODO: cover all variants
        if isinstance(parent, G):
            # if it's a Kind...
            if (parent.value, mast.get_parent_pos()) in [
                ('name_kind', 0),   # TODO: more options
            ]:
                if isinstance(value, M):
                    # replace it with "element of ..." as Kinds are sets
                    mast.replace_in_parent(
                        # TODO: most of this should go into MastGen
                        G(
                            'kind2_to_kind',
                            [
                                TermRef(
                                    'https://mathhub.info?a=smglom/sets&p=mod&m=set&s=element',
                                    [
                                        # TODO: this is just the verbalization from `automata.lexion`
                                        G('http://mathhub.info?a=smglom/sets&p=mod&m=set&s=element__verb0')
                                    ],
                                    wrapfun='wrapped_kind2',
                                ),
                                G('formula_term', [Formula([value.clone()], 'dollarmath')])
                            ]
                        )
                    )
                else:
                    raise NotImplementedError()

            # replacing property used as `property_kind` with a roperty
            elif (parent.value, mast.get_parent_pos()) in [
                ('property_kind', 0),
            ]:
                if _is_property(value):
                    # remove property
                    parent.replace_in_parent(parent[1].clone())
                    # find name_kind parent
                    n = parent
                    while n is not None and isinstance(n, G) and str(n.value) in {'property_kind'}:
                        n = n.get_parent()
                    if n is not None and isinstance(n, G) and n.value == 'name_kind':
                        n.replace_in_parent(
                            G(
                                'nkind_that_is_property',
                                [
                                    n.clone(),
                                    G('positive_pol'),
                                    value.clone(),
                                ]
                            )
                        )
                    else:
                        raise NotImplementedError('only support for named kinds')
                else:
                    raise NotImplementedError('only support for properties')
            else:
                raise NotImplementedError(
                    f'unsupported combination: {(parent.value, mast.get_parent_pos())} for {mast}'
                )
        else:
            # print(mast)
            # print(mast.get_parent())
            # print(value)
            raise NotImplementedError()   # TODO

    elif isinstance(mast, M) and mast.value in substitutions:
        value = substitutions[mast.value][0]   # TODO: cover all variants
        if isinstance(value, M):
            value = deepcopy(value)
            _rename_new_vars(value, ctx)
            # TODO: better heuristic for when we need parentheses
            if len(value) > 0:
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


