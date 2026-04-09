incomplete concrete XmlMagmaFunctor of XmlMagma = XmlConcr ** open RglXml, XmlResource in {
    lin
        tag i = {s = i.s};
        ---
        wrapped_named_kind tag nk = {cn = WRAP_CN tag nk.cn; num = nk.num};
        wrapped_fkind tag fk = {cn = WRAP_CN tag fk.cn; adv = fk.adv};
        wrapped_property tag p = WRAP_AP tag p;
        wrapped_stmt tag s = lin S {s = wrap tag s.s};
        wrapped_sentence tag sf = {s = wrap tag sf.s};
        wrapped_term tag t = {np = WRAP_NP tag t.np; just_formula = t.just_formula};
}
