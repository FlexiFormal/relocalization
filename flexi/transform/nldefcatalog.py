"""
Catalog of natural language definitions
"""
from flexi.parsing.document import Definition, DocNode, DocText
from flexi.parsing.mast import TermDef


class NlDefCatalog:
    def __init__(self):
        self.definitions: dict[str, list[Definition]] = {}

    def add_document(self, document: DocNode) -> NlDefCatalog:
        for definition in document.find_children(lambda x: isinstance(x, Definition)):
            assert isinstance(definition, Definition)

            definienda: set[str] = set()
            for doctext in document.find_children(lambda x: isinstance(x, DocText)):
                assert isinstance(doctext, DocText)
                for sentence in doctext.sentences:
                    for reading in sentence:
                        for definiendum in reading.find_children(lambda x: isinstance(x, TermDef)):
                            definienda.add(definiendum.value)

            for d in definienda:
                if d not in self.definitions:
                    self.definitions[d] = []
                self.definitions[d].append(definition)

        return self

