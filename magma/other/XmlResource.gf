resource XmlResource = {
    oper
        _Tag : Type = {s: Str};

    oper
        wrap : _Tag -> Str -> Str = \t,s -> "<" ++ t.s ++ ">" ++ s ++ "</" ++ t.s ++ ">";

}
