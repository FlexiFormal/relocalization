incomplete concrete XmlMagmaFunctor of XmlMagma = XmlConcr ** open RglXml in {
    lincat
        Tag = {s: Str};
    lin
        tag i = {s = i.s};
        ---
        -- wrapped_prekind tag pk = WRAP_CN tag pk;
        -- wrapped_named_kind tag nk = WRAP_CN tag nk;
        wrapped_property tag p = WRAP_AP tag p;
        wrapped_stmt tag s = lin S {s = wrap tag s.s};
        wrapped_sentence tag sf = {s = wrap tag sf.s};
}
