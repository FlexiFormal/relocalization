"""
Lexicon parsing

This whole implementation is just a test to see if the interface is correct.
In the long term, once the interface has converged, it should be implemented with a clean parser.
"""

import dataclasses
import re
from collections import defaultdict
from typing import Literal

from flexi.config import TEST_FILE_DIR
from flexi.parsing.magma import MAGMA_PATH


class AbstractSyntax:
    def __init__(self, funs: list[str] | None = None):
        self.funs = funs or []


class ConcreteSyntax:
    def __init__(self, lins: list[str] | None = None, opers: list[str] | None = None):
        self.lins = lins or []
        self.opers = opers or []


@dataclasses.dataclass
class VerbalizationRecord:
    argument_order: tuple[int, ...]
    main_argument: int | None
    symbol: str
    fun_name: str
    typ: str


class VerbalizationManager:
    def __init__(self, records: list[VerbalizationRecord] | None = None):
        self.records: list[VerbalizationRecord] = []

        # lookup structures
        self.verbs_by_symb: dict[str, list[VerbalizationRecord]] = defaultdict(list)

        for r in records or []:
            self.add_verb_record(r)

    def add_verb_record(self, record: VerbalizationRecord):
        self.records.append(record)
        self.verbs_by_symb[record.symbol].append(record)


@dataclasses.dataclass
class NotationRecord:
    symbol: str
    fun: str
    arity: int
    is_predicate: bool



class NotationManager:
    """ TODO: Merge this with Verbalization Manager? """
    def __init__(self, notations: list[NotationRecord] | None = None):
        self.records: list[NotationRecord] = []
        self.notations_by_symb: dict[str, list[NotationRecord]] = defaultdict(list)
        for r in notations or []:
            self.add_notation_record(r)

    def add_notation_record(self, record: NotationRecord):
        self.records.append(record)
        self.notations_by_symb[record.symbol].append(record)



class Lexicon:
    def __init__(self, name: str, mode: Literal['forthel', 'ftml']):
        self.abstract_syntax = AbstractSyntax()
        self.concrete_syntax = ConcreteSyntax()
        self.verbalization_manager = VerbalizationManager()
        self.notation_manager = NotationManager()
        self.mode = mode
        self.name = name

        self.word_id_prefix = '_dict_'
        self.covered_word_ids: set[str] = set()

    def add_identifier(self, line: str):
        i = line.strip()
        self.abstract_syntax.funs.append(f'{i} : ForthelPlainIdentifier;')
        self.concrete_syntax.lins.append(f'{i} = "{i}";')

    def add_notation(self, line: str, is_predicate: bool):
        parts = line.split()
        if len(parts) < 3:
            raise ValueError(f'Line {line} is malformed')

        symbol = parts[0]
        if parts[1] != '=':
            raise ValueError(f'Line {line} is malformed')

        fun = symbol + '__notation' + str(len(self.notation_manager.notations_by_symb[symbol]))

        arg_count = 0
        tokens = []
        for part in parts[2:]:
            if part.startswith('#'):
                n = int(part[1:])
                arg_count = max(arg_count, n)
                tokens.append(f'a{n}')
            else:
                tokens.append(f'"{part}"')

        self.abstract_syntax.funs.append(
            f'{fun} : ' + ' -> '.join(['ForthelTerm'] * arg_count + ['ForthelStmt' if is_predicate else 'ForthelTerm']) + ';'
        )
        self.concrete_syntax.lins.append(
            f'{fun} ' + ' '.join([f'a{n}' for n in range(1, arg_count + 1)]) + ' = ' + ' ++ '.join(tokens) +  ';'
        )
        self.notation_manager.add_notation_record(
            NotationRecord(
                symbol=symbol,
                fun=fun,
                arity=arg_count,
                is_predicate=is_predicate,
            )
        )


    def add_word(self, line: str):
        match = re.match(
            r'(?P<id>(?P<word>\w+)_(?P<cat>[a-zA-Z]+))(\s*=\s*(?P<def>.*))?',
            line.strip(),
        )
        if not match:
            raise ValueError(f'Invalid line in lexicon: {line}')
        word = match.group('word')
        cat = match.group('cat')
        def_ = f'mk{cat} ' + (match.group('def') or f'"{word}"')
        id_ = self.word_id_prefix + match.group('id')
        self.concrete_syntax.opers.append(f'{id_} = {def_};')
        self.covered_word_ids.add(id_)

    @classmethod
    def tokenize(cls, line: str) -> list[str]:
        """ at this point just slightly smarter than str.split """
        l = line.split()
        r = []
        for e in l:
            if r and r[-1].startswith('"') and not (len(r[-1]) > 1 and r[-1][-1] == '"'):
                r[-1] += e
            else:
                r.append(e)
        return r

    def add_term(self, line: str):
        """
        This is just quick-and-dirty implementation with insufficient validation etc.
        """
        parts = self.tokenize(line)
        if len(parts) < 4:
            raise ValueError(f'Invalid line in lexicon: {line}')

        typ = parts[0]

        symbol = parts[1]
        if parts[2] != '=':
            raise ValueError(f'Invalid line in lexicon: {line}')

        _num = str(len(self.verbalization_manager.verbs_by_symb[symbol]))
        if symbol.startswith('"'):
            symbol = symbol.strip('"')
            fun = "'" + symbol + '__verb' + _num + "'"
        else:
            fun = symbol + '__verb' + _num

        self.abstract_syntax.funs.append(f'{fun} : {typ};')

        if parts[3].startswith('#'):
            main_arg = int(parts[3][1:])
            start = 4
        else:
            main_arg = None
            start = 3

        arg_order: list[int] = []

        mainword_components: list[str] = []
        preps = []

        for part in parts[start:]:
            if ':' in part:   # arg
                prep, arg = part.split(':')
                arg_order.append(int(arg[1:]))
                preps.append(prep + '_Prep')
            else:
                if part in {'(', ')'} or part.startswith('&'):
                    if part.startswith('&'):
                        part = part[1:]
                    mainword_components.append(part)
                else:  # it's a word
                    id_ = self.word_id_prefix + part
                    if id_ not in self.covered_word_ids:
                        self.add_word(part)
                    mainword_components.append(id_)

        mainword_constructor = {
            'Kind': 'makeCN', 'Kind1': 'makeCN', 'Kind2': 'makeCN', 'Kind3': 'makeCN',
            'FKind': 'makeCN', 'FKind2': 'makeCN',
            'Property': 'mkAP', 'Property2': 'mkAP',
            'Predicate': 'mkVP', 'Predicate2': 'mkVP', 'Predicate3': 'mkVP'
        }
        if typ not in mainword_constructor:
            raise ValueError(f'Invalid type {typ!r} in lexicon: {line}')
        self.concrete_syntax.lins.append(f'{fun} = mk{typ} ({mainword_constructor[typ]} {" ".join(mainword_components)}) {" ".join(preps)};')
        self.verbalization_manager.add_verb_record(
            VerbalizationRecord(
                argument_order=tuple(arg_order),
                main_argument=main_arg,
                symbol=symbol,
                fun_name=fun,
                typ=typ,
            )
        )

    def write(self):
        path = MAGMA_PATH / 'generated'
        path.mkdir(exist_ok=True)

        with open(path / f'{self.name}Grammar.gf', 'w') as fp:
            if self.mode == 'forthel':
                fp.write('--# -path=../magma:../lexica:../other\n\n')
                fp.write(f'abstract {self.name}Grammar = Forthel ** {{\n')
            elif self.mode == 'ftml':
                fp.write('--# -path=../magma:../lexica:../other:../formulae\n\n')
                fp.write(f'abstract {self.name}Grammar = SigFtml ** {{\n')
            else:
                raise NotImplementedError(f'Unknown mode {self.mode!r}')
            fp.write('  fun\n')
            for fun in self.abstract_syntax.funs:
                fp.write(f'    {fun}\n')
            fp.write('}\n')

        with open(path / f'{self.name}GrammarEng.gf', 'w') as fp:
            if self.mode == 'forthel':
                fp.write('--# -path=../magma:../lexica:../other\n\n')
                fp.write(f'concrete {self.name}GrammarEng of {self.name}Grammar = ForthelEng ** open SigConstructorsEng, ParadigmsEng, ConstructorsEng in {{\n')
            elif self.mode == 'ftml':
                fp.write('--# -path=../magma:../lexica:../other:../formulae\n\n')
                fp.write(f'concrete {self.name}GrammarEng of {self.name}Grammar = SigFtmlEng ** open SigConstructorsEng, ParadigmsEng, ConstructorsEng in {{\n')
            else:
                raise NotImplementedError(f'Unknown mode {self.mode!r}')
            fp.write('  oper\n')
            for oper in self.concrete_syntax.opers:
                fp.write(f'    {oper}\n')
            fp.write('\n  lin\n')
            for lin in self.concrete_syntax.lins:
                fp.write(f'    {lin}\n')
            fp.write('}\n')


def augment_lexicon(
        lexicon_source: str,
        lexicon: Lexicon,
) -> Lexicon:
    mode: str = ''

    for line in lexicon_source.splitlines():
        line = line.strip()
        if not line:
            continue
        elif line.startswith('#'):  # comment
            continue
        elif line.startswith('@'):
            mode = line[1:].lower()
            if mode not in {'words', 'terms', 'notations:predicates', 'notations:functions', 'notations:identifiers'}:
                raise ValueError(f'Invalid syntax mode in lexicon: {line}')
            continue
        elif not mode:
            raise ValueError(f'Unexpected line: {line}')
        elif mode == 'words':
            lexicon.add_word(line)
        elif mode == 'terms':
            lexicon.add_term(line)
        elif mode == 'notations:predicates':
            lexicon.add_notation(line, is_predicate=True)
        elif mode == 'notations:functions':
            lexicon.add_notation(line, is_predicate=False)
        elif mode == 'notations:identifiers':
            lexicon.add_identifier(line)
        else:
            raise RuntimeError()

    return lexicon


if __name__ == '__main__':
    augment_lexicon(
        # Path('/tmp/test.txt').read_text(),
        (TEST_FILE_DIR / 'naproche' / 'cantor.lexicon').read_text(),
        Lexicon('cantor', 'forthel'),
    ).write()
