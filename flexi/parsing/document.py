"""
Light-weight representation of a document.
It enforces very little structure at the moment.
This might be a bad trade-off – we'll have to see.
"""

from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path
from typing import Iterable, Callable, Literal

from lxml import etree

from flexi.parsing import gfxml
from flexi.parsing.magma import Sentence, MagmaGrammar
from flexi.parsing.mast import gf_xml_to_mast


class DocNode:
    """ base class for all document nodes (should not be used directly) """

    def __init__(self, children: list[DocNode] = None):
        self.children = children if children is not None else []

    def find_children(
            self,
            filter: Callable[[DocNode], bool],
            recurse_on_match: bool = True,
    ) -> Iterable[DocNode]:
        if filter(self):
            yield self
            if not recurse_on_match:
                return
        for child in self.children:
            yield from child.find_children(filter, recurse_on_match)

    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(repr(c) for c in self.children)})'


class DocText(DocNode):
    def __init__(self, sentences: list[Sentence]):
        super().__init__()
        self.sentences = sentences


class Paragraph(DocNode):
    def __init__(self, children: list[DocNode], label: str = ''):
        super().__init__(children)
        self.label = label


class Definition(Paragraph):
    pass


class Statement(Paragraph):
    def __init__(
            self,
            children: list[DocNode],
            type_: Literal['theorem', 'proposition', 'axiom'] = 'proposition',
            label: str = ''
    ):
        super().__init__(children, label=label)
        self.type_ = type_


class Proof(Paragraph):
    pass


class DocGroup(DocNode):
    pass


def ftml_to_doc(ftml: etree._Element | Path, grammar: MagmaGrammar) -> DocNode:
    if isinstance(ftml, Path):
        ftml = etree.parse(str(ftml), parser=etree.HTMLParser()).getroot()

    result = ftml_to_doc_actual(deepcopy(ftml), grammar)
    print(result)
    # Still should simplify the result

    def _simplify(node: DocNode):
        new_children: list[DocNode] = []
        for child in node.children:
            _simplify(child)
            if isinstance(child, DocGroup):
                if not child.children:
                    continue
                if len(child.children) == 1 and isinstance(child.children[0], DocGroup):
                    child = child.children[0]
            if isinstance(child, DocText) and not child.sentences:
                continue
            new_children.append(child)
        node.children = new_children

    result = DocGroup([result])
    _simplify(result)
    return result.children[0]



def ftml_to_doc_actual(
        ftml: etree._Element,
        grammar: MagmaGrammar,
        run_sentence_extraction: bool = True,
) -> DocNode:
    """ breaks the DOM in the process -> pass clone """
    def _remove(element: etree._Element):
        """ remove element from its parent """
        new_node = etree.Element('span')
        new_node.tail = element.tail
        if element.getparent() is not None:
            element.getparent().replace(element, new_node)

    if 'data-ftml-definition' in ftml.attrib:
        ftml.attrib.clear()
        definition = Definition([ftml_to_doc_actual(ftml, grammar)])
        _remove(ftml)
        return definition

    children: list[DocNode] = []
    for child in ftml:
        children.append(ftml_to_doc_actual(child, grammar, run_sentence_extraction=False))

    if run_sentence_extraction:
        sentences = grammar.parse_ftml_to_sentences(ftml)
        if sentences:
            children.append(DocText(sentences))   # TODO: we lose the order here...

    return DocGroup(children)


def forthel_to_doc(
        forthel_source: str,
        grammar: MagmaGrammar,
) -> DocNode:
    paragraphs: list[DocNode] = []
    current_node: DocNode | None = None

    def push_paragraph(node: DocNode):
        nonlocal current_node
        paragraphs.append(node)
        current_node = node

    def analyse_header(line: str) -> tuple[str, str]:
        m = re.match(r'(?P<type>\w+)(\s+\((?P<label>[^)]*)\))?[.:]', line)
        if m is None:
            raise ValueError(f'Failed to parse {line}')
        return m.group('type'), m.group('label') or ''

    for line in forthel_source.splitlines():
        line = line.rstrip()
        if not line:
            continue
        if line[0].isspace():  # continue current node
            assert current_node is not None
            line = line.strip()
            # forthel pre-processing
            line = line.replace(',', ' , ')
            line = line.replace('(', ' ( ')
            line = line.replace(')', ' ) ')
            line += ' .'
            line = re.sub(r'\s+', ' ', line)
            sentence = Sentence([
                gf_xml_to_mast(gfxml.build_tree([], ast_str))
                for ast_str in
                grammar.parse_to_aststr(line, category='Sentence', preprocess=True)
            ])

            if current_node.children and isinstance(current_node.children[0], DocText):
                dt = current_node.children[0]
                assert isinstance(dt, DocText)
                dt.sentences.append(sentence)
            else:
                current_node.children.append(DocText([sentence]))

        else:       # new paragraph
            type_, label = analyse_header(line)
            if type_.lower() == 'definition':
                push_paragraph(Definition([], label=label))
            elif type_.lower() == 'axiom':
                push_paragraph(Statement([], type_='axiom', label=label))
            elif type_.lower() == 'theorem':
                push_paragraph(Statement([], type_='theorem', label=label))
            elif type_.lower() == 'proof':  # could check of proof follows theorem etc.
                push_paragraph(Proof([], label=label))
            elif type_.lower() == 'qed':
                pass

    return DocNode(paragraphs)




