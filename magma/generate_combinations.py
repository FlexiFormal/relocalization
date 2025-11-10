"""
NOTE: THIS IS NOT USED ANYMORE
INSTEAD, COMBINATIONS ARE MAINTAINED MANUALLY

This script populates the ``magma/combined`` directory.

``.parsing`` files in that directory will be removed and regenerated whenever this script is run.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import itertools


@dataclass
class Module:
    abstract: str
    concrete: str | dict[str, str]
    name: str

    def get_concrete(self, language: str) -> Optional[str]:
        if isinstance(self.concrete, dict):
            return self.concrete.get(language)
        return self.concrete


PREFIX = """--# -path=../magma:../xml:../testlex:../dollarmath
-- AUTOMATICALLY GENERATED FILE

"""

magma = Module("Magma", {"Eng": "MagmaEng"}, "Magma")
xml = Module("XmlMagma", {"Eng": "XmlMagmaEng"}, "X")
dollarmath = Module("DollarMath", "DollarMathConcr", "D")

testlex = Module("TestEngLex", {"Eng": "TestEngLexConcr"}, "LTen")

directory = Path(__file__).parent / "combined"


print("Delete old combined")

for file in directory.glob("*.parsing"):
    print(f"    Deleting {file}")
    file.unlink()

print("Generating new combined")

extensions = [xml, dollarmath]
# lexica cannot be combined with other lexica
lexica = [None, testlex]

for n in range(1, len(extensions) + 1):
    for xcombo in itertools.combinations(extensions, n):
        for lex in lexica:
            if lex is not None:
                combo = list(xcombo) + [lex, magma]
            else:
                combo = list(xcombo) + [magma]
            name = "".join(mod.name for mod in combo)

            combo = [magma] + combo[
                :-1
            ]  # if magma is in front, we get an error (GF bug?)

            print(f"    Generating {name}")

            with open(directory / f"{name}.parsing", "w") as f:
                f.write(PREFIX)
                f.write(
                    f"abstract {name} = "
                    + ", ".join(mod.abstract for mod in combo)
                    + "\n"
                )

            assert isinstance(magma.concrete, dict)
            for lang in magma.concrete.keys():
                concretes = [
                    cm for mod in combo if (cm := mod.get_concrete(lang)) is not None
                ]
                if all(concretes):
                    with open(directory / f"{name}{lang}.parsing", "w") as f:
                        f.write(PREFIX)
                        f.write(
                            f"concrete {name}{lang} of {name} = "
                            + ", ".join(concretes)
                            + "\n"
                        )
