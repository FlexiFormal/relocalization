resource MagmaUtilsGer = MagmaUtils with (Syntax = SyntaxGer) ** open GrammarGer, ParadigmsGer, ResGer, MorphoGer, MakeStructuralGer in {
    oper
        -- term_to_adv : NP -> Adv = PrepNP (mkPrep "");
        -- str_adv : Str -> Adv = \s -> lin Adv {s = s};
        -- property_to_adv : AP -> Adv = \p -> lin Adv {s = p.s ! AgP3Sg Neutr};

        -- all_Det = lin Det (mkDeterminer plural "all");

        _iff_subj: Subj = mkSubj "gdw.";
        _iff_subj_v1: Subj = mkSubj "genau dann, wenn";
        _if_subj: Subj = mkSubj "if";

        _and_str: Str = "und";
}
