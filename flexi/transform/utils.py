import dataclasses

from flexi.parsing.mast import MAst, G, MT, M, MI, MathArg, MSeq, MathSeqArg
from flexi.transform.placeholders import PlaceholderExpression


_var_counter: int = 0


def get_new_var_id() -> str:
    global _var_counter
    _var_counter += 1
    return f'X{_var_counter}'


@dataclasses.dataclass
class IdentifierAnalysisResult:
    """ work in progress """
    identifiers: list[tuple[str, MAst]]
    restriction: PlaceholderExpression | None


def analyse_identifier(formula: MAst) -> IdentifierAnalysisResult | None:
    # "unwrap" outer layers
    while isinstance(formula, G) and len(formula) == 1 and any(formula.value == p for p in [
        '~cast_term#', '~identifier_term#', '~cast_restricted_identifier#', '~cast_identifier#',
    ]):
        formula = formula[0]

    # TODO: cover more cases

    if len(formula) == 0:
        return IdentifierAnalysisResult(identifiers=[(formula.value, formula)], restriction=None)

    return None


class MastCheck:
    @classmethod
    def is_comma(cls, mast: MAst) -> bool:
        match mast:
            case MI('mo', [MT(',')]):
                return True
        return False


    @classmethod
    def is_var(cls, mast: MAst) -> bool:
        return isinstance(mast, M) and mast.omt == 'OMV'   # TODO: what about informal variables?



class MastGen:
    @classmethod
    def projection(cls, n: int) -> MAst:
        return M(
            'http://mathhub.info?a=smglom/sets&amp;p=mod&amp;m=cartesian-product&amp;s=projectionFN',
            [MI('mn', [MT(str(n))])],
            [
                MI('msub', [
                    MI('mi', [MT('π')]),
                    MathArg('1'),
                ])

            ],
            omt='OMA'
        )

    @classmethod
    def tuple(cls, components: list[MAst]) -> MAst:
        return M(
            'http://mathhub.info?a=smglom/sets&p=mod&m=cartesian-product&s=tuple',
            [MSeq('1', components)],
            [
                MI('mo', [MT('⟨')]),
                MathSeqArg('1', separator=MI('mo', [MT(',')])),
                MI('mo', [MT('⟩')]),
            ],
            omt='OMA'
        )

    @classmethod
    def apply(cls, fun: MAst, arg: MAst) -> MAst:
        return M(
            'http://mathhub.info?a=FTML/meta&m=Metatheory&s=apply',
            [fun, arg],
            [
                MathArg('1'),
                MI('mo', [MT('(')]),
                MathArg('2'),
                MI('mo', [MT(')')]),
            ],
            omt='OMA'
        )

