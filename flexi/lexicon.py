import dataclasses
import itertools
import re
from pathlib import Path
from typing import Literal, Iterable

from lxml import etree
from lxml.etree import _Element

from flexi.parsing.magma import MAGMA_PATH


MAGMA_MAPPING: dict[str, tuple[str, str]] = {
    'N': ('makeCN', 'Kind'), 'N2': ('makeCN', 'Kind2'), 'N3': ('makeCN', 'Kind3'),
    'DefN': ('makeCN', 'FKind'), 'DefN2': ('makeCN', 'FKind2'),
    'A': ('mkAP', 'Property'), 'A2': ('mkAP', 'Property2'),
    'V': ('mkVP', 'Predicate'), 'V2': ('mkVP', 'Predicate2'), 'V3': ('mkVP', 'Predicate3'),
}


class BadSpec(Exception):
    pass


@dataclasses.dataclass(kw_only=True)
class VerbalizationRecord:
    spec_str: str
    argument_order: tuple[int, ...]  # excluding main argument
    subject_argument: int | None
    typ: str
    gf_id: str
    gf_lin: str
    depends_on_words: list[str]

    def to_json(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls, json: dict) -> VerbalizationRecord:
        record = cls(**json)
        if isinstance(record.argument_order, list):
            record.argument_order = tuple(record.argument_order)
        return record

    @classmethod
    def from_spec(cls, typ: str | None, spec_str: str, subject_argument: int | None) -> VerbalizationRecord:
        core_tokens: list[str] = []
        prepositions: list[str] = []
        argument_order: list[int] = []

        # STEP 1: Process spec_str
        # implemented a bit like a state machine.
        # states:
        #  * start: initial state
        #  * core: in the "main phrase"
        #  * arg: expecting arguments
        state: Literal['start', 'core', 'arg'] = 'start'
        spec = spec_str.split()
        if not spec:
            raise BadSpec()
        i = 0
        while i < len(spec):
            token = spec[i]
            next_token = spec[i+1] if i + 1 < len(spec) else None
            is_arg = bool(re.match(r'[#?]\d+', token))
            next_is_arg = bool(re.match(r'[#?]\d+', next_token)) if next_token is not None else False

            match state:
                case 'start':
                    if is_arg:
                        if subject_argument is not None:
                            raise BadSpec(f'Unexpected specification of subject argument')
                        subject_argument = int(token[1:])
                        i += 1
                    # else: no subject_argument -> continue in 'core' state
                    state = 'core'
                case 'core':
                    if is_arg:
                        raise BadSpec(f'Unexpected argument {token!r}')
                    if next_is_arg:  # this must be a preposition -> switch to arg state
                        state = 'arg'
                        continue
                    core_tokens.append(token)
                    i += 1
                case 'arg':
                    if is_arg:
                        raise BadSpec(f'Unexpected argument {token!r}')
                    if not next_is_arg:
                        raise BadSpec(
                            f'Expected argument, got {next_token!r}'
                            if next_token is not None else
                            f'Expected argument, but reached end of spec'
                        )
                    prepositions.append(token)
                    argument_order.append(int(next_token[1:]))
                    i += 2
                case _:
                    raise RuntimeError(f'Unexpected state "{state}"')

        # STEP 2: infer missing information
        if typ is None:
            if ':' not in core_tokens[-1]:
                raise BadSpec(f'Cannot infer verbalization type')
            # by default, we assume a subject argument
            argnum = str(len(argument_order) + 1) if argument_order else ''
            pos = core_tokens[-1].split(':')[-1]
            if pos in {'N', 'V', 'A'}:
                typ = pos + argnum
            else:
                raise BadSpec(f'Cannot infer verbalization type')

        if subject_argument is None and re.match(r'[NVA]\d*', typ):
            subject_argument = next(iter(x for x in itertools.count(1) if x not in argument_order))

        # STEP 3: generate compile into verbalization record
        if typ not in MAGMA_MAPPING:
            raise ValueError(f'Unexpected type "{typ}"')

        constr, magma_typ = MAGMA_MAPPING[typ]

        return VerbalizationRecord(
            spec_str=spec_str,
            argument_order=tuple(argument_order),
            subject_argument=subject_argument,
            typ=magma_typ,
            gf_id=f'verb_{"-".join(spec)}_{magma_typ}',
            gf_lin=f'mk{magma_typ} ({constr} {" ".join(f"'{ct}'" for ct in core_tokens)}) {" ".join(p + '_Prep' for p in prepositions)}',
            depends_on_words=core_tokens,
        )


@dataclasses.dataclass
class WordRecord:
    gf_id: str
    gf_def: str
    is_inferred: bool


@dataclasses.dataclass
class SymbolVerbRecord:
    symbol: str
    verb_id: str   # gf id

    name: str | None     # verbalization name
    distributivity: str | None

    def to_json(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls, json: dict) -> SymbolVerbRecord:
        return SymbolVerbRecord(**json)

    def get_verbalization(self, lexicon: Lexicon) -> VerbalizationRecord:
        return lexicon.verbalizations[self.verb_id]


class Lexicon:
    def __init__(self, name: str, lang: str):
        self.name = name
        self.lang = lang
        self.words: dict[str, WordRecord] = {}
        # verbalizations by gf id
        self.verbalizations: dict[str, VerbalizationRecord] = {}
        self.verb_to_symbol: dict[str, list[SymbolVerbRecord]] = {}
        self.symbol_to_verb: dict[str, list[SymbolVerbRecord]] = {}

    def iter_symb_verb_records(self) -> Iterable[SymbolVerbRecord]:
        for l in self.verb_to_symbol.values():
            yield from l

    def add_verbalization(self, vr: VerbalizationRecord):
        self.verbalizations[vr.gf_id] = vr
        for wd in vr.depends_on_words:
            if wd in self.words:
                continue
            # try to infer default entry
            if ':' not in wd:
                continue
            word, cat = wd.split(':', 1)
            if cat not in {'A', 'N', 'V'}:
                continue
            self.add_word(
                WordRecord(
                    gf_id = wd,
                    gf_def = f'mk{cat} "{word}"',
                    is_inferred = True,
                )
            )

    def add_symbol_verb(self, svr: SymbolVerbRecord):
        self.verb_to_symbol.setdefault(svr.verb_id, []).append(svr)
        self.symbol_to_verb.setdefault(svr.symbol, []).append(svr)

    def add_word(self, w: WordRecord):
        if w.gf_id in self.words:
            if not self.words[w.gf_id].is_inferred:   # it's ok to substitute inferred word records
                raise ValueError(f'Duplicate word "{w.gf_id}"')
        self.words[w.gf_id] = w

    def add_word_list(self, path: Path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                line = line.split('=', 1)
                if not len(line) == 2:
                    raise ValueError(f'Invalid word entry in {path}: "{line}"')
                self.add_word(
                    WordRecord(
                        gf_id = line[0].strip(),
                        gf_def = line[1].strip().rstrip(';'),
                        is_inferred = False,
                    )
                )

    def extend_from_ftml(self, ftml: _Element | Path):
        if isinstance(ftml, Path):
            ftml = etree.parse(str(ftml), parser=etree.HTMLParser(encoding='UTF-8')).getroot()
        assert isinstance(ftml, _Element)

        for node in ftml.iter(tag='div'):
            if 'data-ftml-verbalization-symbol' not in node.attrib:
                continue

            vr = VerbalizationRecord.from_spec(
                node.attrib['data-ftml-verbalization-type'] or None,
                node.text,
                None if not (s := node.attrib['data-ftml-verbalization-subject'].strip('?').strip('#')) else int(s),
            )

            if vr.gf_id not in self.verbalizations:
                self.add_verbalization(vr)

            svr = SymbolVerbRecord(
                symbol=node.attrib['data-ftml-verbalization-symbol'],
                verb_id=vr.gf_id,
                name=n if (n := node.attrib['data-ftml-verbalization-name']) else None,
                distributivity=d if (d := node.attrib['data-ftml-verbalization-args']) else None,
            )
            self.add_symbol_verb(svr)

    def write_gf(self):
        path = MAGMA_PATH / 'generated'
        path.mkdir(exist_ok=True)

        with open(path / f'{self.name}.gf', 'w') as fp:
            # if self.mode == 'forthel':
            #     fp.write('--# -path=../magma:../lexica:../other\n\n')
            #     fp.write(f'abstract {self.name}Grammar = Forthel ** {{\n')
            # elif self.mode == 'ftml':
            fp.write('--# -path=../magma:../lexica:../other:../formulae\n\n')
            fp.write(f'abstract {self.name} = SigFtml ** {{\n')
            fp.write('  fun\n')
            for vr in self.verbalizations.values():
                fp.write(f'    \'{vr.gf_id}\' : {vr.typ};\n')
            fp.write('}\n')

        with open(path / f'{self.name}{self.lang}.gf', 'w') as fp:
            # if self.mode == 'forthel':
            #     fp.write('--# -path=../magma:../lexica:../other\n\n')
            #     fp.write(
            #         f'concrete {self.name}GrammarEng of {self.name}Grammar = ForthelEng ** open SigConstructorsEng, ParadigmsEng, ConstructorsEng in {{\n')
            # elif self.mode == 'ftml':
            fp.write('--# -path=../magma:../lexica:../other:../formulae\n\n')
            fp.write(
                f'concrete {self.name}Eng of {self.name} = SigFtmlEng ** open SigConstructorsEng, ParadigmsEng, ConstructorsEng in {{\n')
            fp.write('  oper\n')
            for wr in self.words.values():
                fp.write(f'    \'{wr.gf_id}\' = {wr.gf_def};\n')
            fp.write('\n  lin\n')
            for vr in self.verbalizations.values():
                fp.write(f'    \'{vr.gf_id}\' = {vr.gf_lin};\n')
            fp.write('}\n')
