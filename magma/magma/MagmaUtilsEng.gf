resource MagmaUtilsEng = MagmaUtils - [ my_ssubjs ] with (Syntax = SyntaxEng) ** open GrammarEng, ParadigmsEng, ResEng, MorphoEng in {
    oper
        term_to_adv : NP -> Adv = PrepNP (mkPrep "");
        str_adv : Str -> Adv = \s -> lin Adv {s = s};
        property_to_adv : AP -> Adv = \p -> lin Adv {s = p.s ! AgP3Sg Neutr};

        all_Det = lin Det (mkDeterminer plural "all");

        _iff_subj: Subj = mkSubj "if and only if";
        _iff_subj_v1: Subj = mkSubj "iff";
        _if_subj: Subj = mkSubj "if";

        -- SSubjS introduces a comma – my impression is that there shouldn't be one
        -- (this is also backed descriptively by looking at a few arxiv samples)
        my_ssubjs : S -> Subj -> S -> S =
            \a,s,b -> lin S {s = a.s ++ s.s ++ b.s} ;
}
