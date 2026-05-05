import dataclasses

from lxml.etree import _Element, _Comment

from flexi.parsing.gfxml import build_tree, xify, parse_mtext_contents
from flexi.parsing.magma import MagmaGrammar
from flexi.parsing.mast import MAst, gf_xml_math_to_mast


@dataclasses.dataclass
class Morphism:
    assignments: dict[str, list[MAst]]

    domain: str
    codomain: str | None = None   # do we need this? (it's a bit trickier to extract)


@dataclasses.dataclass
class MorphismExtractionContext:
    grammar: MagmaGrammar


def _only_noncomment_child(node: _Element) -> _Element:
    ncs = [child for child in node if not isinstance(child, _Comment)]
    if not len(ncs) == 1:
        raise ValueError(f'Expected only one child node, got {ncs}')
    return ncs[0]


def extract_from_extstructure_interpretmodule(extstructure: _Element, ctx: MorphismExtractionContext) -> Morphism:
    if not 'data-ftml-feature-structure' in extstructure.attrib:
        raise ValueError('Expected data-ftml-feature-structure attribute in extstructure element')

    root: _Element | None = None
    for child in extstructure:
        if 'data-ftml-feature-morphism' in child.attrib:
            root = child
            # TODO: can there be multiple?
            break

    if root is None:
        raise ValueError('Expected data-ftml-feature-morphism attribute in child of extstructure element')

    assignments: dict[str, _Element] = {}

    for child in root.iterdescendants():
        if not isinstance(child, _Element):
            continue
        if not 'data-ftml-assign' in child.attrib:
            continue

        asgnmt = _only_noncomment_child(child)
        if 'data-ftml-definiens' in asgnmt.attrib:
            asgnmt = _only_noncomment_child(asgnmt)

        # formula has only one reading ...
        gf_xml_tree = build_tree([xify(asgnmt)], 'dollarmath "0"')
        # ... unless we parse textual content, which can be ambiguous
        gf_xml_trees = parse_mtext_contents(
            lambda s: ctx.grammar.parse_to_aststr(s, category='Statement'),
            gf_xml_tree
        )

        print('TRYING', )
        masts = [gf_xml_math_to_mast(gxt) for gxt in gf_xml_trees]
        print('success')

        assignments[child.attrib['data-ftml-assign']] = masts

    return Morphism(
        assignments=assignments,
        domain=root.attrib['data-ftml-domain'],
    )

