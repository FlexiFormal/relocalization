"""
High-level abstraction for working with MaGMA grammars
"""
import functools
import re
import subprocess
import logging
from pathlib import Path

from lxml import etree
from six import StringIO

from flexi.parsing import gfxml
from flexi.parsing.gf_ast import GfAst
from flexi.parsing.gf_shell import GFShellRaw
from flexi.parsing.mast import MAst, gf_xml_to_mast, mast_to_gfxml

logger = logging.getLogger(__name__)

MAGMA_PATH = (Path(__file__).parent.parent.parent / 'magma').absolute()


class ParseError(Exception):
    pass


class Sentence(list[MAst]):
    """ A sentence is a list of its possible readings """


class MagmaGrammar:
    def __init__(self, name: str, lang: str = 'Eng'):
        self.name = name

        # TODO: ideally, we want to only use PGF, but I can't find the sources/a documentation
        # some things don't work for me (e.g. specifying the start category for parsing)
        # Furthermore, there seem to be installation issues for some systems
        # So we use the GF shell for now...

        # self.pgf = get_pgf(name)
        # self.concrete = self.pgf.languages[f'{name}{lang}']
        self.shell = get_shell(name, lang)

    @property
    def pgf(self):
        return get_pgf(self.name)

    def get_fun_type(self, fun: str) -> str:
        return self.pgf.functionType(fun).cat

    def parse_to_aststr(self, sentence: str, category: str = 'Sentence',
                        preprocess: bool = True) -> list[str]:
        # a few quick pre-processing hacks
        string = sentence
        if preprocess and category == 'Sentence':
            # lower-case first letter
            first_letter = re.search(r'[a-zA-Z]', string)
            if first_letter:
                string = string[:first_letter.start()] + string[first_letter.start()].lower() + string[first_letter.start()+1:]

            # put space before last period
            string = re.sub(r'\.([0-9m<>/]*)', r' . \1', string)

        cmd = f'p -cat={category} "{string}"'
        shell_output = self.shell.handle_command(cmd)
        if shell_output.startswith('The parser failed at token') or \
                shell_output.startswith('The sentence is not compelte'):
            self.parser_error = shell_output
            raise ParseError(f'Parser error for "{string}": {shell_output}')
        return [s.strip() for s in shell_output.split('\n') if s.strip()]

    def parse_to_gfast(self, sentence: str, category: str = 'Sentence') -> list[GfAst]:
        return [GfAst.from_str(line) for line in self.parse_to_aststr(sentence, category)]

    def parse_ftml_to_sentences(
            self,
            ftml: etree._Element | Path,
            fail_on_parse_error: bool = True,
    ) -> list[Sentence]:
        if isinstance(ftml, Path):
            ftml = etree.parse(StringIO(ftml.read_text()), parser=etree.HTMLParser()).getroot()
        recovery_info, string = gfxml.get_gfxml_string(ftml)
        sentences = gfxml.sentence_tokenize(string)
        result: list[Sentence] = []
        for s in sentences:
            result.append(Sentence())
            try:
                asts = self.parse_to_aststr(s)
            except ParseError as e:
                if fail_on_parse_error:
                    raise e
                logger.warning(f'Parse error for {s!r}: {e}')
                continue

            for ast in asts:
                tree = gfxml.build_tree(recovery_info, ast)
                # print(tree)
                try:
                    trees = gfxml.parse_mtext_contents(
                        lambda s: self.parse_to_aststr(s, category='Stmt'),
                        tree
                    )
                except ParseError as e:
                    if fail_on_parse_error:
                        raise e
                    logger.warning(f'Parse error for mtext in {s!r}: {e}')
                    continue

                for t in trees:
                    result[-1].append(gf_xml_to_mast(t))

        return result

    def linearize_ast_str(self, ast: str, postprocess: bool = True) -> str:
        """
        Linearize a GF AST string to a sentence.
        """
        shell_output = self.shell.handle_command(f'linearize {ast}').strip()
        if postprocess:
            if shell_output and shell_output[0].isalpha():
                shell_output = shell_output[0].upper() + shell_output[1:]
            if shell_output.endswith(' .'):
                shell_output = shell_output[:-2] + '.'

        return shell_output.strip()

    def linearize_mast(self, ast: MAst, postprocess: bool = True) -> str:
        """
        Linearize a MAGMA AST to a sentence.
        """
        gfxml_tree = mast_to_gfxml(ast)
        # print('GFXMLTree', gfxml_tree)
        gfxml.linearize_mtree_contents(lambda s: self.shell.handle_command(f'linearize {s}'), gfxml_tree)
        recovery_info, ast_str = gfxml_tree.to_gf()
        gf_lin = self.linearize_ast_str(ast_str)
        return gfxml.final_recovery(gf_lin, recovery_info)


@functools.cache
def get_shell(name: str, lang: str = 'Eng') -> GFShellRaw:
    shell = GFShellRaw()
    result = shell.handle_command('import ' + str(MAGMA_PATH / 'combinations' / f'{name}{lang}.gf'))
    assert not result, f'GF import failed: {result}'
    return shell

@functools.cache
def get_pgf(name: str):
    import pgf  # type: ignore

    pgf_dir = MAGMA_PATH / 'pgf'
    pgf_dir.mkdir(parents=True, exist_ok=True)
    pgf_file = pgf_dir / f'{name}.pgf'

    if not pgf_file.exists() or any(
            pgf_file.stat().st_mtime < gf_file.stat().st_mtime
            for gf_file in MAGMA_PATH.rglob('*.gf')
    ):
        logger.info('(Re)compiling PGF for %s', name)
        concretes = [
            str(path.absolute())
            for path in (MAGMA_PATH / 'combinations').glob(f'{name}*.gf')
            if not path.name == f'{name}.gf'
        ]
        if not concretes:
            raise RuntimeError(f'No GF files found for {name}')
        result = subprocess.run(['gf', '--make'] + concretes, cwd=pgf_dir)
        if result.returncode:
            raise RuntimeError('GF compilation failed')

    return pgf.readPGF(str(pgf_file))   # type: ignore
