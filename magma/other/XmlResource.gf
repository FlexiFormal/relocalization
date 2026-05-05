resource XmlResource = {
    oper
        _Tag : Type = {s: Str};

    oper
        wrap : _Tag -> Str -> Str = \t,s -> "<" ++ t.s ++ ">" ++ s ++ "</" ++ t.s ++ ">";
        wrap_prefix : _Tag -> Str -> Str = \t,s -> "<" ++ t.s ++ ">" ++ s;
        wrap_postfix : _Tag -> Str -> Str = \t,s -> s ++ "</" ++ t.s ++ ">";
}
