"""
This module provides code process HTML with GF.
The basic pipeline is as follows:
1. parse HTML
2. Create plaintex representation that contains references to the original HTML tags
3. Tokenize into sentences
4. Parse these sentences with GF
5. Post-process the resulting ASTs so that they contain the data of the original HTML tags again

These ASTs can be manipulated and later turned back into HTML.

The whole code was a quick hack that grew organically and is barely comprehensible by now.
It has to be re-implemented cleanly at some point, but, unfortunately, this is
neither easy nor a priority right now.


A (German -- sorry) description of what happens with an example:

Wenn wir das Dokument
<html><body>Hello word. Look at <emph>this</emph>: <math>...</math></body></html>
verarbeiten wollen, wird es zunächst mit einem HTML parser geparst.
Aus dem HTML-Baum, wird nun ein neuer, xml-artiger String erstellt, bei dem alle Tags durch Zahlen ersetzt wurden:
<0><1>Hello word. Look at <2>this</2>: $ 3 $</1></0>
Außerdem wird ein String erstellt, der keine Tags hat, aber bei dem noch gespeichert wurde, welche Zeichen woher kamen:
Hello word. Look at this: X
Darauf können wir dann einen Standard sentence tokenizer laufen lassen.
Letztlich kriegen wir dann eine Liste von Sätzen:
["Hello word.", "Look at <2>this</2>: $ 3 $"]
Diese Sätze können nun von GF peparst werden.
Die ASTs werden dann nochmal nachverarbeitet, sodass die Zahlen wieder durch die ursprünglichen Tags ersetzt werden.
Damit haben wir dann eine Mischform aus XML/HTML-Knoten und GF-Knoten als Baumstruktur, auf der wir arbeiten können und Ersetzungen machen können.
Um die Ergebnisse wieder als HTML zu haben, geht das ganze auch rückwärts.
"""
import functools
from io import StringIO
from pathlib import Path
from typing import Callable, Optional
import re

from nltk import PunktSentenceTokenizer  # type: ignore
import nltk
from copy import deepcopy

from lxml import etree


@functools.cache
def require_nltk_punkt():
    try:
        PunktSentenceTokenizer()
    except LookupError:
        import sys
        nltk.download('punkt')
        print('Downloaded NLTK punkt tokenizer data. Please restart the program to use it.', file=sys.stderr)
        sys.exit(1)

class GfXmlNode:
    def to_gf(self) -> tuple[list[tuple[str, str]], str]:
        _tags: list[tuple[str, str]] = []
        return _tags, self._to_gf(_tags)

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        raise NotImplementedError()


class XmlNode(GfXmlNode):
    __match_args__ = ('tag', 'children', 'attrs', 'wrapfun')

    def __init__(self, tag: str, children: list[GfXmlNode], attrs: Optional[dict[str, str]] = None,
                 wrapfun: Optional[str] = None):
        self.tag = tag
        self.children = children
        self.attrs = attrs or {}
        self.wrapfun = wrapfun

    def pure_node_strings(self) -> tuple[str, str]:
        a, b = f'<{self.tag} ' + ' '.join(f'{k}="{v}"' for k, v in self.attrs.items()) + '>', f'</{self.tag}>'
        for child in self.children:
            assert isinstance(child, XmlNode) or isinstance(child, XmlText)
            da, db = child.pure_node_strings()
            a += da + db
            # was:
            #   a += da
            #   b = db + b
        return a, b

    def __repr__(self):
        return f'X({self.tag!r}, {self.children!r}, {self.attrs!r}, {self.wrapfun!r})'

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        tag_num = len(_tags)
        # if self.wrapfun is None:
        if self.tag == 'math':
            _tags.append(self.pure_node_strings())
            return f'(dollarmath "{tag_num}")'
        else:
            _tags.append(
                (f'<{self.tag} ' + ' '.join(f'{k}="{v}"' for k, v in self.attrs.items()) + '>', f'</{self.tag}>'))
            return f'({self.wrapfun} (tag {tag_num}) {" ".join(child._to_gf(_tags) for child in self.children)})'


class XmlText(GfXmlNode):
    __match_args__ = ('text',)

    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f'XT({self.text!r})'

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        raise RuntimeError('XT nodes should only be in pure X nodes and never passed to GF')

    def pure_x_node(self) -> bool:
        return True

    def pure_node_strings(self) -> tuple[str, str]:
        return self.text, ''  # TODO: escaping (except if it's the content of an mtext tag that was created using our hacks for recursive linearization)


class GfNode(GfXmlNode):
    __match_args__ = ('node', 'children')

    def __init__(self, node: str, children: list[GfXmlNode] = []):
        if node == '':
            raise ValueError('Node name cannot be empty')
        self.node = node
        self.children = children

    def __repr__(self):
        return f'G({self.node!r}, {self.children!r})'

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        return f'({self.node} {" ".join(child._to_gf(_tags) for child in self.children)})'


SHTML_NS = 'http://example.org/shtml'
MMT_NS = 'http://example.org/mmt'


def parse_shtml(path: Path) -> etree._ElementTree:
    with open(path, 'r', encoding="utf-8") as f:
        # Hack: supply missing namespace declarations
        return etree.parse(
            StringIO(
                f.read().replace(
                    '<html xmlns="http://www.w3.org/1999/xhtml">',
                    f'<html xmlns:shtml="{SHTML_NS}" xmlns:mmt="{MMT_NS}">')
            )
        )


def xify(node: etree._Element | str) -> XmlNode:
    assert not isinstance(node, etree._Comment)
    if isinstance(node, str):
        node = etree.parse(StringIO(node)).getroot()
    x = XmlNode(
        tag=node.tag,
        children=[],
        attrs=node.attrib  # type: ignore
    )
    if node.text and node.text.strip():
        x.children.append(XmlText(node.text))
    for child in node:
        if isinstance(child, etree._Comment):
            continue
        x.children.append(xify(child))
        if child.tail and child.tail.strip():
            x.children.append(XmlText(child.tail))
    return x


def get_gfxml_string(shtml: etree._Element) -> tuple[list[XmlNode], str]:
    strings: list[str] = []

    nodes: list[XmlNode] = []

    def _recurse(node: etree._Element):
        if isinstance(node, etree._Comment):
            return
        if node.attrib.get('data-ftml-invisible', '') == 'true':
            if node.tail:
                strings.append(node.tail)
            return

        tag_num = len(nodes)
        if node.tag.endswith('math'):
            # don't recurse into math nodes - place them as-is
            nodes.append(xify(node))
            strings.append(f'$ {tag_num} $')
            if node.tail:
                strings.append(node.tail)
            return

        nodes.append(XmlNode(
            tag=node.tag,
            children=[],
            attrs=node.attrib  # type: ignore
        ))
        strings.append(f'< {tag_num} >')
        if node.text:
            strings.append(node.text)
        for child in node:
            _recurse(child)

        strings.append(f'</ {tag_num} >')
        if node.tail:
            strings.append(node.tail)

    if isinstance(shtml, etree._Element) and shtml.tag == 'html':
        bodies = [child for child in shtml if child.tag == 'body']
        assert len(bodies) == 1, 'Expected exactly one <body> tag in the HTML document'
        shtml = bodies[0]
    _recurse(shtml)

    return nodes, ''.join(strings)


def sentence_tokenize(text: str) -> list[str]:
    # simplify whitespace
    text = re.sub(r'\s+', ' ', text)

    # we will remove all tags, but remember them to reinsert them later
    tags: list[list[str]] = [[]]  # tags[i] is the list of tags that are should be reinserted at position i
    # open_tags = [[]]   # open_tags[i] is the list of tags that are open at position i
    # close_tags = [[]]
    without_tags = ''

    i = 0
    while i < len(text):
        if text[i] == '<':
            j = i
            while text[j] != '>':
                j += 1
            tags[-1].append(text[i:j + 1])
            i = j
        else:
            tags.append([])
            without_tags += text[i]
            assert len(tags) == len(without_tags) + 1
        i += 1

    require_nltk_punkt()
    tokenizer = PunktSentenceTokenizer()
    sentences: list[str] = []
    for start, end in tokenizer.span_tokenize(without_tags):
        sentence = ''
        for i in range(start, end):
            for tag in tags[i]:
                sentence += tag
            sentence += without_tags[i]

        # remove unmatched tags at the beginning and end of the sentence

        open_tags = [int(match.group('i')) for match in re.finditer(r'< (?P<i>\d+) >', sentence)]
        close_tags = [int(match.group('i')) for match in re.finditer(r'</ (?P<i>\d+) >', sentence)]

        for itag in open_tags:
            if itag not in close_tags and sentence.endswith(f'</ {itag} >'):
                sentence = sentence[:-len(f'</ {itag} >')]
        for itag in close_tags:
            if itag not in open_tags and sentence.startswith(f'< {itag} >'):
                sentence = sentence[len(f'< {itag} >'):]

        # add missing tags at the beginning and end (e.g. "This </ 3 > is a sentence" -> "< 3 > This </ 3 > is a sentence")
        open_tags = [int(match.group('i')) for match in re.finditer(r'< (?P<i>\d+) >', sentence)]
        close_tags = [int(match.group('i')) for match in re.finditer(r'</ (?P<i>\d+) >', sentence)]

        for itag in close_tags:
            if itag not in open_tags:
                sentence = f'< {itag} >' + sentence
        for itag in reversed(open_tags):
            if itag not in close_tags:
                sentence = sentence + f'</ {itag} >'

        # strip away outer tags
        # e.g. < 0 > < 1 > </ 1 > Words </ 0 > -> Words
        while True:
            _just_tags = r'(\s+|</? [0-9]+ >)*'
            # _just_tags = r'\s*'
            m = (
                    # "< i > sentence </ i >"
                    re.match(r'^\s*(< (?P<i>[0-9]+) >)(?P<sentence>.*?)(</ (?P=i) >\s*)$', sentence)
                    # "< i > </ i > sentence"
                    # but also "< i > < j > </ j > < k > </ k > </ i > sentence" etc.
                    or re.match(r'^\s*(< (?P<i>[0-9]+) >)' + _just_tags + r'(</ (?P=i) >)\s*(?P<sentence>.*?)$', sentence)
                    # "sentence < i > </ i >" (and more nested)
                    or re.match(r'^(?P<sentence>.*?)\s*(< (?P<i>[0-9]+) >)' + _just_tags + r'(</ (?P=i) >)\s*$', sentence)
            )
            if m:
                sentence = m.group('sentence')
            else:
                break

        # post-processing
        sentence = sentence.replace('>', '> ')
        sentence = sentence.replace('<', ' <')

        sentences.append(sentence)

    return sentences


def build_tree(nodes: list[XmlNode], ast_str: str) -> GfXmlNode:
    i = 0

    def read_label() -> str:
        nonlocal i
        label = ''
        while i < len(ast_str) and (ast_str[i].isalnum() or ast_str[i] in {'_', '\'', '/', '?', ':', '#', '.', '-'}):
            label += ast_str[i]
            i += 1
        return label

    def expect_str(s: str):
        nonlocal i
        for j in range(len(s)):
            if i + j >= len(ast_str):
                raise ValueError(f'Expected {s!r}, got end of string')
            if ast_str[i + j] != s[j]:
                raise ValueError(f'Expected {s!r}, got {ast_str[i:i + j + 1]!r}')
        i += len(s)

    def read_tag() -> int:
        nonlocal i
        expect_str(' (tag ')
        number = int(read_label())
        expect_str(') ')
        return number

    def read_string_lit() -> str:
        nonlocal i
        expect_str(' "')
        string = ''
        while i < len(ast_str):
            if ast_str[i] == '"':
                i += 1
                break
            elif ast_str[i] == '\\':
                i += 1
                if i >= len(ast_str):
                    raise ValueError('Unexpected end of string in string literal')
                string += ast_str[i]
            else:
                string += ast_str[i]
            i += 1
        if i < len(ast_str) and ast_str[i] == ' ':
            i += 1
        return string

    def read_node() -> GfXmlNode:
        nonlocal i
        tag = read_label()
        if tag.lower().startswith('wrap'):
            node = deepcopy(nodes[read_tag()])
            node.wrapfun = tag
            node.children = [read_node()]
            return node
        elif tag == 'dollarmath':
            node = deepcopy(nodes[int(read_string_lit())])
            node.wrapfun = tag
            if i < len(ast_str):
                expect_str(')')
            return node
        else:
            children = []
            while i < len(ast_str):
                if ast_str[i] == ' ':
                    i += 1
                elif ast_str[i] == '(':
                    i += 1
                    new_node = read_node()
                    children.append(new_node)
                elif ast_str[i] == ')':
                    i += 1
                    break
                elif (ast_str[i].isalnum() or ast_str[i] in {'_', '\'', '/', '?', ':', '#', '.', '-'}):
                    children.append(GfNode(read_label()))
                else:
                    raise ValueError(f'Unexpected character in AST: {ast_str[i]!r}')

            if not tag:
                assert len(children) == 1
                return children[0]
            return GfNode(tag, children)

    node = read_node()

    if i != len(ast_str):
        raise ValueError('Unmatched opening parenthesis')

    return node


def final_recovery(string: str, recovery_info: list[tuple[str, str]]) -> str:
    for i, (open_tag, close_tag) in enumerate(recovery_info):
        if open_tag.startswith('<math'):
            string = string.replace(f'$ {i} $', open_tag + close_tag)
        else:
            string = string.replace(f'< {i} >', open_tag)
            string = string.replace(f'</ {i} >', close_tag)
    return string


def tree_eq(a: GfXmlNode, b: GfXmlNode) -> bool:
    match (a, b):
        case (XmlNode(t1, c1, _, f1), XmlNode(t2, c2, _, f2)):
            return t1 == t2 and f1 == f2 and len(c1) == len(c2) and all(tree_eq(aa, bb) for aa, bb in zip(c1, c2))
        case (GfNode(f1, c1), GfNode(f2, c2)):
            return f1 == f2 and len(c1) == len(c2) and all(tree_eq(aa, bb) for aa, bb in zip(c1, c2))
        case (XmlText(t1), XmlText(t2)):
            return t1 == t2
        case (str(_), str(_)):
            return a == b
        case _:
            return False


def tree_subst(t: GfXmlNode, a: GfXmlNode, b: GfXmlNode) -> GfXmlNode:
    """ replaces all occurrences of a in t with b (ignoring attributes) """
    if tree_eq(t, a):
        return deepcopy(b)
    t = deepcopy(t)
    if isinstance(t, GfNode) or isinstance(t, XmlNode):
        for i in range(len(t.children)):
            t.children[i] = tree_subst(t.children[i], a, b)
    return t


def get_outerNodes(t: GfXmlNode, subtree: GfXmlNode) -> list[GfXmlNode]:
    outer_nodes: list[GfXmlNode] = []
    if isinstance(t, GfNode) or isinstance(t, XmlNode):
        if subtree in t.children:
            outer_nodes.append(t)
        else:
            for child in t.children:
                outer_nodes.extend(get_outerNodes(child, subtree))
    return outer_nodes


def get_firstOuterNode(t: GfXmlNode, subtree: GfXmlNode) -> Optional[GfXmlNode]:
    outer_nodes = get_outerNodes(t, subtree)
    return outer_nodes[0] if outer_nodes else None


def tree_contains_node(t: GfXmlNode, n: GfXmlNode) -> bool:
    if tree_eq(t, n):
        return True
    if isinstance(t, GfNode) or isinstance(t, XmlNode):
        for child in t.children:
            if tree_contains_node(child, n):
                return True
    return False


def parse_mtext_contents(parse_fn: Callable[[str], list[str]], tree: GfXmlNode) -> list[GfXmlNode]:
    todo_list = [tree]
    final_result = []

    class FoundNodeException(Exception):
        def __init__(self, node: GfXmlNode):
            self.node = node

    def _recurse(n: GfXmlNode):
        if isinstance(n, GfNode):
            for child in n.children:
                _recurse(child)
        elif isinstance(n, XmlNode):
            if n.tag == 'mtext':
                if not hasattr(n, '::already_processed'):
                    raise FoundNodeException(n)
            for child in n.children:
                _recurse(child)
        else:
            assert isinstance(n, XmlText), f'Unexpected node type: {n}'

    while todo_list:
        root = todo_list.pop()
        try:
            _recurse(root)
            final_result.append(root)  # nothing left to do
        except FoundNodeException as e:
            setattr(e.node, '::already_processed', True)
            # create string, analogously to get_gfxml_string
            strings: list[str] = []
            nodes: list[XmlNode] = []

            def _recurse2(node: XmlNode):
                tag_num = len(nodes)
                nodes.append(node)

                if node.tag.endswith('math'):
                    strings.append(f'$ {tag_num} $')
                    return

                strings.append(f'< {tag_num} >')
                for child in node.children:
                    if isinstance(child, XmlText):
                        strings.append(child.text)
                    else:
                        assert isinstance(child, XmlNode)
                        _recurse2(child)
                strings.append(f'</ {tag_num} >')

            assert isinstance(e.node, XmlNode)
            for child in e.node.children:
                if isinstance(child, XmlText):
                    strings.append(child.text)
                else:
                    assert isinstance(child, XmlNode)
                    _recurse2(deepcopy(child))

            # integrate the parsed contents
            string = re.sub(r'\s+', ' ', ' '.join(strings)).strip()
            for gf_ast in parse_fn(string):
                tree = build_tree(nodes, gf_ast)
                e.node.children = [tree]
                todo_list.append(deepcopy(root))

    return final_result


def linearize_mtree_contents(linearize_fn: Callable[[str], str], tree: GfXmlNode):
    if isinstance(tree, XmlNode) and tree.tag == 'mtext': # and hasattr(tree, '::already_processed'):
        assert len(tree.children) == 1
        recovery_info, gf_input = tree.children[0].to_gf()
        gf_lin = linearize_fn(gf_input)
        result = final_recovery(gf_lin, recovery_info)
        tree.children = [XmlText(result)]  # TODO: XT content should not be escaped!
    elif isinstance(tree, GfNode) or isinstance(tree, XmlNode):
        for i in range(len(tree.children)):
            linearize_mtree_contents(linearize_fn, tree.children[i])
