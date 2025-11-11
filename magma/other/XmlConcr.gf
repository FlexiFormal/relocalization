incomplete concrete XmlConcr of Xml = {
    lincat
        Tag = {s: Str};

    lin
        tag i = {s = i.s};

    oper
        wrap : Tag -> Str -> Str = \t,s -> "<" ++ t.s ++ ">" ++ s ++ "</" ++ t.s ++ ">";
}
