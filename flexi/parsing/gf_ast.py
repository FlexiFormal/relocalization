from __future__ import annotations

from typing import Optional


class GfAst:
    node: str
    children: list[GfAst]

    __match_args__ = ("node", "children")

    def __init__(self, node: str, children: Optional[list[GfAst]] = None):
        self.node = node
        self.children = children if children is not None else []

    def to_str(self, _suppress_outer_parens: bool = True) -> str:
        s = " ".join([self.node] + [c.to_str(False) for c in self.children])
        if _suppress_outer_parens or not self.children:
            return s
        return f"({s})"

    def __repr__(self) -> str:
        return f"GfAst({self.node!r}, {self.children!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, GfAst):
            return False
        return self.node == other.node and self.children == other.children

    @classmethod
    def from_str(cls, s: str) -> GfAst:
        stack: list[GfAst] = []
        i = 0

        def read_label() -> str:
            nonlocal i
            label = ""
            while (
                i < len(s)
                and (s[i].isalnum()
                or s[i] in {"_", "'", "/", "?", ":", "#", ".", "-", '"'})
            ):
                # Note: quick hack for string literals (does not allow spaces)
                label += s[i]
                i += 1
            return label

        stack.append(GfAst(read_label()))
        while i < len(s):
            if s[i] == " ":
                i += 1
            elif s[i] == "(":
                i += 1
                new_node = GfAst(read_label())
                stack[-1].children.append(new_node)
                stack.append(new_node)
            elif s[i] == ")":
                i += 1
                if not stack:
                    raise ValueError("Unexpected closing parenthesis")
                stack.pop()
            elif s[i].isalnum() or s[i] in {"_", "'", "/", "?", ":", "#", ".", "-", '"'}:
                stack[-1].children.append(GfAst(read_label()))
            else:
                raise ValueError(f"Unexpected character in AST: {s[i]}")

        if len(stack) != 1:
            raise ValueError("Unmatched opening parenthesis")

        return stack[0]
