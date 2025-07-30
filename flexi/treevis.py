import subprocess

from flexi.parsing import gfxml, mast
from flexi.parsing.mast import MAst


def mast_to_dot(node: MAst) -> str:
    result = []

    def l(s: str) -> None:
        result.append(s)

    l('digraph G {')

    def traverse(n: MAst) -> None:
        extra = ''
        if hasattr(n, ':color'):
            style = getattr(n, ':style') if hasattr(n, ':style') else 'filled'
            fillcolor = getattr(n, ":color")
            if style == 'radial':
                fillcolor = f'white:{fillcolor}'
            elif style == 'mystriped':
                fillcolor = f'{fillcolor}:white:{fillcolor}'
                style = 'filled'
            extra = f', fillcolor="{fillcolor}", style={style}'

        display_val = n.value or ''
        if len(display_val) > 20:
            display_val = '...' + display_val[-17:]

        shape = 'plaintext'
        if isinstance(n, mast.G):
            shape = 'ellipse'
        elif isinstance(n, mast.S):
            shape = 'doubleoctagon'
        elif isinstance(n, mast.X):
            shape = 'diamond'
        elif isinstance(n, mast.M):
            shape = 'octagon'
        elif isinstance(n, mast.Formula):
            shape = 'triangle'
        elif isinstance(n, mast.MI):
            shape = 'diamond'
        elif isinstance(n, mast.MT):
            shape = 'plain'
        elif isinstance(n, mast.MSeq):
            shape = 'star'
            display_val = ''
        else:
            display_val = f'{type(n).__name__}({display_val})'

        l(f'  n{id(n)} [label="{display_val}", shape={shape}{extra}]')
        for c in n._children:
            traverse(c)
            l(f'  n{id(n)} -> n{id(c)}')

    traverse(node)

    l('}')
    return '\n'.join(result)

def gfxml_tree_to_dot(g: gfxml.GfXmlNode, no_attrs: bool = False) -> str:
    result = []

    def l(s: str) -> None:
        result.append(s)

    l('digraph G {')

    def traverse(n: gfxml.GfXmlNode) -> None:
        extra = ''
        if hasattr(n, ':color'):
            style = getattr(n, ':style') if hasattr(n, ':style') else 'filled'
            fillcolor = getattr(n, ":color")
            if style == 'radial':
                fillcolor = f'white:{fillcolor}'
            elif style == 'mystriped':
                fillcolor = f'{fillcolor}:white:{fillcolor}'
                style = 'filled'
            extra = f', fillcolor="{fillcolor}", style={style}'
        if isinstance(n, gfxml.XmlNode):
            if n.tag.startswith('?'):
                l(f'  n{id(n)} [label="<{n.tag}>", shape=diamond, fillcolor="lightgreen", style=filled]')
            elif no_attrs:
                l(f'  n{id(n)} [label="<{n.tag + (' ...' if n.attrs else '')}>", shape=box{extra}]')
            else:
                l(f'  n{id(n)} [label="<{n.tag} ' + ' '.join(f'{k}=\\"{v}\\"' for k, v in n.attrs.items()) + f'>", shape=box{extra}]')
            for c in n.children:
                traverse(c)
                l(f'  n{id(n)} -> n{id(c)}')
        elif isinstance(n, gfxml.XmlText):
            l(f'  n{id(n)} [label="{n.text}", shape=parallelogram{extra}]')
        elif isinstance(n, gfxml.GfNode):
            if n.node.startswith('Δ'):
                l(f'  n{id(n)} [label="{n.node[1:]}", shape=triangle{extra}]')
            else:
                l(f'  n{id(n)} [label="{n.node}", shape=ellipse{extra}]')
            for c in n.children:
                traverse(c)
                l(f'  n{id(n)} -> n{id(c)}')
        else:
            raise ValueError(f'Unexpected node type: {type(n)}')

    traverse(g)

    l('}')
    return '\n'.join(result)


def tree_to_qtree(g: gfxml.GfXmlNode) -> str:
    result = []

    def l(s: str) -> None:
        result.append(s)

    def get_label(n: gfxml.GfXmlNode) -> str:
        if isinstance(n, gfxml.XmlNode):
            return r'\textless' +  n.tag.replace('_', r'\_') + r'\textgreater'
        elif isinstance(n, gfxml.XmlText):
            return n.text.replace('_', r'\_')
        elif isinstance(n, gfxml.GfNode):
            return n.node.replace('_', r'\_')
        else:
            raise ValueError(f'Unexpected node type: {type(n)}')

    def traverse(n: gfxml.GfXmlNode) -> None:
        if isinstance(n, gfxml.XmlNode) or isinstance(n, gfxml.GfNode):
            if n.children:
                l(f'[ .{{ \\astnode{{ {get_label(n)} }} }}')
            else:
                l(f'{{ \\astnode{{ {get_label(n)} }} }}')
            for c in n.children:
                traverse(c)
            if n.children:
                l(']')
        elif isinstance(n, gfxml.XmlText):
            l(f'{{ \\astnode{{ {get_label(n)} }} }}')
        else:
            raise ValueError(f'Unexpected node type: {type(n)}')

    l(r'\Tree')
    traverse(g)
    l(r';')
    return ' '.join(result)


def dot_to_svg(dot: str) -> str:
    result = subprocess.run(['dot', '-Tsvg'], input=dot, text=True, capture_output=True)
    if result.returncode != 0:
        with open('/tmp/out.dot', 'w') as f:
            f.write(dot)
        raise ValueError(f'Error running dot (/tmp/out.dot): {result.stderr}')
    return result.stdout
