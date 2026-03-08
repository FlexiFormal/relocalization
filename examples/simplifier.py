from enum import Enum
from flexi.parsing.mast import MAst

class RuleType(Enum):
    R2_1 = "adjective_variable_reduction"
    R2_2 = "verb_variable_reduction"
    R2_3 = "atom_variable_reduction"

class Simplifier:

    def simplify(self, input: MAst, type: RuleType) -> MAst:
        return input
        match type:
            case RuleType.R2_1:
                pass
            case RuleType.R2_2:
                pass
            case RuleType.R2_3:
                pass

    
