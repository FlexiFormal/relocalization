"""
The flexi workbench

Supports a simple interface for documenting the transformation process.

It is not at all thread-safe and only a single workbench can be open at a time.
"""
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from flexi.parsing import gfxml
from flexi.parsing.magma import MagmaGrammar
from flexi.parsing.mast import MAst
from flexi.treevis import dot_to_svg, gfxml_tree_to_dot, mast_to_dot


class S:
    """ global state """
    workbench: Optional[str] = None
    suppress: bool = False
    default_grammar: Optional[MagmaGrammar] = None

@contextmanager
def new_workbench(path: Path, title: str = 'Flexi Workbench'):
    with open(path, 'w') as f:
        with new_workbench_actual(f, title):
            yield


@contextmanager
def new_workbench_actual(file, title: str = 'Flexi Workbench'):
    assert S.workbench is None, 'Another workbench is already open'
    S.workbench = ''
    S.suppress = False
    S.workbench += f'''<html>
    <head>
        <title>{title}</title>
        <style>
            details {{ margin-left: 1em; border: 1px solid #ccc; padding: 0.5em; }}
            summary {{ cursor: pointer; font-weight: bold; }}
            pre {{ white-space: pre-wrap; background-color: #f0f0f0; padding: 0.5em; }}
            /* svg {{ transform: scale(0.5); display: block; margin: 0 auto; }} */
        </style>
    </head>
    <body>'''
    try:
        yield
    finally:
        S.workbench += '</body></html>'
        file.write(S.workbench)
        S.workbench = None

def set_default_grammar(grammar: MagmaGrammar):
    S.default_grammar = grammar

def push_html(html: str):
    if S.suppress:
        return
    assert S.workbench is not None, 'No document open'
    S.workbench += html

def push_sentence_mast(tree: MAst):
    assert S.default_grammar is not None, 'No default shell set'
    # push_html(linearize_tree(tree, S.default_grammar))
    push_html(f'<div>{S.default_grammar.linearize_mast(tree)}</div>')
    push_mast(tree)

def push_mast(tree: MAst):
    with details('MAst'):
        push_html('<pre>' + repr(tree) + '</pre>')
        push_html('<div>')
        # print('>>>', tree)
        push_html(dot_to_svg(mast_to_dot(tree)))
        push_html('</div>')

def push_gfxml_tree(tree: gfxml.GfXmlNode):
    with details('Tree'):
        push_html('<pre>' + repr(tree) + '</pre>')
        push_html('<div>')
        # print('>>>', tree)
        push_html(dot_to_svg(gfxml_tree_to_dot(tree, no_attrs=True)))
        push_html('</div>')

@contextmanager
def details(summary: str):
    push_html(f'<details><summary>{summary}</summary>')
    try:
        yield
    finally:
        push_html('</details>')

@contextmanager
def suppress_tracking():
    """
    Disable the workbench (e.g. to suppress entries created by some library functions).
    """
    previous_value = S.suppress
    S.suppress = True
    try:
        yield
    finally:
        S.suppress = previous_value
