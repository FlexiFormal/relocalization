resource MagmaUtilsEng = MagmaUtils with (Syntax = SyntaxEng) ** open GrammarEng, ParadigmsEng, ResEng, MorphoEng in {
    oper
        term_to_adv : NP -> Adv = PrepNP (mkPrep "");
        str_adv : Str -> Adv = \s -> lin Adv {s = s};
        property_to_adv : AP -> Adv = \p -> lin Adv {s = p.s ! AgP3Sg Neutr};

        all_Det = lin Det (mkDeterminer plural "all");

        _iff_conj: Conj = mkConj "iff";
        _iff_conj_v1: Conj = mkConj "if and only if";
        _if_conj: Conj = mkConj "" "if";
}
