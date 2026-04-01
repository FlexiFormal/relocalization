import dataclasses

from flexi.parsing.mast import MAst, G
from flexi.transform.placeholders import PlaceholderExpression


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
